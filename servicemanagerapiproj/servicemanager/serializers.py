from rest_framework import serializers
from servicemanager.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('GUID','TotalIterations', 'Status','CurrentIteration')