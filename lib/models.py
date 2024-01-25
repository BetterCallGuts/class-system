from django.db import models
from datetime  import datetime, date



class Library(models.Model):
  
  name = models.CharField(max_length=255, verbose_name="اسم المكتبة", blank=True, null=True)
  desc = models.TextField(blank=True, null=True, verbose_name="مواصفات المكتبة/عنوانها")

  def __str__(self):
    return f"{self.name}"


  class Meta:
    verbose_name = "مكتبة"
    verbose_name_plural = "المكاتب"
    
  def total_lib_charges(self):
    charegs  = LibraryCharges.objects.filter(library=self)
    total    = 0 
    for i in charegs :
      total += i.amount
    
    return total
  
  def total_lib_charges_this_month(self):
    charegs  = LibraryCharges.objects.filter(library=self)
    total    = 0
    start    = date(datetime.now().year, datetime.now().month, 1)
    end      = date(datetime.now().year, datetime.now().month, datetime.now().day)
    for i in charegs:
      
      if start <i.time_ad <end:
        total += i.amount

    return total

  
  total_lib_charges.short_description            = "اجمالي فواتير المكتبة"
  total_lib_charges_this_month.short_description = "فواتير المكتبة من بداية هذا الشهر"


class LibraryCharges(models.Model):
  library = models.ForeignKey(Library, on_delete=models.CASCADE, blank=True, verbose_name="المكتبة")
  amount  = models.FloatField(verbose_name ="قيمة الفاتورة")
  descri  = models.TextField(verbose_name="سبب الفاتورة", blank=True)
  time_ad = models.DateField(verbose_name="وقت اضافة الفاتورة", editable=False, default=datetime.now)
  
  
  # 
  class Meta:
    verbose_name        = "فاتورة المكتبة"
    verbose_name_plural = "فواتير المكتبات"
  def __str__(self):
    return f"{self.time_ad}"