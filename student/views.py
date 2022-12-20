from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
import datetime
from django.db.models import Sum
from django.db import connection
from django .http import HttpResponse,JsonResponse

# Create your views here.
from .forms import membershipValidation,membershipForm,budgetForm,yearForm,StaffForm,CourseForm, StudentForm, ClasseForm, TeacherForm, SchoolForm ,CoordinatorForm, CoordinatorUserRegistrationForm,StaffUserRegistrationForm
from .models import *
from .models import Classe, Student, Course, Sector, School ,Teacher, Province , District , Sectors , Cell , Village, Year, Membership, Budget
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
    Cerebral_PalsysID = Student.objects.filter(physical_disability="Cerebral Palsy ID").count()
    Down_syndroms = Student.objects.filter(physical_disability="Down syndrom").count()

    clades1 = Student.objects.filter(classe="CLADE1").count()
    clades2 = Student.objects.filter(classe="CLADE2").count()
    clades3 = Student.objects.filter(classe="CLADE3").count()
    clades4 = Student.objects.filter(classe="CLADE4").count()
    clades5 = Student.objects.filter(classe="CLADE5").count()
    clades6 = Student.objects.filter(classe="CLADE6").count()


    st_male = Student.objects.filter(gender="M").count()
    st_female = Student.objects.filter(gender="F").count()

    context = {'coordinators':coordinators, 'schools':schools, 'teachers':teachers, 'children':children, 'staffs':staffs,
        'Autisms':Autisms, 'Multiples':Multiples, 'Cerebral_Palsys':Cerebral_Palsys, 'Down_syndroms':Down_syndroms,
        'st_male':st_male, 'st_female':st_female, 'clades1':clades1, 'clades2':clades2, 'clades3':clades3, 'clades4':clades4, 'clades5':clades5, 'clades6':clades6 ,
        'Cerebral_PalsysID':Cerebral_PalsysID
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
    Cerebral_PalsysID = Student.objects.filter(physical_disability="Cerebral Palsy ID").count()
    Down_syndroms = Student.objects.filter(physical_disability="Down syndrom").count()

    st_male = Student.objects.filter(gender="M").count()
    st_female = Student.objects.filter(gender="F").count()

    

    context = {'coordinators':coordinators, 'schools':schools, 'teachers':teachers, 'children':children, 'staffs':staffs,
        'Autisms':Autisms, 'Multiples':Multiples, 'Cerebral_Palsys':Cerebral_Palsys, 'Down_syndroms':Down_syndroms,
        'st_male':st_male, 'st_female':st_female, 'Cerebral_PalsysID':Cerebral_PalsysID
    }
    # messages.success(request, 'Welcome You are Logged In As Board User')
    return render(request, 'BoardPage.html', context)



@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def homeCoordinator(request):
    user = request.user
    school = School.objects.get(user=user)

    children = Student.objects.filter(school=school).count() 
    tot_staff = Teacher.objects.filter(school=school).count() 
    teachers = Teacher.objects.filter(service="Teacher",school=school).count()
    nurses = Teacher.objects.filter(service="Nurse",school=school).count()
    fusios = Teacher.objects.filter(service="Physio",school=school).count()
    cares = Teacher.objects.filter(service="Care giver",school=school).count()


    Autisms = Student.objects.filter(physical_disability="Autism", school=school).count()
    Multiples = Student.objects.filter(physical_disability="Multiple", school=school).count()
    Cerebral_Palsys = Student.objects.filter(physical_disability="Cerebral Palsy", school=school).count()
    Cerebral_PalsysID = Student.objects.filter(physical_disability="Cerebral Palsy ID" , school=school).count()
    
    Down_syndroms = Student.objects.filter(physical_disability="Down syndrom", school=school).count()

    clades1 = Student.objects.filter(classe="CLADE1", school=school).count()
    clades2 = Student.objects.filter(classe="CLADE2", school=school).count()
    clades3 = Student.objects.filter(classe="CLADE3", school=school).count()
    clades4 = Student.objects.filter(classe="CLADE4", school=school).count()
    clades5 = Student.objects.filter(classe="CLADE5", school=school).count()
    clades6 = Student.objects.filter(classe="CLADE6", school=school).count()


    st_male = Student.objects.filter(gender="M", school=school).count()
    st_female = Student.objects.filter(gender="F", school=school).count()

    context = {'tot_staff':tot_staff,'fusios':fusios,'cares':cares,'nurses':nurses,'teachers':teachers,'children':children, 'Autisms':Autisms, 'Multiples':Multiples, 'Cerebral_Palsys':Cerebral_Palsys, 'Down_syndroms':Down_syndroms,
        'st_male':st_male, 'st_female':st_female, 'clades1':clades1, 'clades2':clades2, 'clades3':clades3 , 'clades4':clades4, 'clades5':clades5, 'clades6':clades6 , 'Cerebral_PalsysID':Cerebral_PalsysID
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
    user = request.user
    school = School.objects.get(user=user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid:
            form = form.save(commit=False)
            form.school = school
            form.save()
            messages.success(request, 'Course has been Updated Successfully')
            return redirect('courseList')
    context = {'form':form}
    return render(request, 'CourseForm.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def membership_update(request, pk_course):
    membership = Membership.objects.get(id=pk_course)
    form = membershipValidation(instance=membership)
    if request.method == 'POST':
        form = membershipValidation(request.POST, instance=membership)
        if form.is_valid:
            form.save()
            messages.success(request, 'Membership has been Updated Successfully')
            return redirect('ListOfSiteMembershipFee')
    context = {'form':form}
    return render(request, 'membershipValidation.html',context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def budget_update(request, pk_course):
    budget = Budget.objects.get(id=pk_course)
    form = budgetForm(instance=budget)
    if request.method == 'POST':
        form = budgetForm(request.POST, instance=budget)
        if form.is_valid:
            form.save()
            messages.success(request, 'Budget has been Updated Successfully')
            return redirect('budgetList')
    context = {'form':form}
    return render(request, 'budgetForm.html',context)

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
            
        return redirect('classeList')


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
@allowed_users(allowed_roles=['StaffUser'])
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
@allowed_users(allowed_roles=['StaffUser'])
def schoolList(request):
    schools = School.objects.all()
    context={'schools':schools}
    return render(request, 'schoolList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
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
@allowed_users(allowed_roles=['StaffUser'])
def school_delete(request, id):
    school = School.objects.get(pk=id)
    school.delete()
    messages.success(request, 'School has been deleted Successfully')
    return redirect('schoolList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
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
            return redirect('ListOfcoordinatorStaff')
    context = {'form':form}
    return render(request, 'CoordinatorForm.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['AdminUser'])
def coordinator_delete(request, id):
    coordinator = Coordinator.objects.get(pk=id)
    coordinator.delete()
    messages.success(request, 'Coordinator has been deleted Successfully')
    return redirect('ListOfcoordinatorStaff')

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
@allowed_users(allowed_roles=['StaffUser'])
def studentListStaff(request):
    user = request.user
    students = Student.objects.all()
    paginator = Paginator(students, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'students':students, 'page_obj':page_obj}
    return render(request, 'studentListStfaff.html', context)



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
@allowed_users(allowed_roles=['StaffUser'])
def student_details(request, pk_student):
    student = Student.objects.get(id=pk_student)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid:
            form.save()
            messages.success(request, 'Student has been Updated Successfully')
            return redirect('studentListStaff')
    context = {'form':form, 'student':student}
    return render(request, 'studentDetails.html',context)



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
            messages.success(request, 'Staff has been Created Successfully')
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
@allowed_users(allowed_roles=['BoardUser'])
def staff_update(request, pk_teacher):
    staffs = Staff.objects.get(id=pk_teacher)
    form = StaffForm(instance=staffs)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staffs)
        if form.is_valid:
            form.save()
            messages.success(request, 'Staff has been Updated Successfully')
            return redirect('ListOfStaff')
    context = {'form':form}
    return render(request, 'staffForm.html',context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def teacher_delete(request, id):
    teacher = Teacher.objects.get(pk=id)
    teacher.delete()
    messages.success(request, 'Teacher has been deleted Successfully')
    return redirect('teacherList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['BoardUser'])
def teacher_update(request, pk_teacher):
    teacher = Teacher.objects.get(id=pk_teacher)
    form = TeacherForm(instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid:
            form.save()
            messages.success(request, 'Staff has been Updated Successfully')
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

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
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

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['BoardUser'])
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


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['BoardUser'])
def sitesBoardReport(request):

    malestd= Student.objects.filter(gender='M').count()
    femalestd= Student.objects.filter(gender='F').count()
    malestf= Staff.objects.filter(gender='M').count()
    femalestf= Staff.objects.filter(gender='F').count()

    schools = School.objects.all()

    context = {'malestd':malestd, 'femalestd':femalestd, 
                'malestf':malestf, 'femalestf':femalestf,
                'schools':schools
                }
    return render(request, 'generalBoardReport.html',context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StaffUser'])
def siteStaffReport(request):

    malestd= Student.objects.filter(gender='M').count()
    femalestd= Student.objects.filter(gender='F').count()
    malecoo= Coordinator.objects.filter(gender='M').count()
    femalecoo= Coordinator.objects.filter(gender='F').count()
    years = Year.objects.all()


    context = {'malestd':malestd, 'femalestd':femalestd,'malecoo':malecoo, 'femalecoo':femalecoo,
                'years':years,}
    return render(request, 'generalStaffReport.html',context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['CoordinatorUser'])
def siteschoolReport(request):

    user = request.user
    school = School.objects.get(user=user)
    st_male = Student.objects.filter(gender="M", school=school).count()
    st_female = Student.objects.filter(gender="F", school=school).count()
    maleteac= Teacher.objects.filter(gender='M', school=school).count()
    femaleteac= Teacher.objects.filter(gender='F', school=school).count()
 

    context = {'user':user,'school':school,
        'st_male':st_male, 'st_female':st_female,'maleteac':maleteac, 'femaleteac':femaleteac}
    return render(request, 'generalCoordinatorReport.html',context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def addYear(request):
    if request.method == "GET":
        form = yearForm()
        context = {'form':form}
        return render(request,'yearForm.html',context)
    else:
        form = yearForm(request.POST)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('year_name')
            messages.success(request, 'Year has been Created Successfully ' +name)
            
        return redirect('ListOfYear')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def ListOfYear(request):
    years = Year.objects.all()
    context = {'years':years}
    return render(request, 'yearList.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def addBudget(request):
    user = request.user
    school = School.objects.get(user=user)
    if request.method == "GET":
        form = budgetForm()
        context = {'form':form}
        return render(request,"budgetForm.html",context)
    else: 
        form = budgetForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.school = school
            form.save()
            # first_name = form.cleaned_data.get('f_name')
            messages.success(request, 'Budget has been Created Successfully')
        return redirect('budgetList')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def budgetList(request):
    user = request.user
    school = School.objects.get(user=user)
    budgets = Budget.objects.filter(school=school)
    paginator = Paginator(budgets, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'budgets':budgets, 'page_obj':page_obj}
    return render(request, 'budgetList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def addMembership(request):
    user = request.user
    school = School.objects.get(user=user)
    if request.method == "GET":
        form = membershipForm()
        context = {'form':form}
        return render(request,"membershipForm.html",context)
    else: 
        form = membershipForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.school = school
            form.status = "UNVERIFIED"
            form.save()
            # first_name = form.cleaned_data.get('f_name')
            messages.success(request, 'Membership has been Created Successfully')
        return redirect('membershiptList')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['CoordinatorUser'])
def membershiptList(request):
    user = request.user
    school = School.objects.get(user=user)
    members = Membership.objects.filter(school=school)
    paginator = Paginator(members, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'members':members, 'page_obj':page_obj}
    return render(request, 'membershipList.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['StaffUser'])
def ListOfSiteMembershipFee(request):
    members = Membership.objects.all()
    paginator = Paginator(members, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'members':members, 'page_obj':page_obj}
    return render(request, 'allmembershipList.html', context)

def globalCumurativeDisability(request):
    
    template = get_template('globalCumurativeDisability.html')

    current_year = datetime.datetime.now().year
    six_year_before = current_year - 6
    thirteen_year_before = current_year - 13
    twenty_five_year_before = current_year - 25
    
    all_men = Student.objects.filter(gender='M').count()
    all_female = Student.objects.filter(gender='F').count()
    
    
    
    men_six_utism = Student.objects.filter(gender='M', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Autism').count()
    men_six_multiple= Student.objects.filter(gender='M', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Multiple').count()
    men_six_cerebral_palsy= Student.objects.filter(gender='M', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy').count()
    men_six_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
    men_six_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
    men_six_downsyndrome = Student.objects.filter(gender='M', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Down syndrom').count()
    
    female_six_utism = Student.objects.filter(gender='F', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Autism').count()
    female_six_multiple= Student.objects.filter(gender='F', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Multiple').count()
    female_six_cerebral_palsy= Student.objects.filter(gender='F', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy').count()
    female_six_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
    female_six_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
    female_six_downsyndrome = Student.objects.filter(gender='F', dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Down syndrom').count()
    

    men_thirteen_utism = Student.objects.filter(gender='M', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Autism').count()
    men_thirteen_multiple= Student.objects.filter(gender='M', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Multiple').count()
    men_thirteen_cerebral_palsy= Student.objects.filter(gender='M', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy').count()
    men_thirteen_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
    men_thirteen_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
    men_thirteen_downsyndrome = Student.objects.filter(gender='M', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Down syndrom').count()
    
    female_thirteen_utism = Student.objects.filter(gender='F', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Autism').count()
    female_thirteen_multiple= Student.objects.filter(gender='F', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Multiple').count()
    female_thirteen_cerebral_palsy= Student.objects.filter(gender='F', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy').count()
    female_thirteen_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
    female_thirteen_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
    female_thirteen_downsyndrome = Student.objects.filter(gender='F', dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Down syndrom').count()
    
    
    men_twenty_five_utism = Student.objects.filter(gender='M', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Autism').count()
    men_twenty_five_multiple= Student.objects.filter(gender='M', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Multiple').count()
    men_twenty_five_cerebral_palsy= Student.objects.filter(gender='M', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy').count()
    men_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
    men_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
    men_twenty_five_downsyndrome = Student.objects.filter(gender='M', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Down syndrom').count()
    
    female_twenty_five_utism = Student.objects.filter(gender='F', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Autism').count()
    female_twenty_five_multiple= Student.objects.filter(gender='F', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Multiple').count()
    female_twenty_five_cerebral_palsy= Student.objects.filter(gender='F', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy').count()
    female_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
    female_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
    female_twenty_five_downsyndrome = Student.objects.filter(gender='F', dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Down syndrom').count()
    
    
    men_above_twenty_five_utism = Student.objects.filter(gender='M', dob__year__lt=twenty_five_year_before, physical_disability='Autism').count()
    men_above_twenty_five_multiple= Student.objects.filter(gender='M', dob__year__lt=twenty_five_year_before, physical_disability='Multiple').count()
    men_above_twenty_five_cerebral_palsy= Student.objects.filter(gender='M', dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy').count()
    men_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
    men_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
    men_above_twenty_five_downsyndrome = Student.objects.filter(gender='M', dob__year__lt=twenty_five_year_before, physical_disability='Down syndrom').count()
    
    female_above_twenty_five_utism = Student.objects.filter(gender='F', dob__year__lt=twenty_five_year_before, physical_disability='Autism').count()
    female_above_twenty_five_multiple= Student.objects.filter(gender='F', dob__year__lt=twenty_five_year_before, physical_disability='Multiple').count()
    female_above_twenty_five_cerebral_palsy= Student.objects.filter(gender='F', dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy').count()
    female_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
    female_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
    female_above_twenty_five_downsyndrome = Student.objects.filter(gender='F', dob__year__lt=twenty_five_year_before, physical_disability='Down syndrom').count()
    
    context = {'all_men':all_men,'all_female':all_female,'men_six_utism':men_six_utism,
            'men_six_multiple':men_six_multiple,'men_six_cerebral_palsy':men_six_cerebral_palsy,
            'men_six_cerebral_palsy_id':men_six_cerebral_palsy_id,'men_six_downsyndrome':men_six_downsyndrome,
            'female_six_utism':female_six_utism,'female_six_multiple':female_six_multiple,'female_six_cerebral_palsy':female_six_cerebral_palsy,
            'female_six_cerebral_palsy_id':female_six_cerebral_palsy_id,'female_six_downsyndrome':female_six_downsyndrome,'men_thirteen_utism':men_thirteen_utism,
            'men_thirteen_multiple':men_thirteen_multiple,'men_thirteen_cerebral_palsy':men_thirteen_cerebral_palsy,'men_thirteen_cerebral_palsy_id':men_thirteen_cerebral_palsy_id,
            'men_thirteen_downsyndrome':men_thirteen_downsyndrome,'female_thirteen_utism':female_thirteen_utism,'female_thirteen_multiple':female_thirteen_multiple,
            'female_thirteen_cerebral_palsy':female_thirteen_cerebral_palsy,'female_thirteen_cerebral_palsy_id':female_thirteen_cerebral_palsy_id,'female_thirteen_downsyndrome':female_thirteen_downsyndrome,
            'men_twenty_five_utism':men_twenty_five_utism,'men_twenty_five_multiple':men_twenty_five_multiple,'men_twenty_five_cerebral_palsy':men_twenty_five_cerebral_palsy,
            'men_twenty_five_cerebral_palsy_id':men_twenty_five_cerebral_palsy_id,'men_twenty_five_downsyndrome':men_twenty_five_downsyndrome,'female_twenty_five_utism':female_twenty_five_utism,
            'female_twenty_five_multiple':female_twenty_five_multiple,'female_twenty_five_cerebral_palsy':female_twenty_five_cerebral_palsy,'female_twenty_five_cerebral_palsy_id':female_twenty_five_cerebral_palsy_id,
            'female_twenty_five_downsyndrome':female_twenty_five_downsyndrome,'men_above_twenty_five_utism':men_above_twenty_five_utism,'men_above_twenty_five_multiple':men_above_twenty_five_multiple,
            'men_above_twenty_five_cerebral_palsy':men_above_twenty_five_cerebral_palsy,'men_above_twenty_five_cerebral_palsy_id':men_above_twenty_five_cerebral_palsy_id,'men_above_twenty_five_downsyndrome':men_above_twenty_five_downsyndrome,
            'female_above_twenty_five_utism':female_above_twenty_five_utism,'female_above_twenty_five_multiple':female_above_twenty_five_multiple,'female_above_twenty_five_cerebral_palsy':female_above_twenty_five_cerebral_palsy,
            'female_above_twenty_five_cerebral_palsy_id':female_above_twenty_five_cerebral_palsy_id,'female_above_twenty_five_downsyndrome':female_above_twenty_five_downsyndrome
                }
    return render(request, 'globalCumurativeDisability.html', context)
    html = template.render(context)
    pdf= render_to_pdf('globalCumurativeDisability.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Global Cumulative Disability"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def disabilityReportSingleSite(request):
    
    template = get_template('disabilityReportSingleSite.html')
    
    try: 
        schoolId = request.GET.get('school')
    except:
        schoolId = None
    if schoolId:
        school = School.objects.get(id=schoolId)
        current_year = datetime.datetime.now().year
        six_year_before = current_year - 6
        thirteen_year_before = current_year - 13
        twenty_five_year_before = current_year - 25
        
        all_men = Student.objects.filter(gender='M', school=school).count()
        all_female = Student.objects.filter(gender='F', school=school).count()
        
        
        men_six_utism = Student.objects.filter(gender='M', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Autism').count()
        men_six_multiple= Student.objects.filter(gender='M', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Multiple').count()
        men_six_cerebral_palsy= Student.objects.filter(gender='M', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy').count()
        men_six_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
        men_six_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
        men_six_downsyndrome = Student.objects.filter(gender='M', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Down syndrom').count()
        
        female_six_utism = Student.objects.filter(gender='F', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Autism').count()
        female_six_multiple= Student.objects.filter(gender='F', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Multiple').count()
        female_six_cerebral_palsy= Student.objects.filter(gender='F', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy').count()
        female_six_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
        female_six_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Cerebral Palsy ID').count()
        female_six_downsyndrome = Student.objects.filter(gender='F', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year, physical_disability='Down syndrom').count()
        

        men_thirteen_utism = Student.objects.filter(gender='M', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Autism').count()
        men_thirteen_multiple= Student.objects.filter(gender='M', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Multiple').count()
        men_thirteen_cerebral_palsy= Student.objects.filter(gender='M', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy').count()
        men_thirteen_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
        men_thirteen_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
        men_thirteen_downsyndrome = Student.objects.filter(gender='M', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Down syndrom').count()
        
        female_thirteen_utism = Student.objects.filter(gender='F', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Autism').count()
        female_thirteen_multiple= Student.objects.filter(gender='F', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Multiple').count()
        female_thirteen_cerebral_palsy= Student.objects.filter(gender='F', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy').count()
        female_thirteen_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
        female_thirteen_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Cerebral Palsy ID').count()
        female_thirteen_downsyndrome = Student.objects.filter(gender='F', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before, physical_disability='Down syndrom').count()
        
        
        men_twenty_five_utism = Student.objects.filter(gender='M', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Autism').count()
        men_twenty_five_multiple= Student.objects.filter(gender='M', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Multiple').count()
        men_twenty_five_cerebral_palsy= Student.objects.filter(gender='M', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy').count()
        men_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
        men_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
        men_twenty_five_downsyndrome = Student.objects.filter(gender='M', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Down syndrom').count()
        
        female_twenty_five_utism = Student.objects.filter(gender='F', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Autism').count()
        female_twenty_five_multiple= Student.objects.filter(gender='F', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Multiple').count()
        female_twenty_five_cerebral_palsy= Student.objects.filter(gender='F', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy').count()
        female_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
        female_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Cerebral Palsy ID').count()
        female_twenty_five_downsyndrome = Student.objects.filter(gender='F', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before, physical_disability='Down syndrom').count()
        
        
        men_above_twenty_five_utism = Student.objects.filter(gender='M', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Autism').count()
        men_above_twenty_five_multiple= Student.objects.filter(gender='M', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Multiple').count()
        men_above_twenty_five_cerebral_palsy= Student.objects.filter(gender='M', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy').count()
        men_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
        men_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='M', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
        men_above_twenty_five_downsyndrome = Student.objects.filter(gender='M', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Down syndrom').count()
        
        female_above_twenty_five_utism = Student.objects.filter(gender='F', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Autism').count()
        female_above_twenty_five_multiple= Student.objects.filter(gender='F', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Multiple').count()
        female_above_twenty_five_cerebral_palsy= Student.objects.filter(gender='F', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy').count()
        female_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
        female_above_twenty_five_cerebral_palsy_id= Student.objects.filter(gender='F', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Cerebral Palsy ID').count()
        female_above_twenty_five_downsyndrome = Student.objects.filter(gender='F', school=school, dob__year__lt=twenty_five_year_before, physical_disability='Down syndrom').count()
    
    context = {'school':school,'all_men':all_men,'all_female':all_female,'men_six_utism':men_six_utism,
               'men_six_multiple':men_six_multiple,'men_six_cerebral_palsy':men_six_cerebral_palsy,
                'men_six_cerebral_palsy_id':men_six_cerebral_palsy_id,'men_six_downsyndrome':men_six_downsyndrome,
                'female_six_utism':female_six_utism,'female_six_multiple':female_six_multiple,'female_six_cerebral_palsy':female_six_cerebral_palsy,
                'female_six_cerebral_palsy_id':female_six_cerebral_palsy_id,'female_six_downsyndrome':female_six_downsyndrome,'men_thirteen_utism':men_thirteen_utism,
                'men_thirteen_multiple':men_thirteen_multiple,'men_thirteen_cerebral_palsy':men_thirteen_cerebral_palsy,'men_thirteen_cerebral_palsy_id':men_thirteen_cerebral_palsy_id,
                'men_thirteen_downsyndrome':men_thirteen_downsyndrome,'female_thirteen_utism':female_thirteen_utism,'female_thirteen_multiple':female_thirteen_multiple,
                'female_thirteen_cerebral_palsy':female_thirteen_cerebral_palsy,'female_thirteen_cerebral_palsy_id':female_thirteen_cerebral_palsy_id,'female_thirteen_downsyndrome':female_thirteen_downsyndrome,
                'men_twenty_five_utism':men_twenty_five_utism,'men_twenty_five_multiple':men_twenty_five_multiple,'men_twenty_five_cerebral_palsy':men_twenty_five_cerebral_palsy,
                'men_twenty_five_cerebral_palsy_id':men_twenty_five_cerebral_palsy_id,'men_twenty_five_downsyndrome':men_twenty_five_downsyndrome,'female_twenty_five_utism':female_twenty_five_utism,
                'female_twenty_five_multiple':female_twenty_five_multiple,'female_twenty_five_cerebral_palsy':female_twenty_five_cerebral_palsy,'female_twenty_five_cerebral_palsy_id':female_twenty_five_cerebral_palsy_id,
                'female_twenty_five_downsyndrome':female_twenty_five_downsyndrome,'men_above_twenty_five_utism':men_above_twenty_five_utism,'men_above_twenty_five_multiple':men_above_twenty_five_multiple,
                'men_above_twenty_five_cerebral_palsy':men_above_twenty_five_cerebral_palsy,'men_above_twenty_five_cerebral_palsy_id':men_above_twenty_five_cerebral_palsy_id,'men_above_twenty_five_downsyndrome':men_above_twenty_five_downsyndrome,
                'female_above_twenty_five_utism':female_above_twenty_five_utism,'female_above_twenty_five_multiple':female_above_twenty_five_multiple,'female_above_twenty_five_cerebral_palsy':female_above_twenty_five_cerebral_palsy,
                'female_above_twenty_five_cerebral_palsy_id':female_above_twenty_five_cerebral_palsy_id,'female_above_twenty_five_downsyndrome':female_above_twenty_five_downsyndrome
                 }
  # to use pdf remove comment to return render          
    return render(request, 'disabilityReportSingleSite.html', context)
    html = template.render(context)
    pdf= render_to_pdf('disabilityReportSingleSite.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Global Cumulative Disability Single Site"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"



def schoolMembershipReport(request):
    
    template = get_template('schoolMembershipReport.html')
    
    try: 
        schoolId = request.GET.get('school')
    except:
        schoolId = None
    if schoolId:
        school = School.objects.get(id=schoolId)
        school_memberships_unverified = Membership.objects.filter(school=school, status='UNVERIFIED')
        school_memberships_unverified_sum = Membership.objects.filter(school=school, status='UNVERIFIED').aggregate(Sum('membership_amount')).get('membership_amount__sum', 0.00)
    
        school_memberships_verified = Membership.objects.filter(school=school, status='VERIFIED')
        school_memberships_verified_sum = Membership.objects.filter(school=school, status='VERIFIED').aggregate(Sum('membership_amount')).get('membership_amount__sum', 0.00)   
    
    context = {'school':school,'school_memberships_unverified':school_memberships_unverified,'school_memberships_verified':school_memberships_verified,                
                'school_memberships_unverified_sum':school_memberships_unverified_sum, 'school_memberships_verified_sum':school_memberships_verified_sum}
    # to use pdf comment return render
    return render(request, 'schoolMembershipReport.html', context)
    html = template.render(context)
    pdf= render_to_pdf('schoolMembershipReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Single Site Membership Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"


def yearMembershipReport(request):
    
    template = get_template('yearMembershipReport.html')
    
    try: 
        yearId = request.GET.get('year')
    except:
        yearId = None
    if yearId:
        year = Year.objects.get(id=yearId)
        school_membership = Membership.objects.filter(year=year)

    context = {'year':year,'school_membership':school_membership}
    # to use pdf comment return render
    return render(request, 'yearMembershipReport.html', context)
    html = template.render(context)
    pdf= render_to_pdf('yearMembershipReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Yearly Site Membership Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def yearBudgetReport(request):
    
    template = get_template('yearbudgetReport.html')
    
    try: 
        yearId = request.GET.get('year')
    except:
        yearId = None
    if yearId:
        year = Year.objects.get(id=yearId)
        school_budget = Budget.objects.filter(year=year)

    context = {'year':year,'school_budget':school_budget}
    # to use pdf comment return render
    return render(request, 'yearbudgetReport.html', context)
    html = template.render(context)
    pdf= render_to_pdf('yearbudgetReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Yearly Site Budget Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

def siteStaffRole(request):
    template = get_template('siteStaffRole.html')
    
    user = request.user
    school = School.objects.get(user=user)
    address = school.province
    school_name= school.school_name
    teachers = Teacher.objects.filter(school=school)
    tot_tea = teachers.count()
    
    context = {'teachers':teachers, 'school':school, user:'user','address':address,'tot_tea':tot_tea}
    html = template.render(context)
    pdf= render_to_pdf('siteStaffRole.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Single Site Staff Role Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"


def siteBeneficiallyList(request):
    template = get_template('siteBeneficially.html')
    
    user = request.user
    school = School.objects.get(user=user)
    address = school.province
    students = Student.objects.filter(school=school)
    tot_bene = students.count()
    
    context = {'students':students, 'school':school, user:'user','address':address,'tot_bene':tot_bene}
    html = template.render(context)
    pdf= render_to_pdf('siteBeneficially.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Single Site Beneficially Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"


def siteParentList(request):
    template = get_template('siteParent.html')
    
    user = request.user
    school = School.objects.get(user=user)
    address = school.province
    students = Student.objects.filter(school=school)
    
    context = {'students':students, 'school':school, user:'user','address':address}
    html = template.render(context)
    pdf= render_to_pdf('siteParent.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Single Site Beneficially Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"



def schoolgenderReport(request):
    
    template = get_template('schoolgenderReport.html')
    
    try: 
        schoolId = request.GET.get('school')
    except:
        schoolId = None
    if schoolId:
        school = School.objects.get(id=schoolId)
        school_male_beneficially = Student.objects.filter(school=school, gender='M').count()
        school_female_beneficially = Student.objects.filter(school=school, gender='F').count()
        
    context = {'school':school,'school_male_beneficially':school_male_beneficially,'school_female_beneficially':school_female_beneficially}
    return render(request, 'schoolgenderReport.html', context)
    html = template.render(context)
    pdf= render_to_pdf('schoolgenderReport.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Single Site Gender Report"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"



def ageReportSingleSite(request):
    
    template = get_template('ageReportSingleSite.html')
    
    try: 
        schoolId = request.GET.get('school')
    except:
        schoolId = None
    if schoolId:
        school = School.objects.get(id=schoolId)
        current_year = datetime.datetime.now().year
        six_year_before = current_year - 6
        thirteen_year_before = current_year - 13
        twenty_five_year_before = current_year - 25
        
        all_men = Student.objects.filter(gender='M', school=school).count()
        all_female = Student.objects.filter(gender='F', school=school).count()
        
        
        men_six= Student.objects.filter(gender='M', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year).count()
   
        female_six = Student.objects.filter(gender='F', school=school, dob__year__gte=six_year_before, dob__year__lte=current_year).count()
     

        men_thirteen = Student.objects.filter(gender='M', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before).count()
 
        female_thirteen = Student.objects.filter(gender='F', school=school, dob__year__gte=thirteen_year_before, dob__year__lt=six_year_before).count()
   
        
        men_twenty_five = Student.objects.filter(gender='M', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before).count()
   
        female_twenty_five = Student.objects.filter(gender='F', school=school, dob__year__gte=twenty_five_year_before, dob__year__lt=thirteen_year_before).count()
   
        
        men_above_twenty_five= Student.objects.filter(gender='M', school=school, dob__year__lt=twenty_five_year_before).count()
    
        female_above_twenty_five = Student.objects.filter(gender='F', school=school, dob__year__lt=twenty_five_year_before).count()
    
    context = {'school':school,'all_men':all_men,'all_female':all_female,
                'men_six':men_six,'female_six':female_six,
                'men_thirteen':men_thirteen,'female_thirteen':female_thirteen,
                'men_twenty_five':men_twenty_five,'female_twenty_five':female_twenty_five,
                'men_above_twenty_five':men_above_twenty_five,'female_above_twenty_five':female_above_twenty_five,
                 }
    # remove or add comment below          
    return render(request, 'ageReportSingleSite.html', context)
    html = template.render(context)
    pdf= render_to_pdf('ageReportSingleSite.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        file_name = "Global Cumulative Disability Single Site"
        content = "inline; filename='%s'" %(file_name)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
    return HttpResponse*"Not found"

