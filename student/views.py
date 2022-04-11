from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
import datetime
from django.db import connection
from django .http import HttpResponse,JsonResponse

# Create your views here.
from .forms import StaffForm,CourseForm, StudentForm, ClasseForm, TeacherForm, SchoolForm ,CoordinatorForm, CoordinatorUserRegistrationForm,StaffUserRegistrationForm
from .models import *
from .models import Classe, Student, Course, Sector, School ,Teacher, Province , District , Sectors , Cell , Village
from .filters import StudentFilter,TeacherFilter
from .utils import render_to_pdf
from django.template.loader import get_template


@unauthenticated_user
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get()
            return redirect('loginOrg')
    context = {'form':form}
    return render(request,'register.html', context)

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            if Board.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('homeBoard')
            elif Staff.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('homeStaff')
            elif Coordinator.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('homeCoordinator')
            elif Admin.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('homeAdmin')
            
    else:
        form = AuthenticationForm()
    return render(request, 'loginOrg.html', { 'form': form })



def logoutUser(request):
    logout(request)
    return redirect('login_view')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def homeStaff(request):
    coordinators = Coordinator.objects.all().count()
    schools = School.objects.all().count()
    teachers = Teacher.objects.all().count()
    children = Student.objects.all().count() 
    staffs = Staff.objects.all().count()
    Autisms = Student.objects.filter(physical_disability="Autism").count()
    Multiples = Student.objects.filter(physical_disability="Multiple").count()
    Cerebral_Palsys = Student.objects.filter(physical_disability="Cerebral Palsy").count()
    Down_syndroms = Student.objects.filter(physical_disability="Down syndrom").count()

    clades1 = Student.objects.filter(classe="CLADE1").count()
    clades2 = Student.objects.filter(classe="CLADE2").count()
    clades3 = Student.objects.filter(classe="CLADE3").count()


    st_male = Student.objects.filter(gender="M").count()
    st_female = Student.objects.filter(gender="F").count()

    context = {'coordinators':coordinators, 'schools':schools, 'teachers':teachers, 'children':children, 'staffs':staffs,
        'Autisms':Autisms, 'Multiples':Multiples, 'Cerebral_Palsys':Cerebral_Palsys, 'Down_syndroms':Down_syndroms,
        'st_male':st_male, 'st_female':st_female, 'clades1':clades1, 'clades2':clades2, 'clades3':clades3
    }
    return render(request, 'StaffPage.html', context)

