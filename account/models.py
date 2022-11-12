import uuid

# completely creating new model insted extending existing django user model
# settings--> add model ,and custom user model credentiols ,so we can access account app by imprting setting
# also change store/model.py chane user data collection by import django.auth.user to import setting
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# abstract overide the account management of super user,baseuser to build our own  user model,permission for new model
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _  # transalation


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:  # flagging to user interface
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address"))  # "_" is allow transalation

        email = self.normalize_email(email)  # email validating
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    # abstractbase user handle password respected user name django defult setup

    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20, blank=True)

    # User Status
    is_active = models.BooleanField(default=False)
    # after email verification active,if user delete account only deactivating still keeping the data
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()  # to save user

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"  # verbose name is showned in account

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "l@1.com",
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Address
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # uuid provide unique string long custom override defult customer primary key
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"
