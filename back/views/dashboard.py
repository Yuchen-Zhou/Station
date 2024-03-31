import psutil
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from back.utils import *


# 控制台页面
@login_required
def dashboard(request):
    if request.method == 'GET':
        user_info = get_user_info(request)
        print("收到请求")
        print(user_info)
        return JsonResponse(user_info)


# 获取用户存储信息
def get_user_storage(request):
    user_info = CustomUser.objects.filter(email=request.user.email).first()
    already_used = user_info.already_use

    used_gb = already_used / (1024 ** 3)
    total_storage_gb = 5
    user_storage = {
        'used': round(used_gb, 4),
        'unused': round(total_storage_gb - used_gb, 4),
        'total': total_storage_gb
    }

    return JsonResponse(user_storage)


# 获取用户的活动信息
def get_user_activity_info(request):
    user_data = UserActivity.objects.filter(user_email=request.user.email).first()

    user_activity_info = {
        "login_count": user_data.login_count,
        "sea_eyes_count": user_data.image_detect_count + user_data.view_detect_count + user_data.image_restructure_count,
        "llms_count": user_data.llms_count,
        "infoSys_count": user_data.images_infosys_count + user_data.research_count + user_data.models_count
    }
    return JsonResponse(user_activity_info)


def get_hardware_usage(request):
    cpu_usage = psutil.cpu_percent()  # 获取cpu使用率
    memory_info = psutil.virtual_memory()  # 获取内存情况
    total_memory = memory_info.total
    used_memory = memory_info.used
    free_memory = memory_info.free

    data = {
        "cpu_percent": cpu_usage,
        'total_memory': total_memory,
        'used_memory': used_memory,
        'free_memory': free_memory,
    }

    return JsonResponse(data)
