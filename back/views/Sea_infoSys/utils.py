import datetime
import os.path
from django.shortcuts import redirect
from django.conf import settings
from Modules import File
from back.utils import *


# 对上传的文件进行处理
def process_upload(request, User_info, folder_name):
    # 对上传的文件进行处理

    uploaded_files = request.FILES.getlist('files[]')

    for uploaded_file in uploaded_files:

        user_path = os.path.join(settings.MEDIA_ROOT, User_info.UserEmail)  # 用户根路径
        dir_path = os.path.join(user_path, folder_name)
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
            folder_name=folder_name,
        )
        user_file.save()


def list_dir(request, folder_name):
    files = []
    userfiles = UserFile.objects.filter(email=request.user.email, folder_name=folder_name)

    for userfile in userfiles:
        if userfile.file_name == folder_name:
            continue
        size, signal = calculate_bytes(userfile.file_size)
        file = File(name=userfile.file_name, file_type=userfile.file_type,
                    size=size, signal=signal, upload_time=userfile.upload_time,
                    folder_name=userfile.folder_name)
        files.append(file)

    return files
