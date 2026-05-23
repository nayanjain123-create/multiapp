from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Task, Room, Message, Product, ProductRoom, ProductMessage
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return redirect('signin')
    return render(request,'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def home(request):
    return render(request, 'home.html')

# todo app views

@login_required
def todo_app(request):
    task = Task.objects.filter(user=request.user)
    return render(request,'todo_app.html',{'task':task})

@login_required
def task_add(request):
    return render(request,'task_add.html')

@login_required
def add_task(request):
    if request.method == "POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        Task.objects.create(title=title,description=description, user=request.user)
    return redirect('todo_app')

@login_required
def task_edit(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request,'task_edit.html',{'task':task})

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.updated_at = timezone.now()
        task.save()
        return redirect('todo_app')
    
@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('todo_app')

# chat app views

@login_required
def chat_app(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request,'chat_app.html',{'users':users})

@login_required
def start_chat(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    room = Room.objects.filter(

        Q(user1=request.user, user2=other_user) |
        Q(user1=other_user, user2=request.user)

    ).first()

    if not room:

        room = Room.objects.create(
            user1=request.user,
            user2=other_user
        )

    return redirect("chat_room", room.id)

@login_required
def chat_room(request, room_id):

    room = get_object_or_404(
        Room,
        id=room_id
    )

    # find other user
    if room.user1 == request.user:
        other_user = room.user2
    else:
        other_user = room.user1

    messages = Message.objects.filter(
        room=room
    ).order_by("timestamp")

    return render(request, "chat.html", {
        "messages": messages,
        "other_user": other_user,
        "room_id": room.id
    })

# olx app views

def olx_app(request):

    products = Product.objects.exclude(
        seller=request.user
    )

    product_data = []

    for product in products:

        room = ProductRoom.objects.filter(
            product=product,
            buyer=request.user
        ).first()

        has_new_message = False

        if room:

            last_message = ProductMessage.objects.filter(
                room=room
            ).last()

            if last_message and last_message.sender != request.user:
                has_new_message = True

        product_data.append({
            "product": product,
            "room": room,
            "has_new_message": has_new_message
        })

    # SELLER CHAT LIST
    seller_rooms = ProductRoom.objects.filter(
        seller=request.user
    )

    context = {
        "product_data": product_data,
        "seller_rooms": seller_rooms
    }

    return render(
        request,
        "olx_app.html",
        context
    )

@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user).order_by("-id")
    return render(request, "my_products.html", {
        "products": products
    })

@login_required
def add_product(request):

    if request.method == "POST":

        title = request.POST.get("title")

        description = request.POST.get("description")

        price = request.POST.get("price")

        image = request.FILES.get("image")

        Product.objects.create(
            seller=request.user,
            title=title,
            description=description,
            price=price,
            image=image
        )

        return redirect("olx_app")

    return render(request, "add_product.html")

def delete_product(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )
    product.delete()
    return redirect("my_products")

@login_required
def mark_sold(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    product.is_sold = True

    product.save()

    return redirect("olx_app")

@login_required
def start_product_chat(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    room = ProductRoom.objects.filter(
        product=product,
        buyer=request.user
    ).first()

    if not room:

        room = ProductRoom.objects.create(
            product=product,
            buyer=request.user,
            seller=product.seller
        )

    return redirect(
        "product_chat_room",
        room.id
    )

@login_required
def product_chat_room(request, room_id):

    room = get_object_or_404(
        ProductRoom,
        id=room_id
    )

    messages = ProductMessage.objects.filter(
        room=room
    ).order_by("created_at")

    return render(request, "product_chat.html", {
        "room": room,
        "messages": messages
    })