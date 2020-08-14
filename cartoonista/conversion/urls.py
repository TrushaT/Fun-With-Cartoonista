from django.urls import path 
from . import views
app_name = 'conversion'

urlpatterns = [
    path('',views.upload , name = 'upload'), 
    path('share/', views.share, name ='share'),

]