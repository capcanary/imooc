import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_file.html')
        return render(request, 'login.html')


#注册流程
# 1.定义一个注册类，继承View。
# 2.然后分别定义一个GET和POST函数，分别实例化Form
# 3.如果是get请求就返回注册页面
# 4.如果是Post请求，取出用户的账号密码，然后


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        # 实例化form，验证每个字段是否合法
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 取出email和password
            username = request.POST.get("email")
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {"register_form": register_form, "msg": "老哥，你已经注册过了，可以直接登陆了"})
            password = request.POST.get("password")
            # 实例化用户，然后赋值
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册imooc"
            user_message.save()

            send_register_email(username, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})


class LogoutView(View):
    #用户登出
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # authenticate返回一个user,如果user存在，即not none，则通过验证
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, 'login.html', {"msg": "用户未激活"})
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_file.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    #修改用户密码
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if password1 != password2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    #用户个人信息
    def get(self, request):
        UserInfo='UserInfo'
        return render(request, "usercenter-info.html", {
        "UserInfo":UserInfo
        })


class UploadImageView(LoginRequiredMixin, View):
    #用户修改头像
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail'}", content_type='application/json')


class UpdatePwdView(View):
    #个人用户中心修改密码
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return HttpResponse("{'status':'fail','msg':'密码不一致'}", content_type='application/json')
            user = request.user
            user.password = make_password(password2)
            user.save()
            return HttpResponse("{'status':'success','msg':'密码修改成功'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailView(LoginRequiredMixin, View):
    #发送邮箱验证码
    def get(self, request):
        email = request.GET.get('email')

        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email':'邮箱已经存在'}", content_type='application/json')




class MyCourseView(LoginRequiredMixin, View):
    #我的课程
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses":user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    #我收藏的机构
    def get(self, request):
        org_list=[]
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list":org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    #我收藏的授课讲师
    def get(self, request):
        teacher_list=[]
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    # 我收藏的课程
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list
        })


class MyMessageView(LoginRequiredMixin, View):
    # 我的消息
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=int(request.user.id))

        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, request=request, per_page=10)

        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            'messages':messages
        })


class IndexView(View):
    #首页
    def get(self, request):
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "all_banners":all_banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs
        })


