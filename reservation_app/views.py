from django.shortcuts import render, redirect
from reservation_app.models import Room
from django.views import View

class startPage(View):
    def get(self, request):
        return render(request, 'root.html')



class addRoom(View):
    def get(self, request):
        return render(request, 'add_new_room.html')

    def post(self, request):
        name_of_room = request.POST.get('room-name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector_accessibility = request.POST.get('projector') == 0

        if len(name_of_room) !=0\
                and not Room.objects.filter(name=name_of_room).first() and capacity > 0:
            Room.objects.create(name=name_of_room,
                                  capacity=capacity,
                                  projector=projector_accessibility)
            return redirect("start")
        else:
            raise Exception("You data is incorrect")









