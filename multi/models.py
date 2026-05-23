from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Room(models.Model):

    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user1_rooms"
    )

    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user2_rooms"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1} - {self.user2}"


class Message(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    text = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

class Product(models.Model):

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.IntegerField()

    image = models.ImageField(
        upload_to="products/"
    )

    is_sold = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ProductRoom(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer_rooms"
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seller_rooms"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.product.title} - {self.buyer.username}"
    
class ProductMessage(models.Model):

    room = models.ForeignKey(
        ProductRoom,
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.text
    

class ProductChat(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer_chats"
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seller_chats"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title}"

