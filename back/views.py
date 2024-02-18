import os, time, json, sys, cv2, math
from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.db import transaction
from django.conf import settings

from .models import CustomUser, UserFile  # 导入自定义用户模型
from back.utils import *
from Modules import UserInfo, File, Folder

detect_dir = ''  # 上传缓冲区
video_dir = ''  # 视频保存缓冲区

"""
海洋信息综合管理
"""


# 信息管理-图像管理
@login_required
def infoSys_userImages(request):
    user_info_seesion = request.session.get('user_info')

    if user_info_seesion:
        User_info = generate_userInfo(user_info_seesion)

    # 对上传的文件进行处理
    if request.method == 'POST':
        uploaded_files = request.FILES.get('files')
        for uploaded_file in uploaded_files:
            user_path = os.path.join(settings.MEDIA_ROOT, User_info.UserEmail)  # 用户根路径
            file_path = os.path.join(user_path, '海洋生物图像')
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            user_file = UserFile(
                email=User_info.UserEmail,
                file_name=uploaded_file.name,
                file_type=uploaded_file.content_type,
                file_size=uploaded_file.size,
                upload_time=timezone.now(),
                folder_name='海洋生物图像',
            )
            user_file.save()
            return redirect('infoSys_userImages')  # 重定向到当前页面，刷新文件列表

    files = []
    userfiles = UserFile.objects.filter(email=request.user.email, folder_name='海洋生物图像')
    for userfile in userfiles:
        file = File(name=userfile.file_name, file_type=userfile.file_type,
                    size=userfile.file_size, upload_time=userfile.upload_time)
        files.append(file)

    return render(request, 'html/infoSys_userImages.html', {'User_info': User_info})


# 信息管理首页
@login_required
def infoSys(request):
    user = request.user
    email = user.email
    user_folder = os.path.join(settings.MEDIA_ROOT, str(user.email))  # 根据用户ID创建用户文件夹路径

    print(f"邮箱为{email}的用户，登录了海洋信息综合管理系统")

    # 如果用户文件夹不存在，将创建创建用户文件夹以及海洋生物图像文件夹、海洋生态研究文献文件夹、目标检测模型文件夹
    user_folder = os.path.join(settings.MEDIA_ROOT, str(user.email))  # 根据用户ID创建用户文件夹路径
    image_folder = os.path.join(user_folder, '海洋生物图像')  # 在用户根目录下创建生物图像文件夹
    literature_folder = os.path.join(user_folder, '海洋生态研究')  # 在用户根目录下创建海洋生态研究文件夹
    object_model_folder = os.path.join(user_folder, '目标检测模型')  # 在用户根目录下创建目标检测模型文件夹

    def createFolder(folders):
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            folder_name = os.path.basename(folder)
            UserFile.objects.create(email=email, file_name=folder_name,
                                    file_type='Folder', file_size=0,
                                    folder_name=folder_name)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        createFolder([image_folder, literature_folder, object_model_folder])

    folders = []
    # 读取数据库用户文件表
    userfiles = UserFile.objects.filter(email=email)
    for userfile in userfiles:
        if userfile.file_name == userfile.folder_name:  # 判断是否为文件夹
            folder = Folder(name=userfile.file_name, file_type='文件夹',
                            size=userfile.file_size, upload_time=userfile.upload_time)
            folders.append(folder)

    userinfo = CustomUser.objects.filter(email=email).first()

    # 用户已经使用百分比
    percentage = userinfo.already_use / 1024 * 1024 * 1024 * userinfo.storage
    used, signal = calculate_bytes(userinfo.already_use)

    User_info = UserInfo(userinfo.username, userinfo.email, userinfo.storage, used, signal, percentage)

    request.session['user_info'] = {
        'userName': User_info.UserName,
        'userEmail': User_info.UserEmail,
        'userStorage': User_info.UserStorage,
        'userUsed': User_info.UserUsed,
        'userSignal': User_info.UserUsedSignal,
        'userPercentage': User_info.UserPercentage
    }

    print(
        f"这是基本的用户信息,邮箱{User_info.UserEmail},用户名{User_info.UserName}\n"
        f"存储空间{User_info.UserStorage}GB,已经使用{User_info.UserUsed}{User_info.UserUsedSignal}\n")

    return render(request, 'html/infoSys.html', {"folders": folders, "User_info": User_info})


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


def video_show(request):
    global video_dir
    print(f'video_dir = {video_dir}')
    return render(request, 'html/video_show.html', {'video_dir': video_dir})


"""
海洋大模型LLM部分
"""


def sea_llms(request):
    return render(request, 'html/llms.html')
