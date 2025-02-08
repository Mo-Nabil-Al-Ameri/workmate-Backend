from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),       
    path('departments/', include('departments.urls')), 
    path('jobs/', include('jobs.urls')),    
    path('attendant/', include('attendant.urls')),
    path('tasks/', include('task.urls')),
    path('leaves/', include('leave.urls')),
    path('messages/', include('messagingapp.urls')),
    path('notifications/', include('notifications.urls')),
           
]
