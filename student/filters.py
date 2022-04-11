import django_filters
from django_filters import DateFilter,CharFilter

from .models import *

class StudentFilter(django_filters.FilterSet):
    f_name = CharFilter(field_name="f_name", lookup_expr='icontains')
    year_reg = CharFilter(field_name="year_reg", lookup_expr='icontains')
    # start_date = DateFilter(field_name="dob", lookup_expr='gte')
    # end_date = DateFilter(field_name="dob", lookup_expr='lte')
    class Meta:
         model = Student
         fields = '__all__'
         exclude = ['year_reg','l_name','dob', 'service_category', 'st_image']

class TeacherFilter(django_filters.FilterSet):
    f_name = CharFilter(field_name="f_name", lookup_expr='icontains')
    # year_reg = CharFilter(field_name="year_reg", lookup_expr='icontains')
    # start_date = DateFilter(field_name="dob", lookup_expr='gte')
    # end_date = DateFilter(field_name="dob", lookup_expr='lte')
    class Meta:
         model = Teacher
         fields = '__all__'
         exclude = ['year_reg','l_name','dob','start_date']