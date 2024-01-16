from django.db   import           models

import                            datetime
from django.utils.timezone import now

import                            uuid
import                            os
from django.utils.html import     mark_safe

from django.urls import reverse
import qrcode
from django.urls import reverse

# GLobal Vars

# Models
# ________________________


class Parentsphonenumbers(models.Model):
  
  name         = models.CharField(max_length=255, verbose_name="اسم صاحب الرقم")
  phone_number = models.CharField(max_length=255, verbose_name="رقم الهاتف")
  client       = models.ForeignKey("Client",on_delete=models.SET_NULL ,null=True, blank=True)

  def __str__(self):
    return f"{self.name}"
  class Meta:
    verbose_name = "رقم ولي الأمر"
    verbose_name_plural = "ارقام أولياء الأمور"
class Course(models.Model):
  # 
  course_name = models.CharField(max_length=255, verbose_name="اسم الدرس")
  start_date  = models.DateField(default=datetime.datetime.now ,verbose_name="بداية الدرس")

  end_date    = models.DateField(default=datetime.datetime.now, verbose_name="نهاية الدرس")
  cost_forone = models.FloatField(blank=True, default=0, verbose_name="سعر الدرس للفرد الواحد")
  Day_per_week= models.ManyToManyField("config.Days", related_name="Days", blank=True,verbose_name="كم يوما فلأسبوع")
  Voucher     = models.FloatField( blank=True, default=0, verbose_name=" تكلفة الدرس على الاستاذ")


  # 
  
  def save(self):
    super().save()
    if self.Voucher == None:
      self.Voucher = 0
    if self.cost_forone == None:
      self.cost_forone = 0
    super().save()
  
  def __str__(self):
    return f"{self.course_name}"
  # 
  
  
  def income(self):
    pple  = float(self.clients_in_course())
    pple_in_course = ClintCourses.objects.filter(the_course=self)
    result =  ((pple) * self.cost_forone) - self.Voucher
    dont_repeat = []
    for i in pple_in_course:
      if i not in dont_repeat:
        result -= i.the_client.voucher
        dont_repeat.append(i)

    return result
  def lll(self):
    result = 3
    return result

  def income_for_one_month(self):
    pple  = float(self.clients_in_course_this_month())
    
    pple_in_course = ClintCourses.objects.filter(the_course=self)
    
    result =  ((pple) * self.cost_forone) - self.Voucher
    dont_repeat = []


    for i in pple_in_course:
      if i not in dont_repeat:
          result -= i.the_client.voucher
          dont_repeat.append(i)

    return result
  
  # 
  
  def more(self):
    return "المزيد"
  # 
  def clients_in_course(self):
    pple = ClintCourses.objects.filter(the_course=self)
    return f"{len(pple) }"
  def clients_in_course_this_month(self):
    pple = ClintCourses.objects.filter(the_course=self)
    start= datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, 1)
    end  = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
    l    = []
    for i in pple:
      if start <= i.date_for <= end:
        l.append(i)
    return f"{len(l) }"


  def Day_per_week_(self):
    days = self.Day_per_week.all()
    se = []
    for i in days:
      se.append(i.day)
    if len(se) == 0:
      return "لم تقم بوضع الايام"
    
    return ", ".join(se)

  clients_in_course.short_description = "عدد طلاب الدرس"
  income.short_description = "ارباح الدرس"
  income_for_one_month.short_description = "الارباح لهذا الشهر"
  clients_in_course_this_month.short_description = "عدد طلاب الدرس هذا الشهر"
  more.short_description = "انقر للمزيد"

  class Meta:
    verbose_name = 'الدرس'
    verbose_name_plural = "الدروس"
  
