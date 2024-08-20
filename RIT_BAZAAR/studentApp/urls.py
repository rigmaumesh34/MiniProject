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

from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('studentlogin/',views.studentlogin,name='studentlogin'),
    path('studentregister/',views.studentregister,name='studentregister'),
    path('studenthome/',views.studenthome,name='studenthome'),
    path('additem/',views.additem,name='additem'),
    path('reportitemfound/',views.reportitemfound,name='reportitemfound'),
    path('reportitemlost/',views.reportitemlost,name='reportitemlost'),
    path('navbar/',views.navbar,name='navbar'),
    path('events/',views.navbar,name='events'),
    path('logout/',views.studentlogout,name='logout'),
]
