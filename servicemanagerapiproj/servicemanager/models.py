from math import fabs
from pickle import FALSE
from platform import platform
import uuid
from django.db import models


# Create your models here.
class Station(models.Model):
    StationID = models.IntegerField()
    Name = models.CharField(max_length=250)
    Desc = models.CharField(max_length=500)

class Tool(models.Model):
    ToolID = models.IntegerField(primary_key=True, unique=False)
    Name = models.CharField(max_length=150)

class ToolEvent(models.Model):
    ToolEventID = models.IntegerField(primary_key=True, unique=False)
    Name = models.CharField(max_length=150)
    Tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, related_name="toolevents")

class ToolCounter(models.Model):
    ToolCounterID = models.IntegerField(primary_key=True, unique=False)
    Name = models.CharField(max_length=150)
    ToolEvent = models.ForeignKey(ToolEvent, on_delete=models.SET_NULL, null=True, related_name="toolcounterevents")

class Platform(models.Model):
    PlatformID = models.IntegerField()
    Name = models.CharField(max_length=150)

class EmonEvent(models.Model):
    EmonEventID = models.IntegerField()
    Name = models.CharField(max_length=150)
    Platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, related_name="emonevents")

class EmonCounter(models.Model):
    EmonCounterID = models.IntegerField()
    Name = models.CharField(max_length=150)
    EmonEvent = models.ForeignKey(EmonEvent, on_delete=models.SET_NULL, null=True, related_name="emoncounters")

class Idea(models.Model):
    IdeaID = models.IntegerField()
    Name = models.CharField(max_length=200)

class TaskStatus(models.Model):
    TaskStatusID = models.IntegerField()
    Name = models.CharField(max_length=50)

class Task(models.Model):
    TaskID = models.IntegerField()
    Station = models.CharField(max_length=250, null=True)
    IsDebugMode = models.BooleanField(default=FALSE)
    RegressionName = models.CharField(max_length=250)
    Tool = models.CharField(max_length=250, null=True)
    ToolEvent = models.CharField(max_length=500, null= True)
    ToolCounter = models.CharField(max_length=500, null=True)
    Platform = models.CharField(max_length=500, null=True)
    IsEmon = models.BooleanField(default=False)
    PlatformEvent = models.CharField(max_length=500, null=True)
    PlatformCounter = models.CharField(max_length=500, null=True)
    Idea = models.CharField(max_length=500, null=True)
    IsUploadResults = models.BooleanField(default=False)
    TotalIterations = models.IntegerField(default=2)
    Splitter = models.CharField(max_length=50)
    MinImpurityDecrease = models.CharField(max_length=50)
    MaxFeatures = models.CharField(max_length=50)
    CreatedBy = models.CharField(max_length=50)
    CreatedDate = models.DateTimeField()
    ModifiedBy = models.CharField(max_length=50, null=True)
    ModifiedDate = models.DateTimeField(null=True)
    ErrorCode = models.CharField(max_length=10, null=True)
    ErrorMessage = models.CharField(max_length=500, null=True)
    Status = models.CharField(max_length=50, null=True, default="PENDING")
    GUID = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    CurrentIteration = models.IntegerField(default=0)

class TaskIteration(models.Model):
    TaskID = models.IntegerField(null=True)
    GUID = models.UUIDField(primary_key=False)
    Iteration = models.IntegerField(null=True)
    JSONData = models.JSONField(null=True)
    CreatedDate =  models.DateTimeField(null=True)
    CreatedBy = models.CharField(max_length=50, null=True)