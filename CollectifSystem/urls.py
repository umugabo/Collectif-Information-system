"""CollectifSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from student.views import yearBudgetReport,yearMembershipReport,siteParentList,siteBeneficiallyList,membership_update,ageReportSingleSite,schoolgenderReport,siteStaffRole, addMembership,ListOfSiteMembershipFee, disabilityReportSingleSite, globalCumurativeDisability,membershiptList,budgetList,addBudget,ListOfYear,addYear, schoolMembershipReport,siteschoolReport,siteStaffReport,sitesBoardReport,register_staff_user,addStaff,register_coordinator_user, testPdf,SectorStatisticalReport,StatisticalReport,login_view,budget_update, homeStaff, homeCoordinator, addSchool, school_delete, schoolList, school_update, homeAdmin, homeBoard, studentList, classeList, courseList, addCoordinator,ListOfcoordinator ,ListOfParent ,ListOfcoordinatorStaff,ListOfBoard, ListOfStaff,login,studentListStaff,student_details, addCourse, addClasse, addStudent, student_delete, student_update, class_update, class_delete, course_update, course_delete, addTeacher, teacherList ,teacher_delete, teacher_update, coordinator_update, coordinator_delete, registerPage, SearchStudentList, SearchteacherList, logoutUser, error401, ajaxSearch, footer, addCourse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('homeStaff', homeStaff, name='homeStaff'),
    path('homeBoard',homeBoard, name ='homeBoard'),
    path('homeAdmin',homeAdmin, name ='homeAdmin'),
    path('homeCoordinator',homeCoordinator, name ='homeCoordinator'),
    path('',login_view, name='login_view'),
    path('studentList', studentList, name='studentList'),
    path('classeList', classeList, name='classeList'),
    path('courseList', courseList, name='courseList'),
    path('addCourse', addCourse, name='addCourse'),
    path('addClasse', addClasse, name='addClasse'),
    path('addStudent', addStudent, name='addStudent'),
    path('student_delete/<str:id>', student_delete, name='student_delete'),
    path('student_update/<str:pk_student>',student_update, name='student_update'),
    path('student_details/<str:pk_student>',student_details, name='student_details'),
    path('class_update/<str:pk_class>',class_update, name='class_update'),
    path('class_delete/<str:id>',class_delete, name='class_delete'),
    path('course_update/<str:pk_course>',course_update, name='course_update'),
    path('membership_update/<str:pk_course>',membership_update, name='membership_update'),
    path('budget_update/<str:pk_course>',budget_update, name='budget_update'),
    path('course_delete/<str:id>',course_delete, name='course_delete'),
    path('SearchStudentList',SearchStudentList, name='SearchStudentList'),
    path('SearchteacherList',SearchteacherList, name='SearchteacherList'),
    path('registerPage',registerPage, name='registerPage'),
    path('addTeacher',addTeacher, name='addTeacher'),
    path('teacherList',teacherList, name='teacherList'),
    path('addCoordinator', addCoordinator, name='addCoordinator'),
    path('ListOfcoordinator', ListOfcoordinator, name='ListOfcoordinator'),
    path('ListOfcoordinatorStaff', ListOfcoordinatorStaff, name='ListOfcoordinatorStaff'),
    path('ListOfBoard', ListOfBoard, name='ListOfBoard'),
    path('ListOfParent', ListOfParent, name='ListOfParent'),
    path('ListOfStaff', ListOfStaff, name='ListOfStaff'),
    path('teacher_update/<str:pk_teacher>',teacher_update, name='teacher_update'),
    path('teacher_delete/<str:id>',teacher_delete, name='teacher_delete'),    
    path('logout',logoutUser, name='logout'),
    path('error401', error401, name='error401'),
    path('StatisticalReport', StatisticalReport, name='StatisticalReport'),
    path('SectorStatisticalReport', SectorStatisticalReport, name='SectorStatisticalReport'),
    path('ajaxSearch', ajaxSearch, name='ajaxSearch'),
    path('footer', footer, name='footer'),
    path('addCourse', addCourse, name='addCourse'),
    path('addSchool', addSchool, name='addSchool'),
    path('schoolList', schoolList, name='schoolList'),
    path('school_update/<str:pk_school>',school_update, name='school_update'),
    path('school_delete/<str:id>', school_delete, name='school_delete'),
    path('coordinator_update/<str:pk_coordinator>',coordinator_update, name='coordinator_update'),
    path('coordinator_delete/<str:id>', coordinator_delete, name='coordinator_delete'),
    path('testPdf', testPdf, name='testPdf'),
    path('register_coordinator_user', register_coordinator_user, name='register_coordinator_user'),
    path('addStaff', addStaff, name='addStaff'),
    path('register_staff_user', register_staff_user, name='register_staff_user'),
    path('sitesBoardReport', sitesBoardReport, name='sitesBoardReport'),
    path('siteStaffReport', siteStaffReport, name='siteStaffReport'),
    path('siteschoolReport', siteschoolReport, name='siteschoolReport'),
    path('addYear', addYear, name='addYear'),
    path('ListOfYear', ListOfYear, name='ListOfYear'),
    path('addBudget', addBudget, name='addBudget'),
    path('budgetList', budgetList, name='budgetList'),
    path('addMembership', addMembership, name='addMembership'),
    path('membershiptList', membershiptList, name='membershiptList'),
    path('ListOfSiteMembershipFee', ListOfSiteMembershipFee, name='ListOfSiteMembershipFee'),
    path('studentListStaff', studentListStaff, name='studentListStaff'),
    path('globalCumurativeDisability', globalCumurativeDisability, name='globalCumurativeDisability'),
    path('disabilityReportSingleSite', disabilityReportSingleSite, name='disabilityReportSingleSite'),
    path('schoolMembershipReport', schoolMembershipReport, name='schoolMembershipReport'),
    path('siteStaffRole', siteStaffRole, name='siteStaffRole'),
    path('schoolgenderReport', schoolgenderReport, name='schoolgenderReport'),
    path('ageReportSingleSite', ageReportSingleSite, name='ageReportSingleSite'),
    path('siteBeneficiallyList', siteBeneficiallyList, name='siteBeneficiallyList'),
    path('siteParentList', siteParentList, name='siteParentList'),
    path('yearMembershipReport', yearMembershipReport, name='yearMembershipReport'),
    path('yearBudgetReport', yearBudgetReport, name='yearBudgetReport'),


  
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)