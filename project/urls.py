"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #without rest
    path('django/basicjson/', views.without_restframework),

    #using query 
    path('django/query/', views.by_model),

    #using fbv , GET POST from rest framework
    path('rest/fbvlist/', views.fbv_list),

    #using fbv , GET PUT DELETE using PK
    path('rest/fbvlist/<int:pk>', views.fbv_pk),

    #using cbv , GET POST 
    path('rest/cbvlist/', views.Cbv_List.as_view()),

    #using cbv , GET PUT DELETE 
    path('rest/cbvlist/<int:pk>', views.Cbv_pk.as_view()),
]
