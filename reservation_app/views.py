from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Reservation
from django.views import View
import datetime

class startPage(View):
    #add here look for new room forrm
    def get(self, request):
        return render(request, 'root.html')

    def post(self, request):
        name = request.POST.get("lk_name")
        capacity = request.POST.get("lk_capacity")
        projector = request.POST.get("projector") == "on"

        rooms = Room.objects.filter(name__contains=name, capacity__gte=capacity, projector=projector)

        if rooms:
            return render(request, 'all_rooms_list.html', context={"rooms": rooms})
        else:
            return render(request, 'all_rooms_list.html', {"error": "Such room doesn't exist"})


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
        for room in allRooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
            return render(request, 'all_rooms_list.html', context={'rooms':allRooms})
        else:
            return render(request, 'all_rooms_list.html', context={'error': "There is no rooms"})

class roomBook(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        allReservations = Reservation.objects.filter(room_id=room)
        return render(request, 'book_the_room.html', context = {"room": room, 'reservations':allReservations})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        comment = request.POST.get('comment')

        date = request.POST.get('date')
        if Reservation.objects.filter(room_id=room, date=date):
            return render(request, 'book_the_room.html', context = {"room": room, 'error': "The room is already reserved"})
        if date < str(datetime.date.today()):
            return render(request, 'book_the_room.html', context={"room": room, "error": "There is a wrong date!"})

        Reservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect("rooms")



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

        return redirect("rooms")


class roomDelete(View):
    def get(self, request, room_id):
        roomId = Room.objects.get(id=room_id)
        roomId.delete()
        return redirect("rooms")

class roomInfo(View):
    def get(self, request, room_id):
        roomId = Room.objects.get(id=room_id)
        reservation = roomId.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, 'details_about_room.html', context={'room':roomId, 'reservation':reservation})











