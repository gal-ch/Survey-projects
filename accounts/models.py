from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=50, null=True)
    # date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # bio = models.TextField(max_length=500)
    # gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    # city = models.CharField(max_length=50)
    hasProfile = models.BooleanField(default=False)
    # avatar = models.ImageField(blank=True, upload_to=generate_new_filename, default="avatar/default.jpg")

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth', ]

    def __str__(self):
        return self.email

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


def upload_location(instance, filename):
    location= str(instance.user.username)
    return '%s/%s'%(location, filename)


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField()
    bio = models.TextField(max_length=500)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    city = models.CharField(max_length=50)
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True)

    # def __str__(self):
    #     return self.user

    def get_absolute_url(self):
        return reverse("accounts:profile-detail", kwargs={'pk': self.user_id})


class UserJob(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    position = models.CharField(max_length=220)
    location = models.CharField(max_length=220)
    employer_name = models.CharField(max_length=220)

    def __str__(self):
        return self.position








