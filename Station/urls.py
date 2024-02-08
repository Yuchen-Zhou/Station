from django.contrib import admin # 导入内置的Admin功能
from django.urls import path, re_path, include # 导入Django的路由函数模块

# 导入项目应用back
from back.views import index

# 配置媒体文件夹media
from django.views.static import serve
from django.conf import settings

# 代表整个项目的路由集合，以列表格式表示，每一个元素代表一条路由
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('back.urls')),
    # 配置媒体文件的路由地址
    re_path('media/(?P<path>.*)', serve,
            {'document_root': settings.MEDIA_ROOT}, name='media'),
]
