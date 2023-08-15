from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
import environ, os, ast
from cryptography.fernet import Fernet
# Create your models here.
class Answer(models.Model):
    questionIdd = models.ForeignKey(
        "userapp.Question", on_delete=models.CASCADE, related_name='answers')
    answer_title = models.CharField(max_length=100, null=True, blank=True)

    answer_weight = models.CharField(max_length=150,  null=True, blank=True)
    answer_weight_for_hashing = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer_dependens_on = models.ForeignKey('self', on_delete=models.PROTECT,
                                             null=True,
                                               blank=True)
    stage_fit = models.OneToOneField('app.Stage', on_delete=models.PROTECT, null=True,blank=True)
    
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


    def save(self, *args, **kwargs):
        env = environ.Env()
        environ.Env.read_env()
        hash_key = ast.literal_eval(env("hash_key"))
        cipher = Fernet(hash_key)
        self.answer_weight = cipher.encrypt(self.answer_weight_for_hashing.encode())
        return super().save(*args, **kwargs)

    def get_stage_slug(self):
        if self.stage_fit is not None:
            return self.stage_fit.slug
        return None
    

    def __str__(self):
        if self.questionIdd_id:
            return "answer={}; question={}".format(self.answer_title, self.questionIdd.question_title)
        else:
            return "answer={}; question=None".format(self.answer_title)
    
class Question(models.Model):

    question_title = models.CharField(verbose_name='question', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stage=models.ForeignKey('app.Stage', related_name = 'questions', on_delete=models.CASCADE)
    question_dependens_on_answer = models.ForeignKey('userapp.Answer', related_name = 'questions', blank=True,null=True, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, blank=True, null=True)
    question_dependens_on_question = models.ForeignKey('self', blank=True, null=True, related_name='question_depend', on_delete=models.CASCADE)
    question_index = models.IntegerField(blank=True, null=True)
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
        ordering = ['stage__stage_name', 'question_index']

    def __str__(self):
        
        return self.question_title

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

#first_name, last_name, email, password,password2, birth_date, gender, native_language, country

GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),

)

class UserAccount(AbstractBaseUser):
    # username = models.CharField(max_length = 150, unique=True)
    first_name = models.CharField(max_length = 150, null=True, blank = True)
    last_name = models.CharField(max_length = 150, null=True, blank = True)
    email = models.EmailField(unique=True, blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES, blank=True, null=True)
    native_language = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    # age = models.IntegerField(blank=True, null=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    user_info = models.JSONField(blank=True, null=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = "UserAccount"
        verbose_name_plural = "UserAccounts"


    def has_perm(self, perm, obj=None):
      return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser    
    def __str__(self):
        
        return self.email


def file_directory(instance, filname):
    return "report{0}{1}".format(instance.id, filname)


class UserProfile(models.Model):
    user = models.ForeignKey(
        'userapp.UserAccount', models.CASCADE
    )
    report_file = models.FileField(upload_to='images/') 

    def __str__(self) -> str:
        return self.user.email 
    
    def delete(self,*args,**kwargs):
        self.report_file.delete(save=False)
        super().delete(*args, **kwargs)
