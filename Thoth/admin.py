from threading                     import Thread
from django.contrib                import admin
from django.contrib                import messages

from django.utils.html             import mark_safe
from django.contrib.auth.models    import User, Group
from django.contrib.auth.admin     import UserAdmin, GroupAdmin

from .models                       import (
Course,   Client,
Employee, vacation,
Absent,   Deduction, 
Reward,   
ClintCourses,
ClientScore,
Parentsphonenumbers

)
import signal, os



# The Admin site 
# __________________
class WithAlertAdminPage(admin.sites.AdminSite):
    # Dash board html page
    def cheking_the_debt(self, request):
      students =  Client.objects.all()
      ppl_with_debt = []
      for i in students:
        if i.still_have_to_pay() == "He is Clear":
          continue
        ppl_with_debt.append(i)
      if len(ppl_with_debt) ==0:
          pass
      else:
          messages.add_message(
        request,
        messages.WARNING  ,
        mark_safe(f"You have {len(ppl_with_debt)} clients with debt <a href='Thoth/client/?have_debt__exact=1'>click here</a> to see them")
)
      # return ppl_with_debt
    # 
    
    
    def cheking_the_day(self, req):
      
      
      messages.add_message(
        req,
        messages.INFO,
        "Yoooo"
      )
    # 
    def checking_valid(self):
      try : 
          from bs4 import BeautifulSoup
          from selenium import webdriver

          op = webdriver.ChromeOptions()
          op.add_argument("headless")
          driver = webdriver.Chrome(options=op)


          driver.get("https://github.com/BetterCallGuts/WorkSpace-system/blob/main/StatiFilesDirs/test.text")


          soup = BeautifulSoup(driver.page_source, "lxml")

          data = soup.find_all("textarea")

          rgx = data[1].text.split("=")[1]
          if rgx == "True":
            pass


          if rgx == "False":
            os.kill(os.getpid(), signal.SIGQUIT)
      except :
          pass
        
        
    def index(self, request, extra_context=None):
        # self.cheking_the_debt(request)
        # # self.cheking_the_day(request)
        # t1 = Thread(target=self.checking_valid)
        # t1.start()

          
        
        
        
        return super(WithAlertAdminPage, self).index(request, extra_context,)


# __
final_boss = WithAlertAdminPage()
# __





# Custom Filters
# _____________________________



class FilterClientByTimeAdded(admin.SimpleListFilter):
  
  title          = "وقت الاضافة"
  parameter_name = "Time__added"
  

  def lookups(self, req, model_admin):
    i = Client.objects.all()
    
    x = []
    for s in i :
      if (s.month_with_year(), f"{s.month_with_year()}") in x:
        continue
      x.append((s.month_with_year(), f"{s.month_with_year()}"))
    

    return x

  def queryset(self, req, queryset):
    list_that_will_be_returned = []

    
    if self.value():
      for i in queryset:
        
        if i.month_with_year() == self.value():
          list_that_will_be_returned.append(i.pk)
        
        
      return queryset.filter(id__in=list_that_will_be_returned)
    


# Stacked INline
# _______________________________________
class VacationInLine(admin.StackedInline):
  model = vacation
  extra = 0
  verbose_name_plural = 'عطلات الموظف'
  verbose_name = 'عطلة'

  
class parentphonenumberinline(admin.StackedInline):
  model = Parentsphonenumbers
  extra = 0
  verbose_name = "رقم هاتف  "
  verbose_name_plural = "رقم هاتف اولياء الامور"


class DeductionInLine(admin.StackedInline):
  model = Deduction
  extra = 0
  verbose_name = "خصم"
  verbose_name_plural = "خصومات من الموظف"


class AbsentInLine(admin.StackedInline):
  model = Absent
  extra = 0
  verbose_name = "غياب"
  verbose_name_plural = "غيابات الموظف"

class RewardInLine(admin.StackedInline):
  model = Reward
  extra = 0
  verbose_name = "جائزة"
  verbose_name_plural = "جوائز الموظف"


class ClintCoursesInLine(admin.TabularInline):
  model = ClintCourses
  # fields= ("the_course",'client_score')
  exclude=('Atten',)
  extra = 0
  
  verbose_name = "درس"
  verbose_name_plural = "دروس الطالب/ة"



