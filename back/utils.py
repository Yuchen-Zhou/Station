import os, time, json, sys, cv2, math
from Modules import  UserInfo
from YOLOv8.DetectModel import YOLOv8DetectModel
from moviepy.editor import VideoFileClip

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

