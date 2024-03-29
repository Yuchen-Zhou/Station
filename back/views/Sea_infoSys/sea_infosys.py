import os.path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from back.utils import *
from Modules import File, Folder
from .utils import process_upload, list_dir



# 资源管理-生态数据

# 资源管理-模型管理
@login_required
def infoSys_modelManage(request):
    FOLDER_NAME = '目标检测模型'
    User_info = get_user_info(request)
    update_user_activity(request.user.email, action='models_infosys')

    # 对上传的模型进行处理
    if request.method == 'POST':
        process_upload(request, User_info, FOLDER_NAME)
        update_storage(request.user.email)  # 更新用户存储空间
        return redirect('/infoSys/UserModel')  # 重定向到当前页面，刷新文件列表


    files = list_dir(request, folder_name=FOLDER_NAME)

    return render(request, 'sea_infoSys/infoSys_modelManage.html',
                  {'User_info': User_info, "files": files})




# 资源管理-图像管理
@login_required
def infoSys_userImages(request):
    FOLDER_NAME = '海洋生物图像'
    User_info = get_user_info(request)
    update_user_activity(request.user.email, action='images_infosys')

    # 对上传的文件进行处理
    if request.method == 'POST':
        process_upload(request, User_info, FOLDER_NAME)
        update_storage(request.user.email)  # 更新用户存储空间
        return redirect('/infoSys/UserImages')  # 重定向到当前页面，刷新文件列表



    return render(request, 'sea_infoSys/infoSys_userImages.html',
                  {'User_info': User_info, "files": list_dir(request, folder_name=FOLDER_NAME)})


# 资源管理首页
@login_required
def infoSys(request):
    user = request.user
    email = user.email

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

    update_storage(request.user.email) # 更新用户存储空间
    set_user_session(request) # 配置用户Session

    return render(request, 'sea_infoSys/infoSys.html',
                  {"folders": folders, "User_info": get_user_info(request)})
