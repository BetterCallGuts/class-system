from django.contrib import admin
from Thoth.admin    import final_boss
from .models        import (

  
  Days,

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





class CashOutAdminStyle(admin.ModelAdmin):
  list_display = ("Amount", "description", "time_added")
  




final_boss.register(PaymentMethod)

final_boss.register(CashOut, CashOutAdminStyle)




