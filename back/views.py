import datetime, psutil, requests
import os.path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.conf import settings
from back.utils import *
from Modules import UserInfo, File, Folder


detect_dir = ''  # 上传缓冲区
video_dir = ''  # 视频保存缓冲区
logger_ = logging.getLogger('user_info')


"""
海洋信息综合管理
"""


# 设置用户session
def set_user_session(request):
    userinfo = CustomUser.objects.filter(email=request.user.email).first()

    # 用户已经使用百分比
    percentage = userinfo.already_use / (math.pow(1024, 3) * userinfo.storage) * 100
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


# 获取用户基本信息
def get_user_info(request):
    user_info_session = request.session.get('user_info')

    if user_info_session:
        User_info = generate_userInfo(user_info_session)

    return User_info


# 信息管理-图像管理
@login_required
def infoSys_userImages(request):
    set_user_session(request)
    User_info = get_user_info(request)
    update_user_activity(request.user.email, action='images_infosys')

    # 对上传的文件进行处理
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files[]')

        for uploaded_file in uploaded_files:

            user_path = os.path.join(settings.MEDIA_ROOT, User_info.UserEmail)  # 用户根路径
            dir_path = os.path.join(user_path, '海洋生物图像')
            file_path = os.path.join(dir_path, uploaded_file.name)
            print(file_path)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            user_file = UserFile(
                email=User_info.UserEmail,
                file_name=uploaded_file.name,
                file_type=uploaded_file.content_type,
                file_size=uploaded_file.size,
                upload_time=datetime.datetime.now(),
                folder_name='海洋生物图像',
            )
            user_file.save()
        return redirect('/infoSys')  # 重定向到当前页面，刷新文件列表

    files = []
    userfiles = UserFile.objects.filter(email=request.user.email, folder_name='海洋生物图像')

    for userfile in userfiles:
        if userfile.file_name == '海洋生物图像':
            continue
        size, signal = calculate_bytes(userfile.file_size)
        file = File(name=userfile.file_name, file_type=userfile.file_type,
                    size=size, signal=signal, upload_time=userfile.upload_time,
                    folder_name=userfile.folder_name)
        files.append(file)

    return render(request, 'html/infoSys_userImages.html', {'User_info': User_info, "files": files})


# 信息管理首页
@login_required
def infoSys(request):
    user = request.user
    email = user.email
    user_folder = os.path.join(settings.MEDIA_ROOT, str(user.email))  # 根据用户ID创建用户文件夹路径

    # print(f"邮箱为{email}的用户，登录了海洋信息综合管理系统")

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
            size, signal = calculate_bytes(userfile.file_size)
            folder = Folder(name=userfile.file_name, file_type='文件夹',
                            size=size, signal=signal, upload_time=userfile.upload_time)
            folders.append(folder)

    update_storage(request.user.email)
    set_user_session(request)
    User_info = get_user_info(request)

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

        # 验证数据有效性
        if not (username and email and password):
            return JsonResponse({'error': '请填写完整的注册信息'})

        # print(f'检查邮箱是否存在:{CustomUser.objects.filter(email=email).exists()}')
        # 检查邮箱是否已经存在
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': '该用户邮箱已被注册'})

        # 创建用户对象并保存到数据库
        try:
            with transaction.atomic():
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.save()

                login(request, user)
                set_user_session(request)
                update_user_activity(email, action='login')

                logger_.info(f"Username:{username}, UserEmail:{email}, UserPassword:{password}")
            return JsonResponse({'success': '注册成功，现在可以登录了'})
        except Exception as e:
            log_error(email, action="注册")
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
            set_user_session(request)

            # 更新登录次数
            update_user_activity(email, action='login')
            return JsonResponse({'success': '登录成功'})
        else:
            # 登录失败，返回错误信息
            log_error(email, action='登录')
            return JsonResponse({'error': '邮箱或密码错误'})
    # 如果不是POST请求，返回登录页面
    return render(request, 'html/login.html')


# 控制台页面
@login_required
def dashboard(request):
    current_user = request.user
    # 可以在这里使用current_user来获取当前登录用户的相关信息
    # 例如用户名、电子邮件地址等
    set_user_session(request)

    return render(request, 'html/dashboard.html',
                  {'current_user': current_user})

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


# 登出
def user_logout(request):
    update_user_activity(email=request.user.email, action='logout')
    logout(request)
    return redirect('index')


# 个人中心
@login_required
def personal(request):
    update_storage(request.user.email)
    set_user_session(request)
    User_info = get_user_info(request)

    return render(request, 'html/personal.html', {'User_info': User_info})


def index(request):  # 主页面
    value = '欢迎来到基于深度学习的多维度海洋生态监测平台'
    return render(request, 'html/index.html', {"value": value})

# 关于我们
def about_us(request):
    # 日志文件路径
    log_file_path = 'logs/user_activity.log'

    logs = extract_logs_from_file(log_file_path)
    for log in logs:
        print(log)

    return render(request, 'html/about_us.html')




"""
海洋图像处理模块
"""


def sea_eyes(request):  # 海洋之眼跳转链接
    return render(request, 'html/sea_eyes.html')



@login_required
def uploadImages(request):  # 海洋之眼上传页面
    return render(request, 'html/uploadImages.html')


# 显示检测结果
def detect_results(request):
    global detect_dir
    print(f'这是要检测的文件夹{detect_dir}')
    results = detect(detect_dir)
    return render(request, 'html/detect_results.html', {'detection_results': results})


# 上传视频检测页面，一次只能检测一个上传并检测一个视频
@login_required
def uploadVideos(request):
    return render(request, 'html/upload_videos.html')


def video_show(request):
    global video_dir
    print(f'video_dir = {video_dir}')
    return render(request, 'html/video_show.html', {'video_dir': video_dir})


"""
海洋大模型LLM部分
"""


def sea_llms(request):
    update_user_activity(request.user.email, action='llms')
    return render(request, 'html/llms.html')
