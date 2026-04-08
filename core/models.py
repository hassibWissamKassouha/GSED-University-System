from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ─────────────────────────────────────────────
# User Manager
# ─────────────────────────────────────────────

class GlobalUserManager(BaseUserManager):
    def create_user(self, id, first_name, last_name, email_address, password=None, **extra_fields):
        if not id:
            raise ValueError('يجب إدخال الرقم المعرف (ID)')
        email_address = self.normalize_email(email_address)
        user = self.model(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, first_name, last_name, email_address, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(id, first_name, last_name, email_address, password, **extra_fields)


# ─────────────────────────────────────────────
# Department
# ─────────────────────────────────────────────

class Department(models.Model):
    department_name = models.CharField(max_length=100, db_column='department_name')
    faculty_name = models.CharField(max_length=100, db_column='faculty_name')

    def __str__(self):
        return self.department_name


# ─────────────────────────────────────────────
# Global User
# ─────────────────────────────────────────────

class GlobalUser(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True, unique=True, db_column='id')
    first_name = models.CharField(max_length=50, db_column='first_name')
    middle_name = models.CharField(max_length=50, blank=True, db_column='middle_name')
    last_name = models.CharField(max_length=50, db_column='last_name')
    email_address = models.EmailField(unique=True, db_column='email_address')
    is_active = models.BooleanField(default=True, db_column='is_active')
    is_staff = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False, db_column='is_locked')

    objects = GlobalUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email_address']

    # ── Computed properties ──────────────────

    @property
    def role(self):
        """Returns the user's role name from their Django group."""
        group = self.groups.first()
        return group.name if group else None

    @property
    def department(self):
        """Returns department from the user's profile (Student or Professor)."""
        if hasattr(self, 'student'):
            return self.student.department
        if hasattr(self, 'professor'):
            return self.professor.department
        return None

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.id})"


# ─────────────────────────────────────────────
# Student
# ─────────────────────────────────────────────

class Student(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
        ('withdrawn', 'Withdrawn'),
    ]

    user = models.OneToOneField(
        GlobalUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='student',
        db_column='user_id'
    )
    university_id = models.CharField(max_length=20, unique=True, db_column='university_id')
    enrollment_year = models.IntegerField(db_column='enrollment_year')
    student_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_column='student_status'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='students',
        db_column='department_id'
    )

    def __str__(self):
        return f"{self.user.full_name} ({self.university_id})"


# ─────────────────────────────────────────────
# Professor
# ─────────────────────────────────────────────

class Professor(models.Model):

    RANK_CHOICES = [
        ('assistant', 'Assistant Professor'),
        ('associate', 'Associate Professor'),
        ('full', 'Full Professor'),
        ('lecturer', 'Lecturer'),
    ]

    user = models.OneToOneField(
        GlobalUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='professor',
        db_column='user_id'
    )
    academic_rank = models.CharField(
        max_length=50,
        choices=RANK_CHOICES,
        db_column='academic_rank'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='professors',
        db_column='department_id'
    )

    def __str__(self):
        return f"{self.user.full_name} - {self.academic_rank}"


# ─────────────────────────────────────────────
# Course
# ─────────────────────────────────────────────

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True, db_column='course_code')
    course_name = models.CharField(max_length=100, db_column='course_name')
    credits = models.PositiveIntegerField(default=3, db_column='credits')
    professor = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        db_column='professor_id'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses',
        db_column='department_id'
    )

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


# ─────────────────────────────────────────────
# Enrollment
# ─────────────────────────────────────────────

class Enrollment(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments',
        db_column='student_id'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        db_column='course_id'
    )
    semester = models.CharField(max_length=20, db_column='semester')
    enrollment_date = models.DateField(auto_now_add=True, db_column='enrollment_date')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_column='status'
    )

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def __str__(self):
        return f"{self.student} → {self.course} ({self.semester})"


# ─────────────────────────────────────────────
# Grade
# ─────────────────────────────────────────────

class Grade(models.Model):
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='grade',
        db_column='enrollment_id'
    )
    practical_mark = models.FloatField(db_column='practical_mark')
    theoretical_mark = models.FloatField(db_column='theoretical_mark')
    is_validated = models.BooleanField(default=False, db_column='is_validated')
    is_locked = models.BooleanField(default=False, db_column='is_locked')

    @property
    def total(self):
        return self.practical_mark + self.theoretical_mark

    @property
    def letter_grade(self):
        t = self.total
        if t >= 90: return 'A+'
        if t >= 85: return 'A'
        if t >= 80: return 'B+'
        if t >= 75: return 'B'
        if t >= 70: return 'C+'
        if t >= 65: return 'C'
        if t >= 60: return 'D'
        return 'F'

    def __str__(self):
        return f"{self.enrollment} : {self.total} ({self.letter_grade})"


