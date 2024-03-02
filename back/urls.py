from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us', views.about_us, name='about_us'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('personal/', views.personal, name='personal'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/get_user_activity_info', views.get_user_activity_info, name='get_user_activity_info'),
    path('dashboard/get_user_storage', views.get_user_storage, name='get_user_storage'),
    path('get_hardware_usage/', views.get_hardware_usage, name='get_hardware_usage'),
    path('infoSys', views.infoSys, name='infoSys'),
    path('infoSys/UserImages', views.infoSys_userImages, name='UserImages'),
    path('sea_eyes/', views.sea_eyes, name='sea_eyes'),
    path('sea_eyes/upload_images', views.uploadImages, name='upload_images'),
    path('sea_eyes/upload_videos', views.uploadVideos, name='upload_videos'),
    path('sea_eyes/upload_images/detect_results', views.detect_results, name='detect_results'),
    path('sea_eyes/upload_videos/video_show', views.video_show, name='video_show'),
    path('sea_llm/', views.sea_llms, name='sea_llms'),
]
