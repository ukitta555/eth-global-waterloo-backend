import datetime

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models import Q
from django.db.models.functions import Length

from overrated.consts import SECONDS_IN_A_WEEK, SECONDS_IN_4_BLOCKS

models.TextField.register_lookup(Length)
class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    additional_reputation_for_phantom_account = models.FloatField(default=0)
    last_reputation_bump_for_phantom_account = models.DateTimeField(
        default=datetime.datetime(
            year=1970,
            month=1,
            day=1,
            hour=12,
            minute=0,
            second=0,
            tzinfo=datetime.timezone.utc
        )
    )
    public_key = models.TextField()

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email

    def reputation_before_removing_phantom(self):
        print("Calculating reputation with exp. decay...")
        time_diff: datetime.timedelta = datetime.datetime.now(tz=datetime.timezone.utc) - self.last_reputation_bump_for_phantom_account
        number_of_4_block_periods_passed: float = time_diff.total_seconds() / SECONDS_IN_4_BLOCKS
        print(f"Reputation after decay: "
              f"{int(self.additional_reputation_for_phantom_account * 2**(-number_of_4_block_periods_passed))}")
        return int(self.additional_reputation_for_phantom_account * 2**(-number_of_4_block_periods_passed))

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
