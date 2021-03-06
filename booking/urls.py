"""booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from reservation_app.views import startPage, addRoom, roomCollection, roomDelete, roomEdit,roomBook, roomInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('start/', startPage.as_view(), name='start'),
    path('room/new/', addRoom.as_view(), name='add_room'),
    path('rooms/', roomCollection.as_view(), name='rooms'),
    path('room/delete/<int:room_id>/', roomDelete.as_view(), name='delete'),
    path('room/modify/<int:room_id>/', roomEdit.as_view(), name='edit'),
    path('room/reserve/<int:room_id>/', roomBook.as_view(), name='book'),
    path('room/<int:room_id>/', roomInfo.as_view(), name='info')

]
