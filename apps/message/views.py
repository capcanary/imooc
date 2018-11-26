from django.shortcuts import render
from.models import UserMessage
from.import models
from django.http import HttpResponse


def getform(request):
    #1 变量保存法，分别创建数据表和字段的变量，把获取的request请求数据赋值给字段变量，然后把字段变量分别对应赋值给字段，然后保存
    name = request.POST.get('name', '')
    message = request.POST.get('message', '')
    address = request.POST.get('address', '')
    email = request.POST.get('email', '')
    user_message = UserMessage()
    user_message.name = name
    user_message.message = message
    user_message.address = address
    user_message.email = email
    user_message.save()

    #2 变量创建法 创建字段变量，把获取的request请求数据赋值给字段变量，然后把字段变量赋值到创建的数据表字段中
    # name = request.POST.get('name', '')
    # message = request.POST.get('message', '')
    # address = request.POST.get('address', '')
    # email = request.POST.get('email', '')
    # models.UserMessage.objects.create(name=name, message=message, address=address, email=email)

    # 删除数据
    # all_message = models.UserMessage.objects.filter(name='谢')
    # all_message.delete()
    return render(request, '留言板.html')

