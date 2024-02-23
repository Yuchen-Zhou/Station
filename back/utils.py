import os, time, json, sys, cv2, math, logging
from Modules import  UserInfo
from YOLOv8.DetectModel import YOLOv8DetectModel
from moviepy.editor import VideoFileClip
from .models import UserActivity, UserFile, CustomUser

logger = logging.getLogger('user_activity')

def log_error(email, action):
    logger.error(f"邮箱为{email} - {action} 操作出现错误")


# 更新次数
def update_user_activity(email, action):
    try:
        user_activity = UserActivity.objects.get(user_email=email)
    except UserActivity.DoesNotExist:
        # 如果用户活动记录不存在，则创建新记录
        user_activity = UserActivity.objects.create(user_email=email)

    # 根据操作更新相应的字段
    if action == 'login':
        user_activity.login_count += 1
        logger.info(f"邮箱为 {email} 登录成功")
    elif action == 'logout':
        user_activity.logout_count += 1
        logger.info(f"邮箱为 {email} 退出登录")
    elif action == 'image_detect':
        user_activity.image_detect_count += 1
        logger.info(f"邮箱为 {email} 进行了图片识别操作")
    elif action == 'view_detect':
        user_activity.view_detect_count += 1
        logger.info(f"邮箱为 {email} 进行了视频检测操作")
    elif action == 'image_restructure':
        user_activity.image_restructure_count += 1
        logger.info(f"邮箱为 {email} 进行了图像重构操作")
    elif action == 'llms':
        user_activity.llms_count += 1
        logger.info(f"邮箱为 {email} 使用了大模型")
    elif action == 'images_infosys':
        user_activity.images_infosys_count += 1
        logger.info(f"邮箱为 {email} 进行海洋综合管理-海洋图像管理操作")
    elif action == 'models_infosys':
        user_activity.models_count += 1
        logger.info(f"邮箱为 {email} 进行海洋综合管理-模型管理操作")
    elif action == 'research_infosys':
        user_activity.research_count += 1
        logger.info(f"邮箱为 {email} 进行海洋综合管理-文献管理操作")
    elif action == 'data_preprocess':
        user_activity.dataPreprocess_count += 1
        logger.info(f"邮箱为 {email} 使用了数据预处理")


    # 保存更新后的用户活动记录
    user_activity.save()


# 更新用户文件夹的大小
def update_folder_size(email, folder_name):
    user_files = UserFile.objects.filter(email=email, folder_name=folder_name)
    folder_size = 0
    folder = None
    for user_file in user_files:
        if user_file.file_name == user_file.folder_name:
            folder = user_file
        else:
            folder_size += user_file.file_size

    if folder:
        folder.file_size = folder_size
        folder.save()
        # print(f"文件夹{folder.folder_name}的大小已更新为{folder.file_size}字节")


# 更新用户存储空间
def update_storage(email):
    user_files = UserFile.objects.filter(email=email)

    user_info = CustomUser.objects.filter(email=email).first()
    # 对用户的各个文件夹进行更新
    for user_file in user_files:
        if user_file.file_name == user_file.folder_name:
            update_folder_size(email, user_file.folder_name)

    user_storage = 0
    user_files_ = UserFile.objects.filter(email=email)
    for user_file_ in user_files_:
        if user_file_.file_name == user_file_.folder_name:
            user_storage += user_file_.file_size

    if user_info:
        user_info.already_use = user_storage
        user_info.save()


# 根据session生成User信息
def generate_userInfo(user_info_session):
    User_info = UserInfo(user_info_session['userName'], user_info_session['userEmail'],
                         user_info_session['userStorage'], user_info_session['userUsed'],
                         user_info_session['userSignal'], user_info_session['userPercentage'])
    return User_info


# 计算已经使用的文件大小
def calculate_bytes(bytes):
    signal = 'B'
    if bytes >= 1024 and bytes < math.pow(1024, 2):
        signal = 'KB'
        bytes = bytes / 1024
    elif bytes >= math.pow(1024, 2) and bytes < math.pow(1024, 3):
        signal = 'MB'
        bytes = bytes / math.pow(1024, 2)
    elif bytes >= math.pow(1024, 3):
        signal = 'GB'
        bytes = bytes / math.pow(1024, 3)

    bytes = round(bytes, 2)
    return bytes, signal


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

def detect_video(video_path):
    model = YOLOv8DetectModel(mode='detect', img=video_path)
    results = model.detect_video()
    return results


def convert_avi_to_mp4(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

