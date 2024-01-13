from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="direccion de correo electronico", unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    groups = models.ManyToManyField(
        Group, verbose_name="grupos", blank=True, related_name="authentication_users_groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="permisos del usuario",
        blank=True,
        related_name="authentication_users_permissions"
    )