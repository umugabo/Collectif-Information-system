from django.db import models
from django.contrib.auth.models import User


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

PHYSICAL_DISABILITY = [
     ("NO", "No"),
    ("Autism", "Autism"),
    ("Multiple", "Multiple"),
    ("Cerebral Palsy", "Cerebral Palsy"),
    ("Down syndrom", "Down syndrom"),
    
    # ("NO", "NO")
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
    physical_disability = models.CharField(max_length=15, choices=PHYSICAL_DISABILITY, default="NO")
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
    physical_disability = models.CharField(max_length=15, choices=PHYSICAL_DISABILITY, default="NO")
        
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
    physical_disability = models.CharField(max_length=15, choices=PHYSICAL_DISABILITY, default="NO")
    
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
    physical_disability = models.CharField(max_length=15, choices=PHYSICAL_DISABILITY, default="NO")
   
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
    physical_disability = models.CharField(max_length=15, choices=PHYSICAL_DISABILITY, default="NO")
   
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
    physical_disability = models.CharField(max_length=15, choices=PHYSICAL_DISABILITY, default="NO")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    familyNID = models.CharField(max_length=16, blank=False)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    phone =  models.CharField(max_length=10, blank=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    sectors = models.ForeignKey(Sectors, on_delete=models.CASCADE)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    note = models.CharField(max_length=150, blank=False)
  
    def __str__(self):
        return self.f_name  
