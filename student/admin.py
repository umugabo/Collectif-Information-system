from django.contrib import admin
from .models import Classe, Student, Course, School, Sector ,Teacher, Parent, Coordinator , Board , Staff , Admin , Province , District , Sectors , Cell , Village, Membership, Year, Budget


# Register your models here.
admin.site.register(Classe),
admin.site.register(Student),
admin.site.register(Course), 
admin.site.register(School),
admin.site.register(Sector), 
admin.site.register(Teacher), 
admin.site.register(Parent),
admin.site.register(Coordinator),
admin.site.register(Board),
admin.site.register(Staff),
admin.site.register(Admin),
admin.site.register(Province),
admin.site.register(District),
admin.site.register(Sectors),
admin.site.register(Cell),
admin.site.register(Village),
admin.site.register(Membership),
admin.site.register(Year),
admin.site.register(Budget),

# Admin Title
admin.site.site_header = "COLLECTIF INFORMATION SYSTEM ADMNIN PANEL"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcome To Collectif System Admin Area"


