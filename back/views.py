import os, time, json, sys, cv2
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.conf import settings

from .models import CustomUser, UserFile  # 导入自定义用户模型
from YOLOv8.DetectModel import YOLOv8DetectModel
from moviepy.editor import VideoFileClip

detect_dir = ''  # 上传缓冲区
video_dir = ''  # 视频保存缓冲区

"""
海洋信息综合管理
"""


@login_required
def infoSys(request):
    user = request.user
    email = user.email
    user_folder = os.path.join(settings.MEDIA_ROOT, str(user.email))  # 根据用户ID创建用户文件夹路径

    # 如果用户文件夹不存在，将创建创建用户文件夹以及海洋生物图像文件夹、海洋生态研究文献文件夹、目标检测模型文件夹、生态数据文件夹
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)  # 如果用户文件夹不存在，创建用户文件夹


    return render(request, 'html/infoSys.html')


"""
用户注册登录模块
"""


def user_register(request):
    if request.method == 'POST':
        # 接收前端发送的数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"username: {username}\n"
              f"email: {email}\n"
              f"password: {password}")
        # 验证数据有效性
        if not (username and email and password):
            return JsonResponse({'error': '请填写完整的注册信息'})

        print(f'检查邮箱是否存在:{CustomUser.objects.filter(email=email).exists()}')
        # 检查邮箱是否已经存在
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': '该用户邮箱已被注册'})

        # 创建用户对象并保存到数据库
        try:
            with transaction.atomic():
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
            return JsonResponse({'success': '注册成功，现在可以登录了'})
        except Exception as e:
            return JsonResponse({'error': f'注册失败：{str(e)}'})

    # 如果不是POST请求，返回登录页面
    return render(request, 'html/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 验证数据有效性
        if not (email and password):
            return JsonResponse({'error': '请填写完整的登录信息'})

        # 使用authenticate方法验证邮箱和密码是否匹配
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # 登录成功，使用login方法登录用户
            login(request, user)

            return JsonResponse({'success': '登录成功'})
        else:
            # 登录失败，返回错误信息
            return JsonResponse({'error': '邮箱或密码错误'})
    # 如果不是POST请求，返回登录页面
    return render(request, 'html/login.html')


# 控制台页面
@login_required
def dashboard(request):
    current_user = request.user
    # 可以在这里使用current_user来获取当前登录用户的相关信息
    # 例如用户名、电子邮件地址等
    print(f'这是当前登录的用户:{current_user.username}')
    return render(request, 'html/dashboard.html', {'current_user': current_user})


# 登出
def user_logout(request):
    logout(request)
    print(f"{request.user}登出")
    return redirect('index')


# 个人中心
def personal(request):
    return render(request, 'html/personal.html')


def index(request):  # 主页面
    value = '欢迎来到基于深度学习的多维度海洋生态监测平台'
    return render(request, 'html/index.html', {"value": value})


"""
海洋图像处理模块
"""


def sea_eyes(request):  # 海洋之眼跳转链接
    return render(request, 'html/sea_eyes.html')


def uploadImages(request):  # 海洋之眼上传页面
    if request.method == 'POST':
        # 获取上传文件
        uploaded_images = request.FILES.getlist('images')

        # 为每一次上传创建一个专属文件夹
        # 文件夹命名规范当前年月日➕第几次上传
        dir_name = time.strftime('%Y-%m-%d', time.localtime())
        upload_folder = './back/upload/images/' + dir_name

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            writeImages(uploaded_images, upload_folder)
            global detect_dir
            detect_dir = upload_folder
        else:
            counter = 1
            while True:
                new_upload_folder = f'{upload_folder}_{counter}/'
                if not os.path.exists(new_upload_folder):
                    break
                else:
                    counter += 1
                    new_upload_folder = f'{upload_folder}_{counter}/'  # 更新后缀数字
            print(new_upload_folder)
            os.makedirs(new_upload_folder)

            writeImages(uploaded_images, new_upload_folder)

            detect_dir = new_upload_folder
            # detect(detect_dir)  # 检测

        msg = "上传成功,点击查看检测结果"
        return render(request, 'html/uploadImages.html', {'msg': msg})

    return render(request, 'html/uploadImages.html')


# 将上传的图片保存至本地文件夹
def writeImages(uploaded_images, upload_folder):
    for uploaded_image in uploaded_images:
        image_path = os.path.join(upload_folder, str(uploaded_image))
        with open(image_path, 'wb') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)


# 对缓冲区文件夹内的图片进行目标检测任务
def detect(imagefolder):
    dir_path = '/root/autodl-tmp/Station/YOLOv8/'
    mode = 'detect'
    print(imagefolder)
    model = YOLOv8DetectModel(mode, imagefolder)
    results = model.detect()
    print(results)
    for result in results:
        result.show()
    return results
    # return redirect('sea_eyes/upload_images/detect_results', results)
    #     return render(request, 'html/uploadImages.html', {'detection_results': results})


# 显示检测结果
def detect_results(request):
    global detect_dir
    print(f'这是要检测的文件夹{detect_dir}')
    results = detect(detect_dir)
    return render(request, 'html/detect_results.html', {'detection_results': results})


# 上传视频检测页面，一次只能检测一个上传并检测一个视频
def uploadVideos(request):
    if request.method == 'POST':
        uploaded_video = request.FILES.get('video')  # 只获取一个视频
        upload_folder = './back/upload/videos/'

        print(str(uploaded_video))
        video_path = os.path.join(upload_folder, str(uploaded_video))
        print(video_path)

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        with open(video_path, 'wb') as destination:
            for chunk in uploaded_video.chunks():
                destination.write(chunk)

        # results = detect_video(video_path)
        # for result in results:
        #     save_dir = result.save_dir
        #     result_json = result.tojson()
        #
        # filename, extension = os.path.splitext(str(uploaded_video))
        # result_video = '/root/autodl-tmp/Station/' + save_dir + '/' + filename + '.avi'
        #
        # global video_dir
        # video_dir = '/root/autodl-tmp/Station/media/videos/' + filename + '.mp4'
        # convert_avi_to_mp4(result_video, video_dir)
        # print(f'这是要保存的路径{video_dir}')
        #
        # msg = '上传成功'

    return render(request, 'html/upload_videos.html')


def detect_video(video_path):
    model = YOLOv8DetectModel(mode='detect', img=video_path)
    results = model.detect_video()
    return results


def convert_avi_to_mp4(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')


def video_show(request):
    global video_dir
    print(f'video_dir = {video_dir}')
    return render(request, 'html/video_show.html', {'video_dir': video_dir})


"""
海洋大模型LLM部分
"""


def sea_llms(request):
    return render(request, 'html/llms.html')