# ─────────────────────────────────────────────
# Exam Session
# ─────────────────────────────────────────────

class ExamSession(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='exam_sessions',
        db_column='course_id'
    )
    semester = models.CharField(max_length=20, db_column='semester')
    exam_date = models.DateField(db_column='exam_date')
    duration = models.IntegerField(db_column='duration')  # in minutes

    def __str__(self):
        return f"{self.course.course_name} - {self.exam_date}"


# ─────────────────────────────────────────────
# Exam Hall Allocation
# ─────────────────────────────────────────────

class ExamHallAllocation(models.Model):
    exam_session = models.ForeignKey(
        ExamSession,
        on_delete=models.CASCADE,
        related_name='halls',
        db_column='session_id'
    )
    hall_name = models.CharField(max_length=50, db_column='hall_name')
    capacity = models.PositiveIntegerField(db_column='capacity')  # removed nullable — a hall always has capacity

    def __str__(self):
        return f"{self.hall_name} → {self.exam_session}"


# ─────────────────────────────────────────────
# Thesis
# ─────────────────────────────────────────────

class Thesis(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('defended', 'Defended'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='theses',
        db_column='student_id'
    )
    title = models.CharField(max_length=255, db_column='title')  # increased from 50
    supervisor = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supervised_theses',
        db_column='supervisor_id'
    )
    start_date = models.DateField(db_column='start_date')
    defense_date = models.DateField(null=True, blank=True, db_column='defense_date')
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending',
        db_column='status'
    )

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# Seminar
# ─────────────────────────────────────────────

class Seminar(models.Model):
    thesis = models.ForeignKey(
        Thesis,
        on_delete=models.CASCADE,
        related_name='seminars',
        db_column='thesis_id'
    )
    seminar_date = models.DateField(db_column='seminar_date')
    report_summary = models.TextField(db_column='report_summary')
    attendance_status = models.BooleanField(default=False, db_column='attendance_status')

    def __str__(self):
        return f"Seminar: {self.thesis.title} ({self.seminar_date})"


# ─────────────────────────────────────────────
# Decree
# ─────────────────────────────────────────────

class Decree(models.Model):

    EFFECT_TYPE_CHOICES = [
        ('suspension', 'Suspension'),
        ('expulsion', 'Expulsion'),
        ('warning', 'Warning'),
        ('commendation', 'Commendation'),
        ('other', 'Other'),
    ]

    decree_number = models.CharField(max_length=50, unique=True, db_column='decree_number')
    description = models.CharField(max_length=255, db_column='description')
    effect_type = models.CharField(
        max_length=50,
        choices=EFFECT_TYPE_CHOICES,
        db_column='effect_type'
    )
    start_validity = models.DateField(db_column='start_validity')
    end_validity = models.DateField(db_column='end_validity')

    def __str__(self):
        return self.decree_number


# ─────────────────────────────────────────────
# Document Request
# ─────────────────────────────────────────────

class DocumentRequest(models.Model):

    REQUEST_TYPE_CHOICES = [
        ('transcript', 'Transcript'),
        ('enrollment_certificate', 'Enrollment Certificate'),
        ('graduation_certificate', 'Graduation Certificate'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='document_requests',
        db_column='student_id'
    )
    request_type = models.CharField(
        max_length=50,
        choices=REQUEST_TYPE_CHOICES,
        db_column='request_type'
    )
    request_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_column='request_status'
    )
    request_date = models.DateTimeField(auto_now_add=True, db_column='request_date')

    def __str__(self):
        return f"{self.student} - {self.request_type} ({self.request_status})"


# ─────────────────────────────────────────────
# User Decree
# ─────────────────────────────────────────────

class UserDecree(models.Model):
    user = models.ForeignKey(
        GlobalUser,
        on_delete=models.CASCADE,
        related_name='decrees',
        db_column='user_id'
    )
    decree = models.ForeignKey(
        Decree,
        on_delete=models.CASCADE,
        related_name='user_decrees',
        db_column='decree_id'
    )
    assignment_date = models.DateTimeField(auto_now_add=True, db_column='assignment_date')

    class Meta:
        unique_together = ('user', 'decree')

    def __str__(self):
        return f"قرار {self.decree.decree_number} للمستخدم {self.user.id}"