import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from back.utils import update_user_activity, set_user_session, update_storage, get_user_info, log_error
from django.contrib.auth.decorators import login_required
from back.models import CustomUser

logger_ = logging.getLogger('user_info')


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




def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        print(f"email: {email}, password: {password}")
        # 验证数据有效性
        if not (email and password):
            return JsonResponse({'error': '请填写完整的登录信息'})

        # 使用authenticate方法验证邮箱和密码是否匹配
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # 登录成功，使用login方法登录用户
            login(request, user)
            set_user_session(request)
            user_info = get_user_info(request)

            # 更新登录次数
            update_user_activity(email, action='login')
            return JsonResponse({'success': '登录成功', 'user_info': user_info})
        else:
            # 登录失败，返回错误信息
            log_error(email, action='登录')
            return JsonResponse({'error': '邮箱或密码错误'})
    return HttpResponse()

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

    return render(request, 'html/../templates/users/personal.html', {'User_info': User_info})

def check_login(request):
    if request.user.is_authenticated:
        # 用户已登录
        return JsonResponse({'isLoggedIn': True})
    else:
        # 用户未登录
        return JsonResponse({'isLoggedIn': False})
