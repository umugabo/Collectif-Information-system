from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.

GENDER = [
    ("M", "MALE"),
    ("F", "FEMALE"),
]

DEGREE = [
    ("Care Givers", "Care Givers"),
    ("A2 in Education", "A2 in Education"),
    ("A1 in Education", "A1 in Education"),
    ("Bachelor in Education", "Bachelor in Education"),
    ("Masters in Education", "Masters in Education"),
    ("PhD in Education", "PhD in Education"),
    
]

CLADES = [
    ("CLADE1", "CLADE 1"),
    ("CLADE2", "CLADE 2"),
    ("CLADE3", "CLADE 3"),
]

PHYSICAL_DISABILITY = [
     ("NO", "No"),
    ("Autism", "Autism"),
    ("Multiple", "Multiple"),
    ("Cerebral Palsy", "Cerebral Palsy"),
    ("Cerebral Palsy ID", "Cerebral Palsy ID"),
    ("Down syndrom", "Down syndrom"),
    
    # ("NO", "NO")
]
SERVICE_CATEGORY = [
    ("SPECIAL EDUCATION", "SPECIAL EDUCATION"),
    ("FUSION AND EDUCATION", "FUSION AND EDUCATION"), 
]


class Sector(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    sector_name = models.CharField(max_length=30)

    def __str__(self):
        return self.sector_name

class Province(models.Model):
    prov_name = models.CharField(max_length=30)

    def __str__(self):
        return self.prov_name

class School(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.school_name

class Classe(models.Model):
    class_name = models.CharField(max_length=30)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name

class Course(models.Model):
    course_name = models.CharField(max_length=30)
    course_desc = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE , null=True, blank=True)


    def __str__(self):
        return self.course_name



class Teacher(models.Model):
    TeacherNationalId = models.CharField(max_length=16, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=50, blank=False)
    degree = models.CharField(max_length=30, choices=DEGREE)
    recruit_year = models.IntegerField()
    physical_disability = models.CharField(max_length=50, choices=PHYSICAL_DISABILITY, default="NO")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.f_name 

class Parent(models.Model):
    represantativeNationalId = models.CharField(max_length=16, blank=False)
    father_fullName = models.CharField(max_length=100, blank=False)
    mother_fullName = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    district = models.CharField(max_length=30, blank=False)
    sector = models.CharField(max_length=30, blank=False)
    cell = models.CharField(max_length=30, blank=False)
    village = models.CharField(max_length=30, blank=False)
    physical_disability = models.CharField(max_length=50, choices=PHYSICAL_DISABILITY, default="NO")
        
    def __str__(self):
        return self.f_name  

class Coordinator(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    CoordinatorNationalId = models.CharField(max_length=16, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=50, blank=False)
    degree = models.CharField(max_length=30, choices=DEGREE)
    recruit_year = models.IntegerField()
    physical_disability = models.CharField(max_length=50, choices=PHYSICAL_DISABILITY, default="NO")
    # school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.f_name  

class Staff(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    StaffNationalId = models.CharField(max_length=16, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=50, blank=False)
    degree = models.CharField(max_length=30, choices=DEGREE)
    recruit_year = models.IntegerField()
    physical_disability = models.CharField(max_length=50, choices=PHYSICAL_DISABILITY, default="NO")
   
    def __str__(self):
        return self.f_name  
class Board(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    boardNationalId = models.CharField(max_length=16, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=50, blank=False)
    degree = models.CharField(max_length=30, choices=DEGREE)
    recruit_year = models.IntegerField()
    physical_disability = models.CharField(max_length=50, choices=PHYSICAL_DISABILITY, default="NO")
   
    def __str__(self):
        return self.f_name 

class Admin(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    adminNationalId = models.CharField(max_length=16, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=50, blank=False)
    degree = models.CharField(max_length=30, choices=DEGREE)

    def __str__(self):
        return self.f_name 




class District(models.Model):
    dist_name = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    def __str__(self):
        return self.dist_name

class Sectors(models.Model):
    sect_name = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    def __str__(self):
        return self.sect_name

class Cell(models.Model):
    cel_name = models.CharField(max_length=30)
    sectors = models.ForeignKey(Sectors, on_delete=models.CASCADE)
    def __str__(self):
        return self.cel_name

class Village(models.Model):
    vil_name = models.CharField(max_length=30)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    def __str__(self):
        return self.vil_name

class Student(models.Model):
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    dob = models.DateField()
    correspond_age = models.IntegerField()
    year_reg = models.IntegerField()
    physical_disability = models.CharField(max_length=50, choices=PHYSICAL_DISABILITY, default="NO")
    service_category = models.CharField(max_length=50, choices=SERVICE_CATEGORY)
    classe = models.CharField(max_length=50, choices=CLADES)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    familyNID = models.CharField(max_length=16, blank=False)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    phone =  models.CharField(max_length=10, blank=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    sectors = models.CharField(max_length=30, blank=False)
    cell = models.CharField(max_length=30, blank=False)
    village = models.CharField(max_length=30, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    st_image = models.ImageField(default="anonymous-user.png", null=True, blank=True)
    note = models.CharField(max_length=150, blank=False)
    def __str__(self):
        return self.f_name  

