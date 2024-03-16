import datetime
import os.path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from back.utils import *
from Modules import File, Folder




# 资源管理-生态数据

# 资源管理-模型管理
@login_required
def infoSys_modelManage(request):
    User_info = get_user_info(request)
    update_user_activity(request.user.email, action='models_infosys')

    # TODO 对上传的模型进行处理

    files = []
    userfiles = UserFile.objects.filter(email=request.user.email, folder_name='目标检测模型')

    for userfile in userfiles:
        if userfile.file_name == '目标检测模型':
            continue
        size, signal = calculate_bytes(userfile.file_size)
        file = File(name=userfile.file_name, file_type=userfile.file_type,
                    size=size, signal=signal, upload_time=userfile.upload_time,
                    folder_name=userfile.folder_name)
        files.append(file)

    return render(request, 'sea_infoSys/infoSys_modelManage.html', {'User_info': User_info, "files": files})




# 资源管理-图像管理
@login_required
def infoSys_userImages(request):
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

    return render(request, 'sea_infoSys/infoSys_userImages.html', {'User_info': User_info, "files": files})


# 资源管理首页
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

    return render(request, 'sea_infoSys/infoSys.html', {"folders": folders, "User_info": User_info})
