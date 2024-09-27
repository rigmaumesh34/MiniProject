"""
URL configuration for RIT_BAZAAR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('studentlogin/',views.studentlogin,name='studentlogin'),
    path('studentregister/',views.studentregister,name='studentregister'),
    path('studenthome/',views.studenthome,name='studenthome'),
    path('additem',views.additem,name='additem'),
    path('buyitem',views.buyitem,name='buyitem'),
    path('reportitemfound/',views.reportitemfound,name='reportitemfound'),
    path('reportitemlost/',views.reportitemlost,name='reportitemlost'),
    path('navbar/',views.navbar,name='navbar'),
    
    path('logout/',views.studentlogout,name='logout'),
    path('manageitem/', views.manageitem, name='manageitem'),
    path('deleteitem/<int:item_id>/', views.deleteitem, name='deleteitem'),
    path('edititem/<int:item_id>/', views.edititem, name='edititem'),
    path('manageprofile/', views.manageprofile, name='manageprofile'),
    path('viewitemfound/', views.viewitemfound, name='viewitemfound'),
    path('claimitem/<int:found_item_id>/', views.claimitem, name='claimitem'),
    path('viewitemlost/', views.viewitemlost, name='viewitemlost'),
    path('complaint/', views.complaints, name='complaint'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('confirmpassword/<str:token>/', views.confirmpassword, name='confirmpassword'),
    path('events/',views.eventss,name='events'),
    path('deleteitemfound/<int:item_id>/',views.deleteitemfound, name='deleteitemfound'),
    path('manageitemfound/',views.manageitemfound,name='manageitemfound'),
    path('manageitemlost/',views.manageitemlost,name='manageitemlost'),
    path('deleteitemlost/<int:item_id>/',views.deleteitemlost, name='deleteitemlost'),
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('adminlogout/', views.admin_logout, name='adminlogout'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('approve_item/<int:item_id>/', views.approve_item, name='approve_item'),
    path('reject_item/<int:item_id>/', views.reject_item, name='reject_item'),
    path('adminaddevent', views.admin_addevent, name='adminaddevent'),
    path('viewcomplaints/', views.view_complaints, name='viewcomplaints'),
    path('logout/', views.admin_logout, name='logout'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
