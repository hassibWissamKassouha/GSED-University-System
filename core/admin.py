from django.contrib import admin
from .models import (
    GlobalUser, Department, Student, Professor, Course, 
    Enrollment, Grade, ExamSession, ExamHallAllocation, 
    Thesis, Seminar, Decree, DocumentRequest, UserDecree
)

# ── 1. Inlines (لعرض الجداول المرتبطة داخل الموديل الأب) ─────────────────

class GradeInline(admin.StackedInline):
    model = Grade
    extra = 1

class ExamHallInline(admin.TabularInline):
    model = ExamHallAllocation
    extra = 1

class SeminarInline(admin.TabularInline):
    model = Seminar
    extra = 1

class UserDecreeInline(admin.TabularInline):
    model = UserDecree
    extra = 0

# ── 2. Model Admin Customization ────────────────────────────────────────

@admin.register(GlobalUser)
class GlobalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email_address', 'role', 'is_active', 'is_locked')
    list_filter = ('is_active', 'is_locked')
    search_fields = ('id', 'first_name', 'last_name', 'email_address')
    ordering = ('id',)
    inlines = [UserDecreeInline]
    
    # لعرض الـ role (Property) في القائمة
    def role(self, obj):
        return obj.role
    role.short_description = 'الصلاحية'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('university_id', 'user', 'department', 'student_status', 'enrollment_year')
    list_filter = ('student_status', 'department', 'enrollment_year')
    search_fields = ('university_id', 'user__first_name', 'user__last_name')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'academic_rank', 'department')
    list_filter = ('academic_rank', 'department')
    search_fields = ('user__first_name', 'user__last_name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'professor', 'department', 'credits')
    list_filter = ('department', 'credits')
    search_fields = ('course_code', 'course_name')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'status')
    list_filter = ('semester', 'status', 'course__department')
    inlines = [GradeInline] # رصد العلامات مباشرة من صفحة التسجيل

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_date', 'semester', 'duration')
    inlines = [ExamHallInline]

@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'supervisor', 'status', 'defense_date')
    list_filter = ('status',)
    inlines = [SeminarInline]

@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'request_type', 'request_status', 'request_date')
    list_filter = ('request_status', 'request_type')
    actions = ['mark_as_ready']

    def mark_as_ready(self, request, queryset):
        queryset.update(request_status='ready')
    mark_as_ready.short_description = "تغيير حالة الطلبات المحددة إلى 'جاهز'"

# ── 3. تسجيل الموديلات البسيطة ───────────────────────────────────────────

admin.site.register(Department)
admin.site.register(Decree)
admin.site.register(Grade) # مسجل أيضاً كـ Inline في Enrollment