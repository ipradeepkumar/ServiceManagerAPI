from django.urls import path
from servicemanager.views import PostTask, GetAllTasks, GetPlatformCounters, GetPlatformEvents, ProcessEventCounters

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('posttask/', PostTask, name='posttask'),
    path('getalltasks/', GetAllTasks, name='getalltasks'),
    path('event/<platformID>', GetPlatformEvents, name='platform_events'),
    path('counter/<eventID>', GetPlatformCounters, name='platform_counter'),
    path('processeventcounter/', ProcessEventCounters, name='processeventcounter'),
]