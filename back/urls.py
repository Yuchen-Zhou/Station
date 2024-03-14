from django.urls import path
from .views import index as index_views
from .views import users as users_views
from .views import dashboard as dashboard_views
from .views import sea_infosys as infosys_views
from .views import sea_vision as vision_views
from .views import sea_llms as llms_views

urlpatterns = [
    # 首页部分
    path('', index_views.index, name='index'),
    path('about_us', index_views.about_us, name='about_us'),
    # 用户部分
    path('register/', users_views.user_register, name='register'),
    path('login/', users_views.user_login, name='login'),
    path('logout/', users_views.user_logout, name='logout'),
    path('personal/', users_views.personal, name='personal'),
    # 控制台部分
    path('dashboard', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/get_user_activity_info', dashboard_views.get_user_activity_info, name='get_user_activity_info'),
    path('dashboard/get_user_storage', dashboard_views.get_user_storage, name='get_user_storage'),
    path('get_hardware_usage/', dashboard_views.get_hardware_usage, name='get_hardware_usage'),
    # 海洋资源管理
    path('infoSys', infosys_views.infoSys, name='infoSys'),
    path('infoSys/UserImages', infosys_views.infoSys_userImages, name='UserImages'),
    # 海洋视觉处理
    path('sea_eyes/', vision_views.sea_eyes, name='sea_eyes'),
    path('sea_eyes/upload_images', vision_views.uploadImages, name='upload_images'),
    path('sea_eyes/upload_videos', vision_views.uploadVideos, name='upload_videos'),
    path('sea_eyes/image_restruction', vision_views.imageRestruction, name='image_res'),
    # 海洋语言模型
    path('tongyi/', llms_views.tongyi_page, name='tongyi_page'),
    path('sea_llm/tongyi', llms_views.tongyi, name='tongyi')
]
