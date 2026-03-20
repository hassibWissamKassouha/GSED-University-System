from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class GlobalUserManager(BaseUserManager):
    def create_user(self, id, firstName, lastName, emailAddress, password=None, **extra_fields):
        if not id:
            raise ValueError('يجب إدخال الرقم المعرف (ID)')
        emailAddress = self.normalize_email(emailAddress)
        user = self.model(id=id, firstName=firstName, lastName=lastName, emailAddress=emailAddress, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, firstName, lastName, emailAddress, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(id, firstName, lastName, emailAddress, password, **extra_fields)


class Role(models.Model):
    roleName = models.CharField(max_length=50, db_column='roleName')
    roleDescription = models.TextField(null=True, blank=True, db_column='roleDescription')

    def __str__(self):
        return self.roleName

class Permission(models.Model):
    permissionCode = models.CharField(max_length=50, db_column='permissionCode')
    permissionDescription = models.CharField(max_length=200, db_column='permissionDescription')

    def __str__(self):
        return self.permissionCode

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='roleID')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='permissionID')


class Department(models.Model):
    departmentName = models.CharField(max_length=100, db_column='departmentName')
    facultyName = models.CharField(max_length=100, db_column='facultyName')

    def __str__(self):
        return self.departmentName

class GlobalUser(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True, unique=True, db_column='id')
    firstName = models.CharField(max_length=50, db_column='firstName')
    middleName = models.CharField(max_length=50, blank=True, db_column='middleName')
    lastName = models.CharField(max_length=50, db_column='lastName')
    emailAddress = models.EmailField(unique=True, db_column='emailAddress')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, db_column='roleID')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, db_column='departmentID')
    isActive = models.BooleanField(default=True, db_column='isActive')
    is_staff = models.BooleanField(default=False)
    isLocked = models.BooleanField(default=False, db_column='isLocked')
    
    objects = GlobalUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'emailAddress']

class Student(models.Model):
    user = models.OneToOneField(GlobalUser, on_delete=models.CASCADE, primary_key=True, db_column='userID')
    universityId = models.CharField(max_length=20, unique=True, db_column='universityId')
    enrollmentYear = models.IntegerField(db_column='enrollmentYear')
    studentStatus = models.CharField(max_length=20, db_column='studentStatus')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='departmentID')

class Professor(models.Model):
    user = models.OneToOneField(GlobalUser, on_delete=models.CASCADE, primary_key=True, db_column='userID')
    academicRank = models.CharField(max_length=50, db_column='academicRank')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='departmentID')

class Course(models.Model):
    courseCode = models.CharField(max_length=10, db_column='courseCode')
    courseName = models.CharField(max_length=100, db_column='courseName')
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, db_column='professorID')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='departmentID')

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='studentID')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='courseID')
    practicalMark = models.FloatField(db_column='practicalMark')
    theoreticalMark = models.FloatField(db_column='theoreticalMark')
    isValidated = models.BooleanField(default=False, db_column='isValidated')
    isLocked = models.BooleanField(default=False, db_column='isLocked')

class ExamSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='courseID')
    semester = models.CharField(max_length=20, db_column='semester')
    examDate = models.DateField(db_column='examDate')
    duration = models.IntegerField(db_column='duration')

    def __str__(self):
        return f"{self.course.courseName} - {self.examDate}"

class ExamHallAllocation(models.Model):
    examSession = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='halls', db_column='sessionID')
    hallName = models.CharField(max_length=50, db_column='hallName')
    
    capacity = models.IntegerField(null=True, blank=True, db_column='capacity')

    def __str__(self):
        return f"{self.hallName} : {self.examSession.course.courseName}"

class Thesis(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='studentID')
    title = models.CharField(max_length=50, db_column='title')
    supervisor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, db_column='supervisorID')
    startDate = models.DateField(db_column='startDate')
    defenseDate = models.DateField(null=True, blank=True, db_column='defenseDate')
    status = models.CharField(max_length=50, db_column='status')

    def __str__(self):
        return f"{self.title}"

class Seminar(models.Model):
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE, db_column='thesisID')
    seminarDate = models.DateField(db_column='seminarDate')
    reportSummary = models.TextField(db_column='reportSummary')
    attendanceStatus = models.BooleanField(default=False, db_column='attendanceStatus')
    
    def __str__(self):
        return f"{self.thesis.title}"

class Decree(models.Model):
    decreeNumber = models.CharField(max_length=50, db_column='decreeNumber')
    description = models.CharField(max_length=255, db_column='description')
    effectType = models.CharField(max_length=50, db_column='effectType')
    startValidity = models.DateField(db_column='startValidity')
    endValidity = models.DateField(db_column='endValidity')

    def __str__(self):
        return f"{self.decreeNumber}"

class DocumentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='studentID')
    requestType = models.CharField(max_length=50, db_column='requestType')
    requestStatus = models.CharField(max_length=20, default='Pending', db_column='requestStatus')
    requestDate = models.DateTimeField(auto_now_add=True, db_column='requestDate')
    
class UserDecree(models.Model):
    user = models.ForeignKey(GlobalUser, on_delete=models.CASCADE, db_column='userID')
    decree = models.ForeignKey(Decree, on_delete=models.CASCADE, db_column='decreeID')
    assignmentDate = models.DateTimeField(auto_now_add=True, db_column='assignmentDate')

    class Meta:
        db_table = 'User_Decree'
        unique_together = ('user', 'decree')

    def __str__(self):
        return f"قرار {self.decree.decreeNumber} للمستخدم {self.user.id}"