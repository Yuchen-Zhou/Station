from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('personal/', views.personal, name='personal'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('infoSys', views.infoSys, name='infoSys'),
    path('sea_eyes/', views.sea_eyes, name='sea_eyes'),
    path('sea_eyes/upload_images', views.uploadImages, name='upload_images'),
    path('sea_eyes/upload_videos', views.uploadVideos, name='upload_videos'),
    path('sea_eyes/upload_images/detect_results', views.detect_results, name='detect_results'),
    path('sea_eyes/upload_videos/video_show', views.video_show, name='video_show'),
    path('sea_llm/', views.sea_llms, name='sea_llms'),
]
