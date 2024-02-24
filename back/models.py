from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    storage = models.PositiveBigIntegerField(default=5)
    already_use = models.PositiveIntegerField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class UserFile(models.Model):
    email = models.EmailField()
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    file_size = models.PositiveIntegerField()
    upload_time = models.DateTimeField(auto_now_add=True)
    folder_name = models.CharField(max_length=255, blank=True, null=True)


# 日志模型
class UserActivity(models.Model):
    user_email = models.EmailField()
    login_count = models.PositiveIntegerField(default=0) # 登录次数
    logout_count = models.PositiveIntegerField(default=0) # 登出次数
    image_detect_count = models.PositiveIntegerField(default=0) # 图片识别次数
    view_detect_count = models.PositiveIntegerField(default=0) # 视频检测次数
    image_restructure_count = models.PositiveIntegerField(default=0) # 图像重构次数
    llms_count = models.PositiveIntegerField(default=0) # 大模型使用次数
    images_infosys_count = models.PositiveIntegerField(default=0) # 信息管理-图片使用次数
    models_count = models.PositiveIntegerField(default=0) # 模型管理
    research_count = models.PositiveIntegerField(default=0) # 研究次数
    dataPreprocess_count = models.PositiveIntegerField(default=0) # 数据预处理

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user_email} - " \
               f"登录次数: {self.login_count}, " \
               f"登出次数: {self.logout_count}, " \
               f"图片识别次数: {self.image_detect_count}, " \
               f"视频检测次数: {self.view_detect_count}, " \
               f"图像重构次数: {self.image_restructure_count}, " \
               f"大模型使用次数: {self.llms_count}, " \
               f"信息管理-图片使用次数: {self.images_infosys_count}, " \
               f"模型管理次数: {self.models_count}, " \
               f"研究次数: {self.research_count}, " \
               f"数据预处理次数: {self.dataPreprocess_count}"