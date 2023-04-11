from datetime import datetime
import io
import json
from multiprocessing import Process
import multiprocessing
import os
import threading
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from servicemanager.serializers import TaskSerializer
from servicemanager.models import Task, TaskIteration, EmonCounter, EmonEvent, Platform, TaskExecutionLog, Station, Tool
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import time
from django.core import serializers
from django.http import HttpResponse
import uuid


@api_view(['GET'])
def GetAllTasks(request):
    serialzer = TaskSerializer(Task.objects.all(), many = True, context={'request': request})
    return Response(data = serialzer.data, status = status.HTTP_200_OK)

@api_view(['POST'])
def PostTask(request):
    taskJson = request.POST['taskJSON']
    jsonStr = taskJson.replace("\r\n\t","").replace("\r\n","")
    dict = json.loads(jsonStr)
    task = Task.objects.create(**dict)
    task.save()
    
    #instance = Task.objects.get_queryset().filter(GUID=request.data['taskJSON']).first()
    #UpdateJsonConfig(instance)

    process = threading.Thread(target=ProcessTask, args=(request, task))
    process.start()
   
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['GET'])
def GetPlatformEvents(request, platformID):
    platformEventData = EmonEvent.objects.filter(Platform__Name = platformID)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', platformEventData)
    return HttpResponse(serialized_obj, content_type="application/json")

@api_view(['GET'])
def GetPlatformCounters(request, eventID):
    list= eventID.split(",")
    emonCounterData = EmonCounter.objects.filter(EmonEvent__EmonEventID__in = list)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', emonCounterData)
    return HttpResponse(serialized_obj, content_type="application/json")

@api_view(['GET'])
def ProcessEventCounters(request):
     dirPath = os.path.dirname(os.path.realpath(__file__))
     filePath = os.path.join(dirPath, "data", "ipx.json")
     #save platform to db
    #  pltfrm = Platform()
    #  pltfrm.Name = "ipx"
    #  pltfrm.PlatformID = Platform.objects.count() + 1
    #  pltfrm.save()

     st = Station.objects.filter(id = 4).first()
    #  st.Name = "Station 2"
    #  st.Desc = "icx"
    #  st.StationID = Station.objects.count() + 1
    #  st.IsActive  = True
    #  st.save()

     with open(filePath, 'r') as eventcounterfile:
        stream = io.BytesIO(str.encode(eventcounterfile.read()))
        eventCounterData = JSONParser().parse(stream=stream)
        i = EmonEvent.objects.count() + 1
        j = EmonCounter.objects.count() + 1
        for key, value in eventCounterData['evts_cts'].items():
            #save event to DB
            evt = EmonEvent()
            evt.EmonEventID = i
            evt.Name = key
            evt.Station = st#Station.objects.get(id = Platform.objects.last().id)
            evt.save()
            #save counter to DB
            for ctr in value:
                counter = EmonCounter()
                counter.Name = ctr
                counter.EmonCounterID = j
                counter.EmonEvent = EmonEvent.objects.get(EmonEventID = EmonEvent.objects.last().EmonEventID)
                counter.save()
                j = j + 1
            i = i + 1
        return HttpResponse(eventCounterData, content_type="application/json")

@api_view(['GET'])
def GetToolNames(request, stationId):
    toolData = Tool.objects.filter(Tool__StationID = stationId)
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', toolData)
    return HttpResponse(serialized_obj, content_type="application/json")

def ProcessTask(req, instance): 
    isValid = False
    ClearPreviousRunData(instance)
    for i in range(instance.TotalIterations):
            userExecution = Task.objects.get(GUID = instance.GUID).IsUserExecution
            if (userExecution == False):
                break
            data = {
                "CurrentIteration": str(i + 1),
                "Status": 'IN-PROGRESS',
                "TestResults": '{Passed: 3,Failed: 2}',
                "AxonLog": 'Logged data',
                "IterationResult": 'Results',
                "AzureLink": "http://www.google.com"
            }
            serializer = TaskSerializer(instance=instance, data=data)
            if serializer.is_valid():
                isValid = True
                serializer.save()

                taskIteration = TaskIteration()
                jsonData = { 'key1': (i + 1), 'key2': 'value2', 'key3': 'value3', 'key4': 'value4' }
                taskIteration.TaskID = instance.id
                taskIteration.GUID = instance.GUID
                taskIteration.JSONData = jsonData
                taskIteration.CreatedDate = datetime.now()
                taskIteration.Iteration = i + 1
                taskIteration.save()
                
                time.sleep(10)
                userExecution = Task.objects.get(GUID = instance.GUID).IsUserExecution
                if (userExecution == False):
                    break
            if (i == instance.TotalIterations - 1):
                compData = {
                    "Status": 'COMPLETED'
                }
                compSerializer = TaskSerializer(instance=instance, data=compData)
                if compSerializer.is_valid():
                    compSerializer.save()
            
    if (i == instance.TotalIterations - 1):
        SaveTaskExecutionLog(req, instance, 'COMPLETED')
        task = Task.objects.get(GUID = instance.GUID)
        task.IsEowynExecution = True
        task.IsUserExecution = True
        task.CurrentIteration = instance.TotalIterations
        task.Status = 'COMPLETED'
        task.save()
        MakeStationActive(instance=instance)
    else:
        SaveTaskExecutionLog(req, instance, 'STOPPED')
        task = Task.objects.get(GUID = instance.GUID)
        task.IsEowynExecution = False
        task.Status = 'STOPPED'
        task.save()
        MakeStationActive(instance=instance)
       
            
    return isValid

def UpdateJsonConfig(instance):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join("servicemanagerapiproj", "eowyn_inputs","mlc_xmli_cli_config.json")
    with open(filePath, 'r') as configFile:
     stream = io.BytesIO(str.encode(configFile.read()))
     configJson = JSONParser().parse(stream=stream)
     configJson['Eowyn']['regression_name'] = instance.RegressionName
     targetPath = os.path.join("servicemanagerapiproj", "eowyn_inputs","test.json")
     file1 = open(targetPath, "w")
     file1.write(str(configJson))
     file1.close()
     return configJson

def ClearPreviousRunData(instance):
        data = {
            "CurrentIteration": 0,
            "Status": 'IN-PROGRESS',
            "TestResults": '',
            "AxonLog": '',
            "IterationResult": '',
            "AzureLink": ""
        }
        serializer = TaskSerializer(instance=instance, data=data)
        if serializer.is_valid():
                serializer.save()
        TaskIteration.objects.filter(GUID=instance.GUID).delete()

def SaveTaskExecutionLog(req, instance, status):
        executionLog = TaskExecutionLog(
        TaskID = instance.TaskID,
        GUID = instance.GUID,
        StatusDate = datetime.utcnow(),
        Status = status,
        CreatedBy = req.user.username,
        CreatedDate = datetime.utcnow()) 
        executionLog.save()

def MakeStationActive(instance):
    station = Station.objects.get(Name=instance.Station)
    station.IsActive = True
    station.save()