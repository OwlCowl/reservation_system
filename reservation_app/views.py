from django.shortcuts import render, redirect
from .models import Room
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
        projector_accessibility = request.POST.get('projector') == "on"

        if not name_of_room:
            return render(request, "add_new_room.html", context={"error": "Please provide correct name of room"})
        if capacity < 1:
            return render(request, "add_new_room.html", context={"error": "Wrong capacity"})
        if Room.objects.filter(name=name_of_room).first():
            return render(request, "add_new_room.html", context={"error": "This room is already exist"})
        try:
            Room.objects.get(name=name_of_room)
        except Room.DoesNotExist:
            Room.objects.create(name=name_of_room,
                                  capacity=capacity,
                                  projector=projector_accessibility)

        return redirect('start')












