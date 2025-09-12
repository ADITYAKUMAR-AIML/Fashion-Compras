from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AuthManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Auth(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AuthManager()

    def __str__(self):
        return self.email


from django.db import models

from django.db import models

from django.db import models

class Item(models.Model):
    CATEGORY_CHOICES = [
        ("fashion", "Fashion"),
        ("electronics", "Electronics"),
        ("food", "Food"),
        ("home", "Home"),
        ("gaming", "Gaming"),
    ]
    user = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name="items")#A user's items.
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="item_images/", default="blank_image.png")

    def __str__(self):
        return f"Image for {self.item.name}"


class Specification(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="specifications")
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"
