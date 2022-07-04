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


class roomCollection(View):
    def get(self, request):
        allRooms = Room.objects.all()
        if allRooms:
            return render(request, 'all_rooms_list.html', context={'rooms':allRooms})
        else:
            return render(request, 'all_rooms_list.html', context={'error': "There is no rooms"})

class roomBook(View):
    pass

class roomEdit(View):
    def get(self, request, room_id):
        roomToEdit = Room.objects.get(pk=room_id)
        if roomToEdit:
            return render(request, 'crud/edit.html', context = {'room':roomToEdit})

    def post(self, request, room_id):
        roomToEdit = Room.objects.get(pk=room_id)
        roomNewName = request.POST.get("room_name")
        roomCapacity = request.POST.get("capacity")
        roomProjector = request.POST.get("room_projector") == "on"

        if len(roomNewName) < 0:
            return render(request, "crud/edit.html", context={"room": roomNewName,
                                                         "error": "Name should have more than 1 sign"})

        if int(roomCapacity) <= 0:
            return render(request, "crud/edit.html", context={"room": roomNewName,
                                                         "error": "Capacity should be bigger than 1"})

        if roomNewName != roomToEdit.name and Room.objects.filter(name=roomNewName).first():
            return render(request, 'crud/edit.html', context={"error": "There is such room already in database"})

        Room.objects.filter(pk=room_id).update(name=roomNewName, capacity=roomCapacity,
                                                           projector=roomProjector)
        # roomToEdit.name = roomNewName
        # roomToEdit.capacity = roomCapacity
        # roomToEdit.projector_availability = roomProjector
        # roomToEdit.save()
        return redirect("rooms")


class roomDelete(View):
    def get(self, request, room_id):
        roomId = Room.objects.get(id=room_id)
        roomId.delete()
        return redirect("rooms")

class roomInfo(View):
    pass











