from django.contrib import admin
from .models import (
    GlobalUser, Role, Permission, RolePermission, 
    Department, Student, Professor, Course, 
    Grade, ExamSession, ExamHallAllocation, 
    Thesis, Seminar, Decree, DocumentRequest, UserDecree
)

# 1. إدارة المستخدمين (عرض مخصص)
@admin.register(GlobalUser)
class GlobalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstName', 'lastName', 'emailAddress', 'role', 'is_staff', 'isLocked')
    search_fields = ('id', 'firstName', 'lastName', 'emailAddress')
    list_filter = ('is_staff', 'isActive', 'isLocked', 'role')

# 2. إدارة الطلاب (عرض مخصص)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'universityId', 'enrollmentYear', 'studentStatus', 'department')
    search_fields = ('universityId', 'user__id')

# 3. إدارة العلامات (عرض مخصص)
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'practicalMark', 'theoreticalMark', 'isValidated', 'isLocked')
    list_filter = ('isValidated', 'isLocked', 'course')

# 4. تسجيل بقية الجداول (12 جدولاً إضافياً)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)
admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(ExamSession)
admin.site.register(ExamHallAllocation)
admin.site.register(Thesis)
admin.site.register(Seminar)
admin.site.register(Decree)
admin.site.register(DocumentRequest)
admin.site.register(UserDecree)