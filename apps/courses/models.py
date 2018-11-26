from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True, on_delete=None)
    name = models.CharField(max_length=50, verbose_name=u"课程名称")
    description = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    is_banner = models.BooleanField(default=False,verbose_name="是否轮播")
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    favor_numbers = models.IntegerField(default=0, verbose_name=u"收藏")
    image = models.ImageField(upload_to="courses/%y/%m", verbose_name=u"封面图", max_length=100)
    click_numbers = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    category = models.CharField(max_length=20, verbose_name=u"课程类别",default="后端开发")
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True, on_delete=models.CASCADE)
    youneed_know = models.CharField(max_length=300, verbose_name="课程须知", default="")
    teacher_tell = models.CharField(max_length=300, verbose_name="老师告诉你", default="")
    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取章节数
        return self.lesson_set.all().count()

    def get_lenarn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return u'%s' % (self.name)


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        #获取章节视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"视频名称")
    url = models.CharField(max_length=200, verbose_name="访问地址", default="")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
