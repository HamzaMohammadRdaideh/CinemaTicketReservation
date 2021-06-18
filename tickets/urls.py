from django.db import router
from django.urls import path
from django.urls.conf import include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', views.View_sets_guest)
router.register('movies', views.View_sets_movie)
router.register('reservations', views.View_sets_reservation)

urlpatterns = [
    #Without rest
    path('django/basicjson/', views.without_restframework),

    #Using query 
    path('django/query/', views.by_model),

    #Using fbv , GET POST from rest framework
    path('rest/fbvlist/', views.fbv_list),

    #Using fbv , GET PUT DELETE using PK
    path('rest/fbvlist/<int:pk>', views.fbv_pk),

    #Using cbv , GET POST 
    path('rest/cbvlist/', views.Cbv_List.as_view()),

    #Using cbv , GET PUT DELETE 
    path('rest/cbvlist/<int:pk>', views.Cbv_pk.as_view()),

    #Using Mixins and Generic  from rest framework => List
    path('rest/mixinlist/', views.mixins_list.as_view()),

    #Using Mixins and Generic  from rest framework => PUT GET DELETE
    path('rest/mixinlist/<int:pk>', views.mixins_pk.as_view()),

    #Using Generics from rest framework => List
    path('rest/genericlist/', views.Genericslist.as_view()),

    #Using Generics from rest framework => GET PUT UPDATE
    path('rest/genericlist/<int:pk>', views.Generics_pk.as_view()),

    #Using ViewSet
    path('rest/viewsets/',include(router.urls)),

    # *-------------------------------------------*
    #Find movie fbv
    path('fbv/findmovie/',views.find_movie),

    #New reservation fbv
    path('fbv/newreservation/',views.new_reservation),
]