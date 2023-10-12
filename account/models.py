from locale import normalize
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import uuid

class usercoremanager(BaseUserManager):

    def create_user(self,username,email,phone,password):
        if not username:
            raise ValueError("username is required")
        if not email:
            raise ValueError("email is required")
        if not phone:
            raise ValueError("phone number needs to be valid")

        user=self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            max_table_normal=0,
            max_table_not_normal=0
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,phone,password):
        if not username:
            raise ValueError("username is required")
        if not email:
            raise ValueError("email is required")
        if not phone:
            raise ValueError("phone number needs to be valid")

        user=self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            is_admin=True,
            is_staff=True,
            is_superuser=True,
            user_type=1,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class usercore(AbstractBaseUser):

    username = models.CharField(max_length=200, verbose_name='username',unique=True)
    email = models.EmailField(unique=True,max_length=50,verbose_name='place mail adress')
    name = models.CharField(max_length=200, verbose_name='name',blank=True, null=True,default=None)
    surname = models.CharField(max_length=200, verbose_name='surname',blank=True, null=True,default=None)
    
    pic1 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic1",blank=True, null=True)
    pic2 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic2",blank=True, null=True)
    pic3 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic3",blank=True, null=True)
    pic4 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic4",blank=True, null=True)
    pic5 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic5",blank=True, null=True)

    firebase_messaging_token = models.CharField(max_length=255, null=True, blank=True)
    
    wantToKnowHash = models.ManyToManyField("activities.hashtags", verbose_name='want to know' ,related_name="wanttoknowh+",null=True,blank=True)
    wantToKnowComm = models.ManyToManyField("activities.communities", verbose_name='want to know' ,related_name="wanttoknowc+",null=True,blank=True)
    wantToKnowPlac = models.ManyToManyField("activities.places", verbose_name='want to know' ,related_name="wanttoknowp+",null=True,blank=True)

    IKnowAct = models.ManyToManyField("activities.activities", verbose_name='want to know' ,related_name="wanttoknowact+",null=True,blank=True)

    firstLogin = models.BooleanField(verbose_name="firstLogin",default=True)

    gender = models.CharField(
        max_length=10,
        choices=[('Kadın','Kadın'),('Erkek','Erkek'),('Diğer','Diğer')]
   ,blank=True, null=True,default=None)
    
    phone = models.IntegerField(unique=True,verbose_name='phone')
    money = models.IntegerField(verbose_name="money",blank=True, null=True)

    date_joined = models.DateTimeField(auto_now=True,verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True,verbose_name="last login")

    is_admin= models.BooleanField(default=False,verbose_name="is admin")
    is_superuser=models.BooleanField(default=False,verbose_name="is superuser")
    is_staff=models.BooleanField(default=False,verbose_name="is staff")
    user_type = models.IntegerField(default=2,verbose_name='user_type')

    USERNAME_FIELD="username"

    REQUIRED_FIELDS=["email","phone"]

    objects=usercoremanager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True       
    