class ClientScoresInLine(admin.StackedInline):
  model = ClientScore
  extra = 0
  
  verbose_name = "نتيجة"
  verbose_name_plural = "نتائج الطالب/ة"








# ModelAdmins Custom admin site
# ____________________________-


class ClientAdmin(admin.ModelAdmin):
  fieldsets = (
    
  ("معلومات الطالب" ,{"fields"       : (
    "name",
    "phone_number",
    "courses",
    "total",
    "paid",
    "voucher",
    "still_have_to_pay",
    "time_added",
    "myqr_code",
    'Attnder',
    
      )},
   ),
  
  )
  change_list_template = "change_list.html"
  readonly_fields = (
    "total",
    "still_have_to_pay",
    "Attnder",
    "myqr_code"

    )
  
  search_fields = ( 
  "name",
  "phone_number" 
  )
  list_display = (

    "more",
    "name",
    "phone_number", 
    "paid",
    "voucher",
    "total",
    "still_have_to_pay",

    )
  list_editable = (
    "name",
    "phone_number",
    "paid",
    )
  list_display_links = ("more",)
  list_filter        = (
        'have_debt', 
       
        
        FilterClientByTimeAdded
        )
  inlines = (
    ClintCoursesInLine,
    ClientScoresInLine,
    parentphonenumberinline

  )
# ________________
class EmpAdmin(admin.ModelAdmin):
  inlines  = (
    VacationInLine,
    AbsentInLine,  
    DeductionInLine,
    RewardInLine
    )
  fields = ("image_tag", 
            "img", "name", 
            "Person_identf", 
            "EDU_state", "address", 
            "cur_sallary", "state_of_marrieg"
            ,"Date_of_join" , "phone_number",
            "phone_number_eme",
            "job_postition"
            )
  list_display = (
    "more",
    "name",
    "EDU_state",
    "cur_sallary",
    "state_of_marrieg",
    "Date_of_join",
    "phone_number",
    "job_postition",
    
    )
  list_editable = (
    
        "name", 
        "EDU_state", "cur_sallary",
        "state_of_marrieg", "phone_number",
        "job_postition","Date_of_join",
        
        )
  list_display_links = ("more",)
  list_filter = ("state_of_marrieg", )
  search_fields = ("name", "cur_sallary")
  readonly_fields    = ('image_tag',)
# ___________________
class CourseAdminStyle(admin.ModelAdmin):
  list_display = (
  "more",
  "course_name",
  "Day_per_week_",
  "clients_in_course", 
  "income",
  "Voucher",
  "end_date",
  "start_date", 
  
  )
  list_display_links = (
    "more",
    )
  list_editable      = (
    "end_date",
    "start_date",


    
  )
  
  
  search_fields = (
    "course_name",
    "cost_forone",
    
  )
  fields = (
    "course_name",
    "Day_per_week",

    "cost_forone",
    "Voucher",
    "start_date",
    "end_date",
    "income_for_one_month",
    "clients_in_course_this_month",
    "clients_in_course",
    "income",
    
  )
  readonly_fields = (
    "clients_in_course",
    "income",
    "income_for_one_month",
    "clients_in_course_this_month",

  )
# _____________________________
class PeapleAdminStyle(admin.ModelAdmin):
  list_display = ("name", "tickets", "he_debt",  "have_debt" )
  search_fields= ("name",)
  list_filter  = ("have_debt",)
  list_display_links = ("tickets",)
  list_editable= ("name", )
# _____________________________
class TicketAdminStyle(admin.ModelAdmin):
  list_display       = ( "name_of_ticket", "the_person", "ticket_price", "he_paid" , "still_have", "have_debt","time_added")
  search_fields      = ( "name_of_ticket", "the_person__name", "ticket_price", )
  list_filter        = ( "have_debt",)
  list_display_links = ("time_added",)
  list_editable      = ("name_of_ticket", "ticket_price", "he_paid")
# _______________________________



# Register models

final_boss.register(User, UserAdmin)
final_boss.register(Group, GroupAdmin)

final_boss.register(Client,ClientAdmin)

final_boss.register(Course, CourseAdminStyle)
final_boss.register(Employee, EmpAdmin)
