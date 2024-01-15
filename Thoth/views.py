from django.shortcuts               import render,redirect
from django.http                    import HttpRequest, HttpResponse
from datetime                       import date, datetime
from .models                        import ClintCourses, Client
from django.contrib.auth.decorators import login_required
from django.contrib.messages        import success

def attender(req, pk):
    if req.method == "POST":
          a = True
          ds = ""
          for i in req.POST:
            if a:
              a = False
              continue
            ds += f"{i},"
          
          the_course = ClintCourses.objects.get(pk=pk)
          the_course.Atten = ds
          the_course.save()

          return HttpResponse("<script>window.close()</script>")
    
    
    

    the_course = ClintCourses.objects.get(pk=pk)
    if the_course.Atten is None:
      ds = []
    else:
      ds = the_course.Atten.split(",")[:-1]

    start_date = str(the_course.the_course.start_date).split("-")
    end_date   = str(the_course.the_course.end_date).split("-")

    start_date = [int(x) for x in start_date]
    end_date   = [int(x) for x in end_date]
    temp       = start_date
    start_date = date(*start_date)
    end_date   = date(*end_date)
    
    days       = end_date - start_date
    days       = str(days).split(',')[0].replace('days', "").replace("day", "")
    try:
      days       = int(days)
    except:
      return HttpResponse("<script>window.close()</script>")
    returned_date = []
    try:
      add_month = 0 
      remove_from_days = 0
      temp_2 = temp
      i = 0
      b = 0
      if_in = []
      for g in the_course.the_course.Day_per_week.all():
        if_in.append(g.day)
      while True:
        b+=1
        ch = False
        if temp_2[1 ]+ add_month > 12:
          temp_2[1] = 1
          add_month = 0
          temp_2[0] += 1

        try:
          date_by_num = date(temp_2[0], temp_2[1 ]+ add_month, temp_2[2]+i - remove_from_days)

          sentance = f"{date_by_num} - {date_by_num.strftime('%A')}"
          if sentance in ds:
            ch = True
          if date_by_num.strftime('%A') in if_in:
            returned_date.append({"name": sentance , 'ch':ch})

           
          if end_date == date_by_num:
            break
        
        except ValueError:
          add_month +=1
          
          temp_2[2]  = 0
          remove_from_days = i
        
        i +=1
        
    except ValueError:

        pass


    return render(req, "atten.html", {"data":returned_date})


  


def redirectadmin(req:HttpRequest):
  
  
  return redirect("/Caffe/")





def refresh_clients(req:HttpRequest):
  clients__ = Client.objects.all()
  errors = []
  a = 0
  for i in clients__:
    try:
      i.save()
      a +=1
    except:
      errors.append(i.name)
  
  if len(errors) > 0 :
    success(req, f"Successfully refreshed {a} client and {''.join(errors)} need some modify")
  else:
    success(req, f"Successfully refreshed {a} with no errors  ")
    
  
  return redirect(f"{req.META['HTTP_REFERER']}")


# 
def attend_with_pk_qr(req:HttpRequest, pk):
  
  
  the_student = Client.objects.get(pk=int(pk))
  courses_student_in = ClintCourses.objects.filter(the_client=the_student)
  today = datetime.now()
  today_with_nice_formatte = f"{today.year}-{today.month}-{today.day} - {today.strftime('%A')},"
  # print(today_with_nice_formatte, "this is my version" )
  for i in courses_student_in:
    print(i.Atten)
    if i.Atten is None:
      i.Atten = today_with_nice_formatte

    else:
      i.Atten += today_with_nice_formatte
  success(req, f"Succfully gave {the_student.name} day's attend")
  return redirectadmin(req)