# @login_required(login_url='loginPage')
# @allowed_users(allowed_roles=['Admin'])
def homeAdmin(request):
    context = {}
    return render(request, 'AdminPage.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def homeBoard(request):
    coordinators = Coordinator.objects.all().count()
    schools = School.objects.all().count()
    teachers = Teacher.objects.all().count()
    children = Student.objects.all().count() 
    staffs = Staff.objects.all().count()
    Autisms = Student.objects.filter(physical_disability="Autism").count()
    Multiples = Student.objects.filter(physical_disability="Multiple").count()
    Cerebral_Palsys = Student.objects.filter(physical_disability="Cerebral Palsy").count()
    Down_syndroms = Student.objects.filter(physical_disability="Down syndrom").count()

    st_male = Student.objects.filter(gender="M").count()
    st_female = Student.objects.filter(gender="F").count()

    context = {'coordinators':coordinators, 'schools':schools, 'teachers':teachers, 'children':children, 'staffs':staffs,
        'Autisms':Autisms, 'Multiples':Multiples, 'Cerebral_Palsys':Cerebral_Palsys, 'Down_syndroms':Down_syndroms,
        'st_male':st_male, 'st_female':st_female
    }
    return render(request, 'BoardPage.html', context)



@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def homeCoordinator(request):
    user = request.user
    school = School.objects.get(user=user)
    children = Student.objects.filter(school=school).count() 
    Autisms = Student.objects.filter(physical_disability="Autism", school=school).count()
    Multiples = Student.objects.filter(physical_disability="Multiple", school=school).count()
    Cerebral_Palsys = Student.objects.filter(physical_disability="Cerebral Palsy", school=school).count()
    Down_syndroms = Student.objects.filter(physical_disability="Down syndrom", school=school).count()

    clades1 = Student.objects.filter(classe="CLADE1", school=school).count()
    clades2 = Student.objects.filter(classe="CLADE2", school=school).count()
    clades3 = Student.objects.filter(classe="CLADE3", school=school).count()


    st_male = Student.objects.filter(gender="M", school=school).count()
    st_female = Student.objects.filter(gender="F", school=school).count()

    context = {'children':children, 'Autisms':Autisms, 'Multiples':Multiples, 'Cerebral_Palsys':Cerebral_Palsys, 'Down_syndroms':Down_syndroms,
        'st_male':st_male, 'st_female':st_female, 'clades1':clades1, 'clades2':clades2, 'clades3':clades3
    }
    return render(request, 'CoordinatorPage.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def addCourse(request):
    user = request.user
    school = School.objects.get(user=user)
    if request.method == "GET":
        form = CourseForm()
        context = {'form':form}
        return render(request,'CourseForm.html',context)
    else:
        form = CourseForm(request.POST)
        if form.is_valid:
           form = form.save(commit=False)
           form.school = school
           form.save()
        messages.success(request, 'Course has been Created Successfully in Your School')

        return redirect('courseList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def courseList(request):
    user = request.user
    school = School.objects.get(user=user)
    courses = Course.objects.filter(school=school)
    context={'courses':courses, 'user':user , 'school':school}
    return render(request, 'courseList.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def course_update(request, pk_course):
    course = Course.objects.get(id=pk_course)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid:
            form.save()
            messages.success(request, 'Course has been Updated Successfully')
            return redirect('courseList')
    context = {'form':form}
    return render(request, 'CourseForm.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def course_delete(request, id):
    course = Course.objects.get(pk=id)
    course.delete()
    
    messages.error(request, 'Course has been Deleted Successfully')
    return redirect(courseList)
    


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def addClasse(request):
    if request.method == "GET":
        form = ClasseForm()
        context = {'form':form}
        return render(request,'ClasseForm.html',context)
    else:
        form = ClasseForm(request.POST)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('class_name')
            messages.success(request, 'Class has been Created Successfully ' +name)
            
        return redirect('homeCoordinator')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def classeList(request):
    classes = Classe.objects.all()
    context={'classes':classes}
    return render(request, 'classeList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def class_update(request, pk_class):
    classe = Classe.objects.get(id=pk_class)
    form = ClasseForm(instance=classe)
    if request.method == 'POST':
        form = ClasseForm(request.POST, instance=classe)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('class_name')
            messages.success(request, 'Class has been Updated Successfully'+name)
            return redirect('classeList')
    context = {'form':form}
    return render(request, 'ClasseForm.html',context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def class_delete(request, id):
    classe = Classe.objects.get(pk=id)
    classe.delete()
    messages.success(request, 'Class has been deleted Successfully')
    return redirect('classeList')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def addSchool(request):
    if request.method == "GET":
        form = SchoolForm()
        context = {'form':form}
        return render(request,'SchoolForm.html',context)
    else:
        form = SchoolForm(request.POST)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('school_name')
            messages.success(request, 'School has been Created Successfully ' +name)
            
        return redirect('schoolList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def schoolList(request):
    schools = School.objects.all()
    context={'schools':schools}
    return render(request, 'schoolList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def school_update(request, pk_school):
    school = School.objects.get(id=pk_school)
    form = SchoolForm(instance=school)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid:
            form.save()
            messages.success(request, 'School has been Updated Successfully')
            return redirect('schoolList')
    context = {'form':form}
    return render(request, 'SchoolForm.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def school_delete(request, id):
    school = School.objects.get(pk=id)
    school.delete()
    messages.success(request, 'School has been deleted Successfully')
    return redirect('schoolList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def addCoordinator(request):
    if request.method == "GET":
        form = CoordinatorForm()
        context = {'form':form}
        return render(request,'CoordinatorForm.html',context)
    else:
        form = CoordinatorForm(request.POST)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('f_name')
            messages.success(request, 'Coordinator has been Created Successfully ' +name)
            
        return redirect('ListOfcoordinator')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def addStaff(request):
    if request.method == "GET":
        form = StaffForm()
        context = {'form':form}
        return render(request,'StaffForm.html',context)
    else:
        form = StaffForm(request.POST)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('f_name')
            messages.success(request, 'Staff has been Created Successfully ' +name)
            
        return redirect('ListOfStaff')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def coordinator_update(request, pk_coordinator):
    coordinator = Coordinator.objects.get(id=pk_coordinator)
    form = CoordinatorForm(instance=coordinator)
    if request.method == 'POST':
        form = CoordinatorForm(request.POST, instance=coordinator)
        if form.is_valid:
            form.save()
            messages.success(request, 'Coordinator has been Updated Successfully')
            return redirect('coordinatorListStaff')
    context = {'form':form}
    return render(request, 'CoordinatorForm.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['AdminUser'])
def coordinator_delete(request, id):
    coordinator = Coordinator.objects.get(pk=id)
    coordinator.delete()
    messages.success(request, 'Coordinator has been deleted Successfully')
    return redirect('coordinatorListStaff')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def addStudent(request):
    user = request.user
    school = School.objects.get(user=user)
    if request.method == "GET":
        form = StudentForm()
        context = {'form':form}
        return render(request,"StudentForm.html",context)
    else: 
        form = StudentForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.school = school
            form.save()
            # first_name = form.cleaned_data.get('f_name')
            messages.success(request, 'Student has been Created Successfully')
        return redirect('studentList')


@login_required(login_url='loginPage')
# @allowed_users(allowed_roles=['BoardUser'])
@allowed_users(allowed_roles=['CoordinatorUser'])
# @allowed_users(allowed_roles=['StaffUser'])
def studentList(request):
    user = request.user
    school = School.objects.get(user=user)
    students = Student.objects.filter(school=school)
    paginator = Paginator(students, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'students':students, 'page_obj':page_obj}
    return render(request, 'studentList.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def student_delete(request, id):
    student = Student.objects.get(pk=id)
    student.delete()
    messages.success(request, 'Student has been deleted Successfully')
    return redirect('studentList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def student_update(request, pk_student):
    student = Student.objects.get(id=pk_student)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid:
            form.save()
            messages.success(request, 'Student has been Updated Successfully')
            return redirect('studentList')
    context = {'form':form, 'student':student}
    return render(request, 'StudentForm.html',context)



@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def addTeacher(request):
    user = request.user
    school = School.objects.get(user=user)
    if request.method == "GET":
        form = TeacherForm()
        context = {'form':form}
        return render(request,"TeacherForm.html",context)
    else: 
        form = TeacherForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.school = school
            form.save()
            # first_name = form.cleaned_data.get('f_name')
            messages.success(request, 'Teacher has been Created Successfully')
        return redirect('teacherList')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def teacherList(request):
    user = request.user
    school = School.objects.get(user=user)
    teachers = Teacher.objects.filter(school=school)
    paginator = Paginator(teachers, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'teachers':teachers, 'page_obj':page_obj}
    return render(request, 'teacherList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def ListOfcoordinator(request):
    coordinators = Coordinator.objects.all()
    context = {'coordinators':coordinators}
    return render(request, 'coordinatorList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def ListOfcoordinatorStaff(request):
    coordinators = Coordinator.objects.all()
    context = {'coordinators':coordinators}
    return render(request, 'coordinatorListStaff.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def ListOfBoard(request):
    boards = Board.objects.all()
    context = {'boards':boards}
    return render(request, 'boardList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def ListOfStaff(request):
    staffs = Staff.objects.all()
    context = {'staffs':staffs}
    return render(request, 'staffList.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def teacher_delete(request, id):
    teacher = Teacher.objects.get(pk=id)
    teacher.delete()
    messages.success(request, 'Teacher has been deleted Successfully')
    return redirect('teacherList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def teacher_update(request, pk_teacher):
    teacher = Teacher.objects.get(id=pk_teacher)
    form = TeacherForm(instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid:
            form.save()
            messages.success(request, 'Teacher has been Updated Successfully')
            return redirect('teacherList')
    context = {'form':form}
    return render(request, 'TeacherForm.html',context)



@login_required(login_url='loginPage')
# @allowed_users(allowed_roles=['StaffUser'])
def SearchStudentList(request):
    students = Student.objects.all()
    myFilter = StudentFilter(request.GET, queryset=students)
    students = myFilter.qs 
    
    context = {'students':students,
    'myFilter':myFilter}
    return render(request, 'search.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
@allowed_users(allowed_roles=['StaffUser'])
def SearchteacherList(request):
    teachers = Teacher.objects.all()
    myFilter = TeacherFilter(request.GET, queryset=teachers)
    teachers = myFilter.qs 
    
    context = {'teachers':teachers,
    'myFilter':myFilter}
    return render(request, 'searchForTeacher.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def ListOfParent(request):
    user = request.user
    school = School.objects.get(user=user)
    students = Student.objects.filter(school=school)
    paginator = Paginator(students, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'students':students, 'page_obj':page_obj}
    return render(request, 'ParentList.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def enterMarks(request):
    
    Student_CourseFormSet = inlineformset_factory(Student.objects.filter(classe=4), Student_Course, fields=('student','course','quater','mid_marks','final_marks'),max_num=Student.objects.filter(classe=4).count(), extra=Student.objects.filter(classe=4).count())
    formset = Student_CourseFormSet(instance=Student.objects.filter(classe=4))
    if request.method == 'POST':
        form = StudentCourseForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home_school')
    
    context = {'formset':formset}
    
    
    return render(request,'schoolPages/enterMarks.html',context)


@login_required(login_url='loginPage')
def schoolStatisticalReport(request):

    context = {}
    return render(request, 'schoolStatisticalReport.html', context)



@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def StatisticalReport(request):
    user = request.user
    school = School.objects.get(user = user)
    school_id = school.id

    now = datetime.datetime.now()
    year = now.year

    cursor = connection.cursor()
    male_female = "select sum(case when gender='M' then 1 else 0 end) as male_count,sum(case when gender='F' then 1 else 0 end) as female_count, sum(case when physical_disability='YES' then 1 else 0 end) as disability_count,sum(case when physical_disability='NO' then 1 else 0 end) as no_disability_count, count(*) as n_students from student_student inner join student_classe on student_classe.id=student_student.classe_id inner join student_school on student_school.id=student_classe.school_id where student_student.year_reg=%s and student_school.id=%s" %(year, school_id)
    cursor.execute(male_female)
    answers2 = cursor.fetchall()
    context = {'answers2':answers2}
    return render(request, 'statisticalReport.html', context)



@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def SectorStatisticalReport(request):
    user = request.user
    school = Board.objects.get(user = user)
    school_id = school.id

    now = datetime.datetime.now()
    year = now.year

    cursor = connection.cursor()
    male_female = "select sum(case when gender='M' then 1 else 0 end) as male_count,sum(case when gender='F' then 1 else 0 end) as female_count, sum(case when physical_disability='YES' then 1 else 0 end) as disability_count,sum(case when physical_disability='NO' then 1 else 0 end) as no_disability_count, count(*) as n_students from student_student inner join student_classe on student_classe.id=student_student.classe_id inner join student_school on student_school.id=student_classe.school_id where student_student.year_reg=%s and student_school.id=%s" %(year, school_id)
    cursor.execute(male_female)
    answers2 = cursor.fetchall()
    context = {'answers2':answers2}
    

    return render(request, 'SectorStatisticalReport.html', context)


def error401(request):

    context = {}
    return render(request, '401.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def ajaxSearch(request):
    if 'term' in request.GET:
        qs = Teacher.objects.filter(f_name__icontains=request.GET.get('term'))
        qs = Teacher.objects.filter(f_name__istartswith=request.GET.get('term'))
        f_name = list()
        for teacher in qs:
            f_name.append(teacher.f_name)
        return JsonResponse(f_name, safe=False)
    context = {}
    return render(request, 'ajaxTeacherForm.html', context)
   


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def autosuggest(request):
    print(request.GET)
    query_original = request.GET.get(term)

    context = {}
    return render(request, 'ajaxTeacherForm.html', context)

def register_coordinator_user(request):
    form = CoordinatorUserRegistrationForm()
    if request.method == 'POST':
        form = CoordinatorUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='CoordinatorUser')
            user.groups.add(group)
            messages.success(request, 'School director user has been successfully registered')
            
            return redirect('addCoordinator')
    
    context = {'form':form}
    return render(request, 'coordinator_user_form.html', context)


def register_staff_user(request):
    form = StaffUserRegistrationForm()
    if request.method == 'POST':
        form = StaffUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='StaffUser')
            user.groups.add(group)
            messages.success(request, 'Staff user has been successfully registered')
            
            return redirect('addStaff')
    
    context = {'form':form}
    return render(request, 'staff_user_form.html', context)

def footer(request):
    context = {}
    return render(request, 'footer.html', context)

def testPdf(request):
    template = get_template('testpdf.html')
    user = request.user
    
    # return render(request, 'testpdf.html')
    context = {}
    html = template.render(context)
    pdf= render_to_pdf('testpdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Test pdf"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"


    