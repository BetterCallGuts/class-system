from django.contrib import admin
from Thoth.admin    import final_boss
from .models        import (

  
  Days,

  CashOut,
  )





class FilterClientByTimeAdded(admin.SimpleListFilter):
  
  title          = "وقت الاضافة"
  parameter_name = "Time__added"
  

  def lookups(self, req, model_admin):
    i = CashOut.objects.all()
    
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
    



def build_days():
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


# build_days()


class CashOutAdminStyle(admin.ModelAdmin):
  list_display = ("Amount", "description", "time_added")
  
  search_fields = ("Amount", "description", )
  list_filter   = (
    FilterClientByTimeAdded,
  )




final_boss.register(CashOut, CashOutAdminStyle)




