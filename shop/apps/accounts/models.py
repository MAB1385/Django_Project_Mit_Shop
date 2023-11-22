from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from utils import FileUpload


#! A way to build a user model without using the default model:
class CustomUserManager(
    BaseUserManager
):  # ? Child of the BaseUserManager class --> Manage user creation
    #! For normal user:
    def create_user(
        self,
        mobail_number,
        email="",
        name="",
        family="",
        active_code=None,
        gender=None,
        password=None,
    ):
        if not mobail_number:  # ? Chake mobail_number
            raise ValueError("باید شماره موبایل را وارد کنید")
        if (
            len(mobail_number) != 11 or "09" != mobail_number[:2]
        ):  # ? Chake mobail_number
            raise ValueError("این شماره موبایل نا معتبر می باشد")
        user = self.model(
            mobail_number=mobail_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
        )
        user.set_password(password)  # ? hash password
        user.save(using=self._db)  # ? saving the model
        return user

    #! For super user:
    def create_superuser(
        self,
        mobail_number,
        email,
        name,
        family,
        active_code=None,
        gender=None,
        password=None,
    ):
        user = self.create_user(
            mobail_number=mobail_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)  # ? saving the model
        return user


# todo --------------------------------------------------------------------------
class CustomUser(
    AbstractBaseUser, PermissionsMixin
):  #! Child of the AbstractBaseUser class and PermissionsMixin class
    mobail_number = models.CharField(
        max_length=11, unique=True, verbose_name="شماره موبایل"
    )
    email = models.EmailField(max_length=200, blank=True, verbose_name="ایمیل")
    name = models.CharField(max_length=50, blank=True, verbose_name="نام")
    family = models.CharField(max_length=50, blank=True, verbose_name="نام خانوادگی")
    # ? GENDER_CHOICES for choices gender
    GENDER_CHOICES = [
        ("True", "مرد"),
        ("False", "زن"),
    ]
    gender = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=GENDER_CHOICES,
        default="True",
        verbose_name="جنسیت",
    )
    register_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ درج")
    is_active = models.BooleanField(default=False, verbose_name="فعال / غیر فعال")
    active_code = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="کد فعال سازی"
    )
    is_admin = models.BooleanField(default=False, verbose_name="ادمین / غیر ادمین")

    USERNAME_FIELD = "mobail_number"  # ? Field equivalent to username
    REQUIRED_FIELDS = [
        "email",
        "name",
        "family",
    ]  # ? The important fields to build a super user

    objects = CustomUserManager()  # ? Communicate with CustomUserManager class

    def __str__(self) -> str:
        return f"{self.name} {self.family} {self.mobail_number}"

    @property
    def is_staff(self):  # ? Access to admin panel
        return self.is_admin

    # // Access level(PermissionsMixin):
    # // def has_perms(self, perm_list, obj=None):#When log in site -->
    # //     return True
    # // def has_module_perms(self, app_label):
    # //     return True
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"


# todo --------------------------------------------------------------------------
class Customer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="کاربر",
        related_name="coustomer",
    )
    phone_number = models.CharField(
        max_length=11, null=True, blank=True, verbose_name="شماره موبایل"
    )
    address = models.TextField(null=True, blank=True, verbose_name="آدرس")
    file_upload = FileUpload("images", "customer")
    image = models.ImageField(
        upload_to=file_upload.upload_to,
        verbose_name="تصویر پروفایل",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری ها"
