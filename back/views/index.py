from django.shortcuts import render, redirect
from back.utils import extract_logs_from_file


def index(request):  # 主页面
    value = '欢迎来到基于深度学习的海洋生态环境检测平台'
    return render(request, 'html/index.html', {"value": value})

# 关于我们
def about_us(request):
    # 日志文件路径
    log_file_path = 'logs/user_activity.log'

    logs = extract_logs_from_file(log_file_path)
    for log in logs:
        print(log)

    return render(request, 'html/about_us.html')
