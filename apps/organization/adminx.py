from .models import CityDict, CourseOrg, Teacher
import xadmin

class CityDictAdmin(object):
    list_display = ['name', 'description', 'add_time']
    search_fields = ['name', 'description']
    list_filter = ['name', 'description', 'add_time']

class CourseOrgAdmin(object):
    list_display = ['name', 'description', 'click_nums', 'favors_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'description', 'click_nums', 'favors_nums', 'image', 'address', 'city']
    list_filter = ['name', 'description', 'click_nums', 'favors_nums', 'image', 'address', 'city', 'add_time']
    relfieild_style = 'fk-ajax'

class TeacherAdmin(object):
    list_display =  ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'favors_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'favors_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'favors_nums', 'add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)