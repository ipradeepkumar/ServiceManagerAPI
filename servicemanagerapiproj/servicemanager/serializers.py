from dataclasses import fields
from rest_framework import serializers
from servicemanager.models import Task, TaskIteration


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('GUID','TotalIterations', 'Status','CurrentIteration','TestResults','AxonLog','IterationResult','AzureLink')

class TaskIterationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskIteration
        fields = ('TaskID', 'GUID', 'JSONData', 'CreatedData', 'CreatedBy')