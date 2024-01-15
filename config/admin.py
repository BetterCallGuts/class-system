from django.contrib import admin
from Thoth.admin    import final_boss
from .models        import (
  JobPosition,
  
  Days,
  CourseGroup,
  CashOut,
  PaymentMethod
  )



try:
  days  = Days.objects.all()
  a = 0

  for i in days:
    a += 1


  if a == 7:
    pass
  else:
    days  = [
      "Monday", "Tuesday", "Wednesday", "Thursday",
      "Friday", "Saturday", "Sunday"
      
            ]
    for i in days:
      b = Days.objects.create(day=i)
      b.save()
except :
  pass



class JobPosAdminStyle(admin.ModelAdmin):
  
  list_display  = ("job_title",)
  search_fields= ("job_title",)

class CashOutAdminStyle(admin.ModelAdmin):
  list_display = ("Amount", "description", "time_added")


final_boss.register(JobPosition, JobPosAdminStyle)

final_boss.register(PaymentMethod)
final_boss.register(CourseGroup)
final_boss.register(CashOut, CashOutAdminStyle)




