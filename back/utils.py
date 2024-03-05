import os, time,  math, logging, re
from YOLOv8.DetectModel import YOLOv8DetectModel
from moviepy.editor import VideoFileClip
from .models import UserActivity, UserFile, CustomUser
from Modules import UserInfo
from faker import Faker
import random
from tqdm import trange


logger = logging.getLogger('user_activity')



# 创建日期文件夹
def create_upload_folder(base_folder):
    """
    创建一个专属文件夹，命名规范为当前年月日加上上传次数后缀。

    Args:
        base_folder (str): 基础文件夹路径。

    Returns:
        str: 创建的文件夹路径。
    """
    dir_name = time.strftime('%Y-%m-%d', time.localtime())
    upload_folder = os.path.join(base_folder, dir_name)

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        return upload_folder

    counter = 1
    while True:
        new_upload_folder = f'{upload_folder}_{counter}/'
        if not os.path.exists(new_upload_folder):
            os.makedirs(new_upload_folder)
            return new_upload_folder
        else:
            counter += 1


# 分析日志数据
def extract_logs_from_file(file_path):
    logs = []
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - INFO - 邮箱为 (\S+) 进行(.*)操作'
    with open(file_path, 'r') as file:
        for line in file:
            matches = re.findall(pattern, line)
            for match in matches:
                log = {
                    'time': match[0],
                    'user': match[1],
                    'operation': match[2]
                }
                logs.append(log)
    return logs


# 模拟日志数据
def simulate(num_users=10000, max_actions_per_user=20):
    # 创建一个Faker对象
    fake = Faker()

    # 定义模拟的用户行为列表
    actions = ['login', 'logout', 'image_detect', 'view_detect', 'image_restructure', 'llms',
               'images_infosys', 'models_infosys', 'research_infosys']

    # 模拟生成指定数量的用户数据
    for _ in trange(num_users, desc="Generating User Activities"):
        email = fake.email()  # 生成随机的邮箱地址

        # 生成随机行为次数
        num_actions = random.randint(1, max_actions_per_user)

        # 为每个用户生成随机次数的随机行为
        for _ in range(num_actions):
            # 随机选择一个数字作为行为的索引
            action_index = random.randint(0, len(actions) - 1)
            action = actions[action_index]  # 获取对应的行为
            update_user_activity(email, action)  # 调用更新用户行为的函数


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
        logger.info(f"邮箱为 {email} 图片识别")
    elif action == 'view_detect':
        user_activity.view_detect_count += 1
        logger.info(f"邮箱为 {email} 视频检测")
    elif action == 'image_restructure':
        user_activity.image_restructure_count += 1
        logger.info(f"邮箱为 {email} 图像重构")
    elif action == 'llms':
        user_activity.llms_count += 1
        logger.info(f"邮箱为 {email} 海洋语言模型")
    elif action == 'images_infosys':
        user_activity.images_infosys_count += 1
        logger.info(f"邮箱为 {email} 海洋资源管理-海洋图像管理")
    elif action == 'models_infosys':
        user_activity.models_count += 1
        logger.info(f"邮箱为 {email} 海洋资源管理-模型管理")
    elif action == 'research_infosys':
        user_activity.research_count += 1
        logger.info(f"邮箱为 {email} 海洋资源管理-生态研究")


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


def detect_video(video_path):
    model = YOLOv8DetectModel(mode='detect', img=video_path)
    results = model.detect_video()
    return results


def convert_avi_to_mp4(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')


from datetime import datetime

