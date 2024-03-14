import datetime, psutil, json
import os.path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

"""
海洋图像处理模块
"""


def sea_eyes(request):  # 海洋之眼跳转链接
    return render(request, 'html/sea_eyes.html')



@login_required
def uploadImages(request):  # 海洋之眼上传页面
    return render(request, 'html/uploadImages.html')



# 上传视频检测页面，一次只能检测一个上传并检测一个视频
@login_required
def uploadVideos(request):
    return render(request, 'html/upload_videos.html')


def imageRestruction(request):
    return render(request, 'html/image_restruction.html')

