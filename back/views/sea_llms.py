import json
from django.shortcuts import render
from django.http import JsonResponse
from back.utils import *


"""
海洋大模型LLM部分
"""


def tongyi_page(request):
    update_user_activity(request.user.email, action='llms')
    return render(request, 'html/../templates/llms/tongyi_page.html')




def tongyi(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get('user_input')
        # 在这里处理用户输入并生成 AI 的回答
        ai_response = call_with_prompt(user_input)

        return JsonResponse({'result': ai_response['text']})
