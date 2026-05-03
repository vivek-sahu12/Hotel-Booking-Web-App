from django.shortcuts import render,redirect
from .models import Room,Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

#LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('rooms')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')
#SIGNUP
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully!")

        return redirect('login')

    return render(request, 'signup.html')

#LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')

def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'rooms.html', {'rooms': rooms})  

@login_required
def book_room(request, room_id):
    room = Room.objects.get(id=room_id)

    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

        days = (datetime.strptime(check_out, "%Y-%m-%d") - 
                datetime.strptime(check_in, "%Y-%m-%d")).days

        total_price = days * room.price

        Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price
        )

        room.is_available = False
        room.save()

        # ✅ SUCCESS MESSAGE
        messages.success(request, "🎉 Room booked successfully!")

        return redirect('rooms')   # 👈 important

    return render(request, 'book.html', {'room': room})