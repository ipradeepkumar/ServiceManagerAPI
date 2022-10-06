from datetime import datetime
import io
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from servicemanager.serializers import TaskSerializer, TaskIterationSerializer
from servicemanager.models import Task, TaskIteration
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import time
from django.http import HttpResponse




@api_view(['GET'])
def GetAllTasks(request):
    serialzer = TaskSerializer(Task.objects.all(), many = True, context={'request': request})
    return Response(data = serialzer.data, status = status.HTTP_200_OK)

@api_view(['POST'])
def PostTask(request):
    instance = Task.objects.get_queryset().filter(GUID=request.data['GUID']).first()
    UpdateJsonConfig(instance)
    ProcessTask(instance=instance)
    return HttpResponse(status=status.HTTP_200_OK)

def ProcessTask(instance): 
    isValid = False
    for i in range(instance.TotalIterations):
            data = {
                "CurrentIteration": str(i + 1),
                "Status": 'IN-PROGRESS'
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
                
                time.sleep(5)
    if (i == instance.TotalIterations - 1):
        compData = {
            "Status": 'COMPLETED'
        }
        compSerializer = TaskSerializer(instance=instance, data=compData)
        if compSerializer.is_valid():
            compSerializer.save()
    return isValid

def UpdateJsonConfig(instance):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join("servicemanagerapiproj", "eowyn_inputs","mlc_xmli_cli_config.json")
    with open(filePath, 'r') as configFile:
     stream = io.BytesIO(str.encode(configFile.read()))
     configJson = JSONParser().parse(stream=stream)
     configJson['Eowyn']['regression_name'] = instance.RegressionName
     return configJson