class Client(models.Model):
  # 
  name           = models.CharField(max_length=255, verbose_name="اسم الطالب/ة")
  phone_number   = models.CharField(max_length=255, verbose_name="رقم الهاتف")
  paid           = models.IntegerField(default=0, blank=True, verbose_name="المبلغ الذي تم دفعة")
  have_debt      = models.BooleanField(default=True, verbose_name="مدين؟")
  courses        = models.ManyToManyField(Course, verbose_name="الدروس", blank=True, )
  voucher        = models.FloatField(default=0, blank=True, verbose_name="الخصومات")
  time_added     = models.DateField(default=datetime.datetime.now,  verbose_name="وقت اضافة الطالب",)
  myqr           = models.ImageField(upload_to="clientqrcodes", blank=True, editable=False,)
  def month_with_year(self):
    
    

    return "-".join(str(self.time_added).split('-')[:-1])
  # 
  def total(self):
    result= 0
    for i in self.courses.all():

        result += i.cost_forone
    if self.voucher == 0 or self.voucher == None:
      
      return result
    
    return  result - self.voucher
  # 
  def myqr_code(self):
    
    if self.myqr== "" and self.pk is not None:
      res = qrcode.make(reverse("attend-with-pk",args=[self.pk]))
      
      res.save(f"mediaRoot/clientqrcodes/{self.name}|{self.pk}.png")
      
      self.myqr = f"clientqrcodes/{self.name}|{self.pk}.png"
      self.save()
    
    return mark_safe(f"<img alt='student qrcode' style='width:300px;height:300px;' src='{self.myqr.url}' />")
  # 
  def more(self):
    return "المزيد"
  # 
  
  def still_have_to_pay(self):
    still_didt_pay = float(self.total()) - float(self.paid)
    if still_didt_pay <= 0 :
      return "خالص"
    return still_didt_pay

  def __str__(self):
    return f"{self.name}"
  # 
  def save(self):
    if self.paid == None:
      self.paid  =0
    super().save()
    if self.still_have_to_pay() == "خالص":
      self.have_debt = False
    else:
      self.have_debt = True
    super().save()
  # 
  class Meta:
    verbose_name = "الطالب/ة"
    verbose_name_plural = "الطلاب"
  # 
  def save_model(self, request, obj, form, changed):
    if '_continue' in request.POST:
        if self.paid == None:
          self.paid  =0
        super().save()
        if self.still_have_to_pay() == "خالص":
          self.have_debt = False
        else:
          self.have_debt = True
        super().save()
    return super().change_view(request, obj, form, changed)
  # 
  still_have_to_pay.short_description = "متبقي للدفع"
  total.short_description = "المبلغ الكلي"
  more.short_description   = "انقر للمزيد"
  
  def Attnder(self):
    my_ = ClintCourses.objects.filter(the_client=self)

    div = '''
    
    <div>
    
          '''
    
    for i in my_:

      try:
        
        days = i.Atten.split(',')
      except:
        days = None
      

        days_html = f"""
      <hr>
      <h2>
        {i.the_course.course_name}
      </h2> 
      <a 
        href='{reverse("attend",args=(i.pk,))}' 
        target='popup'
        >
          Edit it
        </a>
        <br>
        You havn't set it up yet  
        <hr
        > <br>"""
     
      

      if days is not None:
        the_cours_name = i.the_course.course_name
        days_html = f''' 
        
        <hr>
        <h2>
        {the_cours_name}
        </h2>
        <a 
        href='{reverse("attend",args=(i.pk,))}' 
        target='popup'
        >
          Edit it
        </a>
        '''
        for m in days:
          days_html += f"<p> {m}</p>"

        days_html += '<hr>'
        days_html = mark_safe(days_html)

      div += mark_safe(days_html)
    
  
    div += mark_safe("</div>")
    div += mark_safe( ''' 
          <script>
    links = document.querySelectorAll('a[target=popup]');
    
    for ( link of links) {
        link.addEventListener('click', ()=>{
            window.open(link.getAttribute("href"), 'popup',' width=600,height=600'); return false; 
        }) 
    }
          </script>''')
    return mark_safe(div) 
  Attnder.short_description = "الحضور"
  myqr_code.short_description = "كود الطالب"

class ClientScore(models.Model):
  the_client   = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
  the_course   = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name="الدرس")
  client_score = models.IntegerField(verbose_name="درجة الطالب/ة")
  max_score = models.IntegerField(verbose_name = "الدرجة النهائية")
  
  def __str__(self):
    return f"{self.the_client.name}"
  class Meta:
    verbose_name = "نتيجة الطالب"
    verbose_name_plural = "نتائج الطلاب"
class ClintCourses(models.Model):
  
  the_course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="اسم الدرس")
  the_client = models.ForeignKey(Client, on_delete=models.CASCADE,)

  Atten      = models.TextField(blank=True, null=True)
  date_for   = models.DateField( default=datetime.datetime.now, editable=False)

  class Meta:
    
    verbose_name        = "درس الطالب"
    verbose_name_plural = "دروس الطلاب"
  def __str__(self):
    return f"{self.the_course}"


