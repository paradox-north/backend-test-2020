from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.serializers.json import json
from django import forms
from django.urls import reverse



def index(request):
    #获得所有的课程,课程名：教师
    if not request.session.get('is_login', None):
        message = '很抱歉，只有登陆后才能查看主页信息'
        return render(request, 'Choose_Courses/login.html', {'message': message})
    courses = Course.objects.all()
    output = {}
    for course in courses:
        output[course.name] = course.id
    return render(request, 'Choose_Courses/index.html', {'output':output})
    
        
def get_details(request, course_id):
    #查看course_id对应的课程详细信息
    course = get_object_or_404(Course, pk=course_id)
    output = {
            '课程名称': course.name,
            '授课教师': course.teacher,
            '课程内容': course.content,
        }
    return JsonResponse(output, json_dumps_params={'ensure_ascii': False})

'''以下为注册，登录，登出系统
未登录-->全部跳转login
已登录-->访问login自动跳转index，不允许访问register，需要先logout
登出-->自动跳转到login
'''

def register(request):
    #注册
    if request.method == "POST":
        #用户名，输入两次密码
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if username.strip():  #判断用户名是否为空,空格去除
            if password1 == password2:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已存在!'
                    return render(request, 'Choose_Courses/register.html', {'message': message})
                else:  #注册新用户
                    new_user = User()
                    new_user.name = username.strip()
                    new_user.password = password1
                    new_user.save()
                    message = '注册成功!'
                    return render(request, 'Choose_Courses/login.html', {'message': message})
            else:
                message = '两次密码不相同!'
                return render(request, 'Choose_Courses/register.html', {'message': message})
        else:
            message = '用户名未填写!'
            return render(request, 'Choose_Courses/register.html', {'message': message})
    return render(request,'Choose_Courses/register.html')

def login(request):
    #学生登录
    if request.session.get('is_login', None):  #不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            #用户名和密码合理性的其他验证
            try:
                user = User.objects.get(name=username)
            except:
                message = '用户名不存在，请重新输入用户名或注册新用户'
                return render(request, 'Choose_Courses/login.html', {'message': message})
            if user.password == password:       #如果成功登录了
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return render(request, 'Choose_Courses/index.html')
            else:
                message = '密码错误！'
                return render(request, 'Choose_Courses/login.html', {'message': message})
    return render(request,'Choose_Courses/login.html')

def logout(request):
    #登出
    if not request.session.get('is_login'): #如果没有登录
        return redirect('/index')  
    request.session.flush()  #删除会话
    return redirect('/index')

    