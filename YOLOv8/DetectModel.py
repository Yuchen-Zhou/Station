from ultralytics import YOLO
from PIL import Image
from django.conf import settings
import os, shutil



# 定义YOLOv8海洋生物检测模型
class YOLOv8DetectModel:
    def __init__(self, mode, img):  # 初始化参数必须给入模式(mode)、图片地址(img)
        self.mode = mode
        self.img = img
        self.model = YOLO('/root/autodl-tmp/runs/detect/train3/weights/best.pt')  # 初始化模型

    def detect(self):  # 图片检测函数
        if self.mode == 'detect':
            results = self.model.predict(source=self.img, save=True, save_txt=True)  # 对图片进行检测
            imageResults = []


            for result in results:
                names = result.names
                save_dir = result.save_dir
                for f in os.listdir(save_dir + '/labels'):
                    file_path = os.path.join(save_dir + '/labels', f)
                with open(file_path, 'r') as file:
                    specis = file.read().split(' ')[0]


                file_name = result.path.split('/')[-1]  # 图片名
                file_path = os.path.join(save_dir, file_name)
                shutil.copy(file_path, os.path.join(settings.MEDIA_ROOT, file_name)) # 将图片复制到media下
                kinds = []
                kind = names.get(int(specis))  # 检测到的生物
                kinds.append(kind)
                imageResult = ImageResult(file_name, kinds, save_dir)
                imageResults.append(imageResult)
            return imageResults

    def detect_video(self):
        results = self.model.predict(source=self.img, stream=True, save=True)
        return results


# 图片检测结果类
class ImageResult:
    def __init__(self, image, species, save_dir):
        self.image = image      # 图片名
        self.species = species   # 生物种类
        self.save_dir = save_dir    # 保存路径
        self.image_path = os.path.join(self.save_dir, self.image)
        self.numbers = len(species)     # 生物数量

    def show(self):
        print(f'图片名是{self.image}\n生物种类有{self.species}\n'
              f'文件保存在{self.image_path}\n生物数量有{self.numbers}只')
        print(f'文件的绝对路径为{os.path.abspath(self.save_dir)}')