class vacation(models.Model):
  
  choices = (
    ("Sick leave", "مرضي"),
    ("weekends", "اعتيادي")    ,
    
  )
  Emp           = models.ForeignKey("Employee", on_delete=models.CASCADE, )
  vacation_type = models.CharField(choices=choices, max_length=300, verbose_name="نوع الاجازة") 
  how_many_days = models.IntegerField(verbose_name="عدد ايام الاجازة",default=0 )
  # 
  def __str__(self):
    return f"{self.Emp.name}"
  class Meta:
      verbose_name = "اجازة الموظف"
      verbose_name_plural = "اجازات الموظفين"
  # 

class Absent(models.Model):
  # 
  Emp           = models.ForeignKey("Employee", on_delete=models.CASCADE)
  how_many_days = models.IntegerField(verbose_name="عدد الأيام") 
  Reson         = models.TextField(verbose_name="السبب", blank=True, default=" ")
  # 
  def __str__(self):
    return f"{self.how_many_days} يوم"
  # 
  class Meta:

    verbose_name = 'غياب الموظف'
    verbose_name_plural = "غيابات الموظف"

class Deduction(models.Model):
  # 
  Emp        = models.ForeignKey("Employee", on_delete=models.CASCADE)
  The_amount = models.IntegerField(verbose_name="المقدار")
  the_reson  = models.TextField(null=True, blank=True, verbose_name="السبب")
  # 
  
  class Meta:

    verbose_name = "خصم من الموظف"  # 
    verbose_name_plural = "خصومات الموظفين"
  def __str__(self):
    return f"{self.The_amount}"


class Reward(models.Model):
  # 
  Emp        = models.ForeignKey("Employee", on_delete=models.CASCADE)
  The_amount = models.IntegerField(verbose_name="المقدار")
  the_reson  = models.TextField(null=True, blank=True, verbose_name="السبب")
  img        = models.ImageField(verbose_name="صورة لشهادة(اختياري)", blank=True)
  # 
  class Meta:
    verbose_name = "جائزة للموظف"
    verbose_name_plural = 'جوائز الموظفين'
  # 
  def __str__(self):
    return f"{self.The_amount}"




class Employee(models.Model):
  # 
  choices = (
    ("Married" , "متزوج" ),
    ("Single"  , "اعزب")  ,
    ("Divorced", "مطلق"),
    ("Widower" , "ارمل") ,
  )
  name             = models.CharField(max_length=255, verbose_name="اسم الموظف")
  Person_identf    = models.CharField(max_length=255, default=" ",verbose_name="الرقم القومي", null=True, blank=True, ) 
  EDU_state        = models.CharField(max_length=300, default=" ", null=True, blank=True, verbose_name="المستوى التعليمي") 
  address          = models.CharField(max_length=300, default=" ", null=True, blank=True, verbose_name="العنوان") 
  img              = models.ImageField(upload_to="EMP Pic", verbose_name=" ", blank=True)
  cur_sallary      = models.FloatField(verbose_name="راتب شهري") 
  Date_of_join     = models.DateField(default=datetime.datetime.now, verbose_name="تاريخ الانضمام")
  state_of_marrieg = models.CharField(choices=choices, verbose_name="الحالة الاجتماعية", max_length=300)
  phone_number     = models.CharField(max_length=20, verbose_name="رقم الهاتف", blank=True, null=True)
  phone_number_eme = models.CharField(max_length=20, verbose_name="رقم الهاتف فحالة طارئة", blank=True, null=True)
  job_postition    = models.CharField(max_length=255, null=True,blank=True, verbose_name="المنصب الوظيفي")
  more             = models.CharField(editable=False, default="المزيد",max_length=10)
  # 
  def image_tag(self):
    return mark_safe(f'<img style="width:200px;hieght:200px" src="{ self.img.url}" />' )
  # 
  def __str__(self):
    return f"{self.name}"
  # 
  class Meta:
    verbose_name = "موظف"
    verbose_name_plural = "الموظفين"
  
  image_tag.short_description = 'صورة الموظف'
  image_tag.allow_tags = True



# 
