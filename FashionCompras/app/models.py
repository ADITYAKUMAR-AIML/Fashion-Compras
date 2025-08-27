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

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)   # 👈 usually TextField doesn’t need max_length
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    quantity = models.PositiveIntegerField(default=0)  # 👈 ensures no negative qty
    image = models.ImageField(upload_to="images/", default="images/blank_image.png", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

