from django.urls import path

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView

app_name='courses'
urlpatterns = [
    #课程列表页
    path('list/', CourseListView.as_view(), name="course_list"),

    #课程详情页
    path('detail/<course_id>', CourseDetailView.as_view(), name="course_detail"),
    path('info/<course_id>', CourseInfoView.as_view(), name="course_info"),

    #课程评论
    path('comment/<course_id>', CommentsView.as_view(), name="course_comments"),

    #添加课程评论
    path('add_comment/', AddCommentsView.as_view(), name="add_comments"),
]