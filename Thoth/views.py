from django.shortcuts               import render,redirect
from django.http                    import HttpRequest, HttpResponse
from datetime                       import date, datetime
from .models                        import  Client, ClientCourseRel, Course

from django.contrib.messages        import success, error
from django.utils.html              import mark_safe
from django.urls                    import reverse


def attender(req, pk):
    if req.method == "POST":
          a = True
          ds = ""
          for i in req.POST:
            if a:
              a = False
              continue
            ds += f"{i},"
          
          the_course = ClientCourseRel.objects.get(pk=pk)
          the_course.attend = ds
          the_course.save()

          return HttpResponse("<script>window.close()</script>")
    
    
    

    the_course = ClientCourseRel.objects.get(pk=pk)
    if the_course.attend is None:
      ds = []
    else:
      ds = the_course.attend.split(",")[:-1]

    start_date = str(the_course.course.start_date).split("-")
    end_date   = str(the_course.course.end_date).split("-")

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
      for g in the_course.course.Day_per_week.all():
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
  courses_student_in = ClientCourseRel.objects.filter(client=the_student)
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













def attend_grid(req, pk):
    the_course = Course.objects.get(pk=pk)
    
    rel_in = ClientCourseRel.objects.filter(course=the_course)
    
    
    
    
    if req.method == "POST":
            a = True
            ds = ""
            
            studentss = Client.objects.all()
            for i in studentss:
              ds = ""
              for k in req.POST:
                
                if i.name in k:
                    #  name = k.split("$")[1]
              
                    day  = k.split("$")[0].replace("|","-")
                    ds += f"{day},"
              try:

                rel = ClientCourseRel.objects.get(client=i,course=the_course)
                rel.attend = ds
                rel.save()
              except:
                pass
                
            
            
            
            return HttpResponse("<script>window.close()</script>")
      
    first__ = True
    returned_date = []
    for s in rel_in:

      the_course = s
      if the_course.attend is None:
        ds = []
      else:
        ds = the_course.attend.split(",")[:-1]

      student_list = []
      
      start_date = str(the_course.course.start_date).split("-")
      end_date   = str(the_course.course.end_date).split("-")
      start_date = [int(x) for x in start_date]
      end_date   = [int(x) for x in end_date]
      temp       = start_date
      start_date = date(*start_date)
      end_date   = date(*end_date)
      
      days       = end_date - start_date
      days       = int(str(days).split(',')[0].replace('days', "").replace("day", ""))
      
      try:
        add_month = 0 
        remove_from_days = 0
        temp_2 = temp
        i = 0
        b = 0
        if_in = []
        for g in the_course.course.Day_per_week.all():
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

            sentance = f"{date_by_num} | {date_by_num.strftime('%A')}"
            if f"{date_by_num} - {date_by_num.strftime('%A')}" in ds:
              ch = True
            if date_by_num.strftime('%A') in if_in:
              student_list.append({"name": sentance , 'ch':ch, })

            
            if end_date == date_by_num:
              if first__:
                first__ = False

                p  = []
                for i in student_list:
                  temp_3 = i["name"]
                  i["name"] = i['name'].split("|")[0] +"<br>" +i['name'].split("|")[1][0:3] 
                  p.append( mark_safe(i['name']))
                  i['name'] = temp_3

                returned_date.append([p])

              returned_date.append([student_list, s.client.name, s.client.pk])
              break
          
          except ValueError:
            add_month +=1
            
            temp_2[2]  = 0
            remove_from_days = i
          
          i +=1
          
      except ValueError:

          pass
    

  # 
    return render(req, "attend__system.html", {'data' : returned_date, "stu" : returned_date[1:]})


def attend_all_students_with_qr_scanner(req:HttpRequest):
  
  
  if req.method == "POST":
    data = req.POST.get("pk_for_student", None)
    if data is not None:
      try:
        
        current_client           = Client.objects.get(pk=int(data))
      except:
        error(req, "كود الطالب خاطئ او الطالب غير مسجل")
        return render(req,"attend_all_students_with_qr_scanner.html" )

      courses_client_in        = ClientCourseRel.objects.filter(client=current_client)
      today                    = datetime.now()
      today_in_list_formate    = str(today).split("-")
      today_in_list_formate[2] = today_in_list_formate[2][0:2]
      today_in_list_formate    = [int(x) for x in today_in_list_formate]
      today                    = date(*today_in_list_formate)
      if today.month < 10 :
        month = f"0{today.month}"
      else:
        month = today.month
      today_with_nice_formatte = f"{today.year}-{month}-{today.day} - {today.strftime('%A')},"
      for i in courses_client_in :
        if i.attend is None:
          i.attend = today_with_nice_formatte
          i.save()
        
        else:
          if today_with_nice_formatte in i.attend:
            pass
          else:
            i.attend += today_with_nice_formatte
            i.save()
      
      success(req, mark_safe(f"لقم تم تسجيل حضور الطالب <a href='/Caffe/Thoth/client/{current_client.pk}/change/'>{current_client.name}</a> لهذا الدرس"))
      
      

  
  return render(req,"attend_all_students_with_qr_scanner.html" )