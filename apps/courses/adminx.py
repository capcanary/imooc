from .models import Course, Lesson, Video, CourseResource
import xadmin


class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['name', 'description', 'detail', 'degree', 'learn_times', 'students', 'favor_numbers', 'image', 'click_numbers', 'add_time']
    search_fields = ['name', 'description', 'detail', 'degree', 'students', 'favor_numbers', 'image', 'click_numbers']
    list_filter = ['name', 'description', 'detail', 'degree', 'learn_times', 'students', 'favor_numbers', 'image', 'click_numbers', 'add_time']
    ordering = ['-click_numbers']
    readonly_fields = ['click_numbers']
    exclude = ['favor_numbers']
    inlines = [LessonInline, CourseResourceInline]


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)