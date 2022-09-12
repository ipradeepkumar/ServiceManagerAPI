from django.urls import path
from servicemanager.views import PostTask, GetAllTasks

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('posttask/', PostTask, name='posttask'),
    path('getalltasks/', GetAllTasks, name='getalltasks')
]