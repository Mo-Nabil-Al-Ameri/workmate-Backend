from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),       
    path('departments/', include('departments.urls')), 
    path('jobs/', include('jobs.urls')),               
]
