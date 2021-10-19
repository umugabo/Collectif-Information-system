from django.forms import ModelForm
from .models import Classe,Student,Course ,Teacher ,School , Coordinator, Province, District, Sectors, Cell, Village
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import date
import datetime
from django import forms



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'course_desc')
        labels = {
            'course_name':'Course Name',
            'course_desc':'Course Description'
        }

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ('class_name','school')
        labels = {
            'class_name':'Class Name',
            'school':'school',
        }
class DateInput(forms.DateInput):
    input_type = 'date'

class StudentForm(forms.ModelForm):
    dob =forms.DateField(widget=DateInput)
    class Meta:
        model = Student
        fields = ('f_name','l_name','gender','dob','correspond_age','year_reg','physical_disability','classe','school','familyNID','father_name','mother_name','phone','province','district','sectors','cell','village','note')
        labels = {
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'dob':'Date of Birth',
            'correspond_age':'Mental corresponding age',
            'year_reg':'Registration Year',
            'physical_disability':'Disability Type',
            'classe':'Class Name',
            'school':'School Name',
            'familyNID':'Family NationalId',
            'father_name':'Father Name',
            'mother_name':'Mother Name',
            'phone':'Family Phone Number',
            'province':'Province',
            'district':'District',
            'sectors':'Sector',
            'cell':'Cell',
            'village':'Village',
            'note':'Observation Note'

            
        }
    def __init__(self,*args,**kwargs):
        super(StudentForm,self).__init__(*args,**kwargs)
        self.fields['classe'].empty_label = "Select Class"
        self.fields['gender'].empty_label = "Select Gender"


class TeacherForm(forms.ModelForm):
    
    class Meta:
        model = Teacher
        fields = ('TeacherNationalId','f_name','l_name','gender','degree','recruit_year','phone','email','physical_disability','course','school')
        labels = {
            'TeacherNationalId':'National Identification',
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'degree':'Level Of Education',
            'recruit_year':'Recruitment Year',
            'phone':'phone',
            'email':'email',         
            'physical_disability':'Physical Disability?',
            'course':'Course the teacher teachs in Class', 
            'school':'In which school will teachs in'
            
        }
    def __init__(self,*args,**kwargs):
        super(TeacherForm,self).__init__(*args,**kwargs)
        self.fields['gender'].empty_label = "Select Gender"
        self.fields['degree'].empty_label = "Select Degree"


class CoordinatorForm(forms.ModelForm):
    
    class Meta:
        model = Coordinator
        fields = ('CoordinatorNationalId','f_name','l_name','gender','degree','recruit_year','phone','email')
        labels = {
            'CoordinatorNationalId':'National Identification',
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'degree':'Level Of Education',
            'recruit_year':'Recruitment Year',
            'phone':'phone',
            'email':'email',         
            
            
        }
    def __init__(self,*args,**kwargs):
        super(CoordinatorForm,self).__init__(*args,**kwargs)
        self.fields['gender'].empty_label = "Select Gender"
        self.fields['degree'].empty_label = "Select Degree"

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ('school_name','province','user')
        labels = {
            'school_name':'School Name',
            'province_name':'province',
            'user':'School_Coordinator',
        }


