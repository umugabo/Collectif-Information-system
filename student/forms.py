from django.forms import ModelForm
from .models import Membership, Year,Budget, Staff,Classe,Student,Course ,Teacher ,School , Coordinator, Province, District, Sectors, Cell, Village
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import date
import datetime
from django import forms



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'course_desc','school')
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
        fields = ('f_name','l_name','gender','dob','correspond_age','year_reg','course','physical_disability','classe','familyNID','father_name','mother_name','phone','province','district','sectors','cell','village','note', 'service_category', 'st_image')
        labels = {
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'dob':'Date of Birth',
            'correspond_age':'Mental corresponding age',
            'year_reg':'Registration Year',
            'physical_disability':'Disability Type',
            'classe':'Class Name',
            'course':'Course To Take',
            'familyNID':'Family NationalId',
            'father_name':'Father Name',
            'mother_name':'Mother Name',
            'phone':'Family Phone Number',
            'province':'Province',
            'district':'District',
            'sectors':'Sector',
            'cell':'Cell',
            'village':'Village',
            'note':'Observation Note',
            'service_category':'Service Category',
            'st_image':'Image',         
        }
    def __init__(self,*args,**kwargs):
        super(StudentForm,self).__init__(*args,**kwargs)
        self.fields['classe'].empty_label = "Select Class"
        self.fields['gender'].empty_label = "Select Gender"


class TeacherForm(forms.ModelForm):
    
    class Meta:
        model = Teacher
        fields = ('TeacherNationalId','f_name','l_name','gender','degree','recruit_year','phone','email','physical_disability','service')
        labels = {
            'TeacherNationalId':'National Identification',
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'degree':'Level Of Education',
            'recruit_year':'Recruitment Year',
            'phone':'phone',
            'email':'email',         
            'physical_disability':'Disability?',
            'service':'Service to provide', 
        }
    def __init__(self,*args,**kwargs):
        super(TeacherForm,self).__init__(*args,**kwargs)
        self.fields['gender'].empty_label = "Select Gender"
        self.fields['degree'].empty_label = "Select Degree"


class CoordinatorForm(forms.ModelForm):
    
    class Meta:
        model = Coordinator
        fields = ('CoordinatorNationalId','f_name','l_name','gender','degree','recruit_year','phone','email', 'user')
        labels = {
            'CoordinatorNationalId':'National Identification',
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'degree':'Level Of Education',
            'recruit_year':'Recruitment Year',
            'phone':'phone',
            'email':'email', 
            'user':'Select User',
            # 'school':'School'       
            
            
        }
    def __init__(self,*args,**kwargs):
        super(CoordinatorForm,self).__init__(*args,**kwargs)
        self.fields['gender'].empty_label = "Select Gender"
        self.fields['degree'].empty_label = "Select Degree"

class StaffForm(forms.ModelForm):
    
    class Meta:
        model = Staff
        fields = ('StaffNationalId','f_name','l_name','gender','degree','recruit_year','phone','physical_disability', 'email', 'user')
        labels = {
            'StaffNationalId':'National Identification',
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'degree':'Level Of Education',
            'recruit_year':'Recruitment Year',
            'phone':'phone',
            'physical_disability':'Disability',
            'email':'email', 
            'user':'Select User',
              
            
            
        }
    def __init__(self,*args,**kwargs):
        super(StaffForm,self).__init__(*args,**kwargs)
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

class CoordinatorUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        
    def __init__(self, *args, **kwargs):
        super(CoordinatorUserRegistrationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username','email','password1','password2']:
            self.fields[fieldname].help_text = None
    def save(self, commit=True):
        user = super(CoordinatorUserRegistrationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
        return user



class StaffUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        
    def __init__(self, *args, **kwargs):
        super(StaffUserRegistrationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username','email','password1','password2']:
            self.fields[fieldname].help_text = None
    def save(self, commit=True):
        user = super(StaffUserRegistrationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
        return user

class budgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ('budget_amount','year')
        labels = {
            'budget_amount':'Budget Amount',
            'year':'Select the Year',
            # 'school':'School Name',
       
        }

class yearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ('year_name',)
        labels = {
            'year_name':'Year to Submit',
       
        }

class membershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('membership_amount','year')
        labels = {
            'membership_amount':'Membership Amount',
            'year':'Select the Year',
            # 'school':'School Name',
       
        }
