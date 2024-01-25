from django.db import models
from datetime import datetime





class Days(models.Model):
  
  day = models.CharField(max_length=255, verbose_name="Day Name")
  
  def __str__(self):
    return f"{self.day}"


class CashOut(models.Model):
  Amount      = models.IntegerField(verbose_name="مقدار السعر")
  description = models.TextField(blank=True, null=True, verbose_name="الوصف") 
  time_added  = models.DateField(auto_now_add=datetime.now, editable=False, verbose_name="وقت الاضافة")
  def month_with_year(self):
    
    

    return "-".join(str(self.time_added).split('-')[:-1])
  class Meta:
    verbose_name = 'تكلفة'
    verbose_name_plural = "تكاليف المكان"
  
  def __str__(self):
    
    return f"{self.Amount}|{self.time_added}"


