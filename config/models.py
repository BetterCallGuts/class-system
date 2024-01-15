from django.db import models
from datetime import datetime


class JobPosition(models.Model):
  
  job_title =  models.CharField(max_length=300, verbose_name="اسم المنصب الوظيفي")
  
  
  class Meta:
    verbose_name = "منصب وظيفي"
    verbose_name_plural = "المناصب الوظيفية"
  
  def __str__(self):
    
    return f"{self.job_title}"
  



class Days(models.Model):
  
  day = models.CharField(max_length=255, verbose_name="Day Name")
  
  def __str__(self):
    return f"{self.day}"

class CourseGroup(models.Model):
  name = models.CharField(max_length=255, verbose_name="اسم الفئة")
  
  
  class Meta:
    verbose_name = "فئة"
    verbose_name_plural = "الفئات"
  def __str__(self):
    
    return f"{self.name}"
  


class CashOut(models.Model):
  Amount      = models.IntegerField(verbose_name="مقدار السعر")
  description = models.TextField(blank=True, null=True, verbose_name="الوصف") 
  time_added  = models.DateField(auto_now_add=datetime.now, editable=False, verbose_name="وقت الاضافة")
  
  class Meta:
    verbose_name = 'تكلفة'
    verbose_name_plural = "تكاليف المكان"
  
  def __str__(self):
    
    return f"{self.Amount}|{self.time_added}"



class PaymentMethod(models.Model):
  Paymentname = models.CharField(verbose_name="اسم الطريقة", max_length=255)

  class Meta:
    verbose_name = "طريقة الدفع"
    verbose_name_plural = "طرق الدفع"
  def __str__(self):
    
    return f"{self.Paymentname}"
    
  