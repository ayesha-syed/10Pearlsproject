
from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from django.shortcuts import redirect
from .models import *
from django.urls import reverse
from json import dumps
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.contrib.sessions.models import Session
from random import seed
from random import randint
from datetime import date,datetime

# Create your views here.

def landingpage(request):
    try:                                    # To see if redirect is from admin signup page
    
        em=request.session['A_Email']       #This value was saved in session/cache when admin signed up
        p=request.session['Password']       #This value was saved in session/cache when admin signed up
        f=request.session['f_Name']         #This value was saved in session/cache when admin signed up
        l=request.session['l_Name']         #This value was saved in session/cache when admin signed up
        s=request.session['done']           # if redirect is from admin signup page
        form=admin_signup_form()
        obj = form.save(commit=False)
        obj.email=em
        obj.first_Name=f
        obj.last_Name=l
        obj.password=p
        obj.save()                          # save the credentials of the admin that just signed up into the admin table
        Session.objects.all().delete()      #delete admin credentials(that was saved when they signed up) from cache/session
        return render(request,'landingpage.html',{'logged_in':False})  #render  landingpage after admin signup
    except:  #if no redirection was done(first time loading the page/refreshing the page)
        Session.objects.all().delete()
        return render(request,'landingpage.html',{'logged_in':False})


def candidate_login(request):
    form=candidate_login_form(request.POST or None,request.FILES or None)
    if request.method == "POST":                #if a post request is made by the  user
            name=request.POST["username"]       #get username from post request that user made by clicking login button
            password=request.POST["password"]   #get password from post request that user made by clicking login button
            try:
                checkname=Candidate.objects.get(username=name)   #check if username exist in the candidate table
                if checkname.password==password:                 #if user credentials that were entered matches an instance in the candidate table
                    request.session['C_username']=name           #save username in session/cache to keep track of the current user that has logged in 
                    form=candidate_login_form()
                    return redirect('complete_candidate_info')   #redirect to complete candidate information page
                else:                               #if entered username matches the username of an instance in the candidate table but passwords doesn't match
                    form=candidate_login_form()
                    context={'form':form,'invalid_input':True,'logged_in':False}    
                    return render(request,"candidate_login.html",context)  #render login page again but with invalid credentials alert
            except :   #if entered username doesn't match with any username in the candidate table
                form=candidate_login_form()
                context={'form':form,'invalid_input':True,'logged_in':False}
                return render(request,"candidate_login.html",context)  #render login page again but with invalid credentials alert
    else:    #if post request was not made by the user(first time loading the page/refreshing the page)
        context={'form':form,'invalid_input':False,'logged_in':False}
        return render(request,"candidate_login.html",context)



def candidate_signup(request):
    if 'A_email' in request.session:  #if admin email address is in session/cache. This is done to make sure this page is accessed by a legitimate admin that has logged in successfully
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            form=candidate_signup_form(request.POST or None,request.FILES or None)
            if request.method == "POST":  # if post request is made by the candidate 
                val=EmailValidator()   # To check the validity of the entered email address
                if request.POST['Position']!='' and request.POST["email"]!= '' and request.POST["password"]!='' and request.POST["username"]!='':  #To make sure non of the fields was left empty
                    try:
                        ss=val(request.POST["email"])   #validating email address
                        if (Candidate.objects.filter(email=request.POST["email"]).exists() or Admin.objects.filter(email=request.POST["email"]).exists()) : #if entered email address matches an email address in either the admin table or the candidate table
                            form=candidate_signup_form()
                            context={'form':form,'email_exists':True,'invalid_input':False,'invalid_email':False,'logged_in':True,'username':username,'username_exist':False}
                            return render(request,"candidate_signup.html",context)  #render candidate page again with  "email already exists" alert
                        elif (Candidate.objects.filter(username=request.POST["username"]).exists()):
                            form=candidate_signup_form()
                            context={'form':form,'email_exists':True,'invalid_input':False,'invalid_email':False,'logged_in':True,'username':username,'username_exist':True}
                            return render(request,"candidate_signup.html",context)  #render candidate page again with  "email already exists" alert
                        else:    # if entered email address is unique
                            form.save()    #save form
                            request.session['new_user']=request.POST["email"] #to indicate that a new user was added by the current admin on setup interview page
                            return redirect('create_interview')   #return to landing page
                    except:   #if email validation failed
                        form=candidate_signup_form()
                        context={'form':form,'email_exists':False,'invalid_input':False,'invalid_email':True,'logged_in':True,'username':username,'username_exist':False}
                        return render(request,"candidate_signup.html",context)  #render candidate page again with invalid email address alert
                else:  #if some or all of the fields were left blank
                    form=candidate_signup_form()
                    context={'form':form,'email_exists':False,'invalid_input':True,'invalid_email':False,'logged_in':True,'username':username,'username_exist':False}
                    return render(request,"candidate_signup.html",context) #render candidate page again with invalid input address alert
            else:    #if post request was not made by the user(first time loading the page/refreshing the page) 
                return render(request,'candidate_signup.html',{'form':form,'logged_in':True,'username':username,'username_exist':False})
        else:
            return redirect('landingpage')
    else:
        return redirect('landingpage')

def complete_candidate_info(request):
    if 'C_username' in request.session:   #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        s=Candidate.objects.get(username=request.session['C_username'])  #fetch the info of current user
        if (s.first_Name==None):   #if first_Name=None means that candidate is a new user and they haven't provided their complete info yet
            if request.method == "POST":  #if post request is made by the candidate
                form=complete_candidate_form(request.POST ,instance=s)  #creating a form with prefilled fields(certain fields are prefilled using the info of candidate fetched from the candidate table)
                if request.POST['first_Name']!='' and request.POST['last_Name']!='' and request.POST["username"]!= '' and request.POST["password"]!='': #To make sure non of the fields was left empty
                    if (Candidate.objects.filter(username=request.POST["username"]).exists() ) :  #if entered username matches the username of an instance in the candidate table
                        val=Candidate.objects.get(username=request.POST["username"]) #fetch info of the instance whose username matched with the entered username
                        if val.id!=s.id:    #if mached username belongs to two different candidates
                            form=complete_candidate_form(instance=s)
                            context={'form':form,'username_exists':True,'invalid_input':False}
                            return render(request,"complete_candidate_info.html",context) #render page again with "username exists" alert
                        else:                            
                            if form.is_valid():   #checking if form is valid
                                form.save()       #save form
                                request.session['C_username']=request.POST["username"]  #save the entered username in the session/cache(this is done so that if candidate change their username, it is updated in the cache/session) 
                                return redirect('candidate_panel')   # redirect to candidate panel
                    else:                         #if entered username doesn't match any username in the candidate table
                            if form.is_valid():  #checking if form is valid
                                form.save()   #save form
                                request.session['C_username']=request.POST["username"]  #save the entered username in the session/cache(this is done so that if candidate change their username, it is updated in the cache/session) 
                                return redirect('candidate_panel')  # redirect to candidate panel
                else:  #if one or more fields were left empty in the form
                    form=complete_candidate_form(instance=s)
                    context={'form':form,'username_exists':False,'invalid_input':True}
                    return render(request,"complete_candidate_info.html",context)   #render same page with invalid input alert
            else:    #if post request was not made by the user(first time loading the page/refreshing the page)
                form=complete_candidate_form(instance=s)
                context={'form':form,'username_exists':False,'invalid_input':False}
                return render(request,"complete_candidate_info.html",context)
        else:  #if candidate is not new to the portal
            return redirect('candidate_panel')
    else:  #if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')

def candidate_editprofile(request):
    if 'C_username' in request.session:   #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        if request.session['C_username']!='':
            s=Candidate.objects.get(username=request.session['C_username'])  #fetch the info of current user
            if request.method == "POST":  #if post request is made by the candidate
                form=complete_candidate_form(request.POST ,instance=s)  #creating a form with prefilled fields(certain fields are prefilled using the info of candidate fetched from the candidate table)
                if request.POST['first_Name']!='' and request.POST['last_Name']!='' and request.POST["username"]!= '' and request.POST["password"]!='': #To make sure non of the fields was left empty
                    if (Candidate.objects.filter(username=request.POST["username"]).exists() ) :  #if entered username matches the username of an instance in the candidate table
                        val=Candidate.objects.get(username=request.POST["username"]) #fetch info of the instance whose username matched with the entered username
                        if val.id!=s.id:    #if mached username belongs to two different candidates
                            form=complete_candidate_form(instance=s)
                            context={'form':form,'username_exists':True,'invalid_input':False,'logged_in':True,'username':request.session['C_username']}
                            return render(request,"candidate_editprofile.html",context) #render page again with "username exists" alert
                        else:                            
                            if form.is_valid():   #checking if form is valid
                                form.save()       #save form
                                request.session['C_username']=request.POST["username"]  #save the entered username in the session/cache(this is done so that if candidate change their username, it is updated in the cache/session) 
                                return redirect('candidate_panel')   # redirect to candidate panel
                    else:                         #if entered username doesn't match any username in the candidate table
                            if form.is_valid():  #checking if form is valid
                                form.save()   #save form
                                request.session['C_username']=request.POST["username"]  #save the entered username in the session/cache(this is done so that if candidate change their username, it is updated in the cache/session) 
                                return redirect('candidate_panel')  # redirect to candidate panel
                else:  #if one or more fields were left empty in the form
                    form=complete_candidate_form(instance=s)
                    context={'form':form,'username_exists':False,'invalid_input':True,'logged_in':True,'username':request.session['C_username']}
                    return render(request,"candidate_editprofile.html",context)   #render same page with invalid input alert
            else:    #if post request was not made by the user(first time loading the page/refreshing the page)
                form=complete_candidate_form(instance=s)
                context={'form':form,'username_exists':False,'invalid_input':False,'logged_in':True,'username':request.session['C_username']}
                return render(request,"candidate_editprofile.html",context)
        else:
            return redirect('landingpage')
    else:  #if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')


def candidate_panel(request):  
    if 'C_username' in request.session:    #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        request.session['interview_id']=''
        d=request.session['C_username']
        ss=Candidate.objects.get(username=d)  #fetdh info of current candidate
        s=Interview.objects.filter(candidate_id=ss.id)   #feth all inteviews of current candidate(assigned+missed interviews)
        today = date.today()  
        available=[]   #for assigned interviews
        notavailable=[]  #for missed interviews
        z={}   #for creeating an object containing info of each interview (assigned+missed)
        c=1  #for numbering of assigned interviews
        e=1  #for numbering of missed interviews
        for f in s:  #for each interview
            if f.Status==False:  #to avoid showing interviews that the candidate has already given
                z={}
                t=Admin.objects.get(email=f.admin_id)  #get admin info of interview
                z['interview_deadline']=f.interview_deadline
                z['fname']=t.first_Name
                z['lname']=t.last_Name
                z['real_id']=f.id   #to be used if user wants to give interview
                if f.interview_deadline>=today: #for assigned interview
                    z['id']=c
                    c+=1
                    available.append(z)  #append to assigned interviews list
                else:  #for missed interview
                    z['id']=e
                    e+=1
                    notavailable.append(z)    #append to missed interviews list
        av_exist=False   #used for frontend(irrelevant for you)
        notav_exist=False   #used for frontend(irrelevant for you)
        if len(available)>0:
            av_exist=True
        if len(notavailable)>0:
            notav_exist=True
        context={'available':available,'notavailable':notavailable,'av_exist':av_exist,'notav_exist':notav_exist,'logged_in':True,'username':request.session['C_username']}
        return render(request,'candidate_panel.html',context)   #render page with interview lists
    else:   #if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')


def instructions(request,pk):
    if 'C_username' in request.session:       #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        candidate=Candidate.objects.get(username=request.session['C_username'])  #fetch current candidate's info from candidate table
        interview=Interview.objects.get(id=pk)  #get id of current interview from url
        if str(interview.candidate_id)==str(candidate.email):  #if this interview does belong to current candidate(making sure current candidate is not trying to access an interview that was not assigned to them)
            if interview.Status==False:
                today = date.today() 
                if today<=interview.interview_deadline:  #if user is not trying to access a mixed interview
                    request.session['interview_id']=interview.id
                    return render(request,'instructions.html',{'logged_in':True,'username':request.session['C_username']})
                else:  #current candidate is trying to access a missed interview
                    return redirect('candidate_panel')
            else:
                return redirect('candidate_panel')
        else:  #current candidate is trying to access an interview that was not assigned to them
            return redirect('candidate_panel')
    else:   #if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')


def checkmedia(request):
    if 'C_username' in request.session:   #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        if 'interview_id' in request.session:  #to make sure proper flow is being observed(This page was accessed by the appropriate candidate)
            if  request.session['interview_id']!='':   #to make sure proper flow is being observed(user clicked on 'give interview' button hence why they're here)
                interview=Interview.objects.get(id=request.session['interview_id']) #fetching info of the interview 
                if interview.Status==False:  #to make sure user is not trying to give the same interview twice(Status indicates whether user is giving the interview for the first time or not)
                    return render(request,'check_media.html',{'logged_in':True,'username':request.session['C_username']})
                else:  #if user is  trying to give the same interivew twice
                    return redirect('candidate_panel')
            else:  #if proper flow is not being observed(user didn't click 'give interview' button)
                return redirect('candidate_panel')
        else: #if proper flow is not being observed(invalid access) 
            return redirect('candidate_panel')
    else:    #if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')



def interview(request):
    if 'C_username' in request.session:   #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        if 'interview_id' in request.session: #to make sure proper flow is being observed(This page was accessed by the appropriate candidate)
            if  request.session['interview_id']!='':    #to make sure proper flow is being observed(user clicked on 'give interview' button hence why they're here)
                interview=Interview.objects.get(id=request.session['interview_id'])  #fetching info of the interview 
                form=Video_form(request.POST or None,request.FILES or None,instance=interview) 
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':  #if ajax call was made
                    if form.is_valid(): #if form is valid
                        form.save()
                        interview.interview_video=form['interview_video']
                        response = {'status': 1, 'message': "Ok"}
                        return HttpResponse(dumps(response), content_type='application/json')  #return success response to ajax call
                    else:
                        response = {'status': 0, 'message':"something went wrong"}   #return error response to ajax call
                        return HttpResponse(dumps(response), content_type='application/json')
                else: #if ajax call was not made
                    if interview.Status==False:     #to make sure user is not trying to give the same interview twice(Status indicates whether user is giving the interview for the first time or not)
                        interview.Status=True    #mark status as true which indicates that interview has been given
                        interview.save()
                        questions=Questionnaire.objects.get(Questionnaire_name=interview.Questionnaire)  #get questionnnaire object that was assigned to this interview by the interviewer
                        ques=[]
                        for qq in questions.questions.all().values_list('Actual_Question'):   #fetch each question from the questionnaire
                            ques.append(qq)
                        dd={'Questions':ques,'no_of_questions':len(ques)}
                        data=dumps(dd)   #make json object(so what we can use this data in js script)
                        return render(request,'interviewpage.html', {"form":form,'data':data,'logged_in':True,'username':request.session['C_username']})
                    else:  #if user is  trying to give the same interivew twice
                        return redirect('candidate_panel')
            else:    #if proper flow is not being observed(user didn't click 'give interview' button)
                return redirect('candidate_panel')
        else:#if proper flow is not being observed(invalid access)
            return redirect('candidate_panel')
    else:#if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')




def feedbackpage(request):
    if 'C_username' in request.session:   #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        if 'interview_id' in request.session: #to make sure proper flow is being observed(This page was accessed by the appropriate candidate)
            if  request.session['interview_id']!='':    #to make sure proper flow is being observed(user clicked on 'give interview' button hence why they're here)
                interview=Interview.objects.get(id=request.session['interview_id'])  #fetching info of the interview 
                if interview.Status==True: #to make sure user has given the interview
                    s=Interview.objects.get(id=request.session['interview_id'])   #fetch current interview info
                    form=FeedbackForm(request.POST or None,instance=s)
                    if request.method=="POST":  #if post request was made by the user
                        if form.is_valid(): #if form is valid
                            form.save()#save feedback
                            return redirect('concludepage')
                        else: #if invalid form(invalid input)
                            form=FeedbackForm(request.POST or None,instance=s)
                            context={'form':form,'invalid_input':True,'logged_in':True,'username':request.session['C_username']}
                            return render(request, 'feedback.html',context)  #render same page with "invalid input" alert
                    else:     #if post request was not made by the user(first time loading the page/refreshing the page)
                        form=FeedbackForm(request.POST or None,instance=s)
                        context={'form':form,'invalid_input':False,'logged_in':True,'username':request.session['C_username']}
                        return render(request, 'feedback.html',context)
                else:  #if user is  trying to give feedback to an interivew more than once
                        return redirect('candidate_panel')
            else:    #if proper flow is not being observed(user didn't click 'give interview' button)
                return redirect('candidate_panel')
        else:#if proper flow is not being observed(invalid access)
            return redirect('candidate_panel')
    else:#if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')


def concludepage(request):
    if 'C_username' in request.session:   #if candidate username is in session/cache. This is done to make sure this page is accessed by a legitimate candidate that has logged in successfully
        if 'interview_id' in request.session: #to make sure proper flow is being observed(This page was accessed by the appropriate candidate)
            if  request.session['interview_id']!='':    #to make sure proper flow is being observed(user clicked on 'give interview' button hence why they're here)
                interview=Interview.objects.get(id=request.session['interview_id'])  #fetching info of the interview 
                if interview.Status==True: #to make sure user has given the interview
                    if request.method=="POST":  
                        return redirect('candidate_panel')
                    else:
                        return render(request, 'conclude.html',{'logged_in':True,'username':request.session['C_username']})
                else:  #if user is  trying to give feedback to an interivew more than once
                        return redirect('candidate_panel')
            else:    #if proper flow is not being observed(user didn't click 'give interview' button)
                return redirect('candidate_panel')
        else:#if proper flow is not being observed(invalid access)
            return redirect('candidate_panel')
    else:#if candidate username is not in session/cache(Invalid access to this page)
        return redirect('landingpage')

















def adminn(request):   #for the option of signup or login for admin
    return render(request,'adminpage.html',{'logged_in':False})


def admin_login(request):
    form=admin_login_form(request.POST or None,request.FILES or None)
    if request.method == "POST":             #if a post request is made by the  user
            name=request.POST["email"]       #get email from post request that user made by clicking login button
            password=request.POST["password"]   #get password from post request that user made by clicking login button
            try:
                checkname=Admin.objects.get(email=name)   #check if entred email address exist in the admin table
                if checkname.password==password:           #if user credentials that were entered matches an instance in the admin table
                    request.session['A_email']=name        #save email address in session/cache to keep track of the current user that has logged in  
                    return redirect('admin_home')    #redirect to admin edit profile page(will be changed to admin panel)
                else:           #if entred email address does not exist in the admin table
                    form=admin_login_form()
                    context={'form':form,'invalid_input':True,'logged_in':False}
                    return render(request,"admin_login",context)   #render login page again but with invalid credentials alert
            except :        #if entered username doesn't match with any username in the candidate table
                form=admin_login_form()
                context={'form':form,'invalid_input':True,'logged_in':False}
                return render(request,"admin_login.html",context)   #render login page again but with invalid credentials alert
    else:
        form=admin_login_form()
        context={'form':form,'invalid_input':False,'logged_in':False}
        return render(request,"admin_login.html",context)




def admin_signup(request):
    val=False
    form=admin_signup_form(request.POST or None,request.FILES or None)
    if request.method == "POST":  #if post request is  made by the user
        val=EmailValidator()  #for email address validation
        try:
            ss=val(request.POST["email"])  #validating email address
            if request.POST["first_Name"]!='' and  request.POST["last_Name"]!='' and request.POST["email"]!= '' and request.POST["password"]!='' and not ss:  #if no field of the form was left blank and email address is valid
                if (Admin.objects.filter(email=request.POST["email"]).exists() or Candidate.objects.filter(email=request.POST["email"]).exists()) :  #if entered email address matches an email address in either the admin table or the candidate table
                    form=admin_signup_form()
                    context={'form':form,'email_exists':True,'invalid_input':False,'invalid_email':False,'logged_in':False}
                    return render(request,"admin_signup.html",context) #render same page with "email address already exists" alert
                else:  
                    current_date = datetime.now()
                    seed(int(current_date.strftime("%Y%m%d%H%M%S")))
                    request.session['f_Name']=request.POST["first_Name"]  #save entered first name of admin in session/cache 
                    request.session['l_Name']=request.POST["last_Name"]    #save entered last name of admin in session/cache 
                    request.session['A_Email']=request.POST["email"] #save email entered address of admin in session/cache 
                    request.session['Password']=request.POST["password"]   #save entered password of admin in session/cache 
                    request.session['d1']=randint(0,9)  #generate random 8 digit validation code
                    request.session['d2']=randint(0,9)  
                    request.session['d3']=randint(0,9)
                    request.session['d4']=randint(0,9)
                    request.session['d5']=randint(0,9)
                    request.session['d6']=randint(0,9)
                    request.session['d7']=randint(0,9)
                    request.session['d8']=randint(0,9)
                    s="Your confirmation code is :"+str(request.session['d1'])+str(request.session['d2'])+str(request.session['d3'])+str(request.session['d4'])+str(request.session['d5'])+str(request.session['d6'])+str(request.session['d7'])+str(request.session['d8'])
                    print(s)
                    # send_mail('Confirmation code',s,'tpearls.interportal@gmail.com',[request.POST["email"]],fail_silently=False)   #send confirmation email to user's email address
                    return redirect('email_confirmation')  #redirect to email confirmation page
            else:  #if one or more fields were left blank
                form=admin_signup_form()
                context={'form':form,'email_exists':False,'invalid_input':True,'invalid_email':False,'logged_in':False}
                return render(request,"admin_signup.html",context)  #render same page with "invalid input" alert
        except:   #invalid email address was entered
                form=admin_signup_form()
                context={'form':form,'email_exists':False,'invalid_input':False,'invalid_email':True,'logged_in':False} #render same page with "invalid email" alert
                return render(request,"admin_signup.html",context)
    else:  #if post request was not made by the user(first time loading the page/refreshing the page)
        form=admin_signup_form()
        context={'form':form,'email_exists':False,'invalid_input':False,'invalid_email':False,'logged_in':False}
        return render(request,"admin_signup.html",context)



def email_confirmation(request):
    try:
        em=request.session['A_Email']    #if admin email address is in session/cache. This is done to make sure this page is accessed by a legitimate admin that has logged in successfully
        context={'digit1':request.session['d1'],'digit2':request.session['d2'],'digit3':request.session['d3'],'digit4':request.session['d4'],'digit5':request.session['d5'],'digit6':request.session['d6'],'digit7':request.session['d7'],'digit8':request.session['d8'],'email':em}   #8 digit confirmation code
        data = dumps(context)  #making json dump to be used in the js script of email.confirmation.html
        return render(request,'email_confirmation.html',{'data':data,'logged_in':False})
    except:     #if admin email address is not in session/cache(Invalid access to this page)
        return redirect('landingpage')



def update_session(request):   #this page can't be accessed directly. It has no url. It will be accessed by the email confirmation page to indicate that email verification has been done
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':   #for ajax interaction
        request.session['done'] = 'true'  #for landing page(to indicate that a redirection has been done)
        return redirect('landingpage')



def admin_editprofile(request):
    if 'A_email' in request.session:  #if admin email address is in session/cache. This is done to make sure this page is accessed by a legitimate admin that has logged in successfully
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            form=admin_editprofile_form(request.POST or None,instance=s)
            if request.method == "POST": #if post request is made
                if request.POST["first_Name"]!='' and  request.POST["last_Name"]!='' and request.POST["email"]!= '' and request.POST["password"]!='':  #To make sure non of the fields was left empty          
                    if form.is_valid():  #if form is valid
                        form.save()
                        request.session['A_email']=request.POST["email"]  #save the email in session(update)
                        return redirect('admin_home')
                    else: #if form is invalid
                        form=admin_editprofile_form(instance=s)
                        context={'form':form,'invalid_input':True,'logged_in':True,'username':username} #render same page with 'invalid input' alert
                        return render(request,"admin_editprofile.html",context)
                else:  #if one or more fields were left empty in the form
                    form=admin_editprofile_form(instance=s)
                    context={'form':form,'invalid_input':True,'logged_in':True,'username':username} #render same page with 'invalid input' alert
                    return render(request,"admin_editprofile.html",context)
            else: # if post request was not made
                context={'form':form,'invalid_input':False,'logged_in':True,'username':username}
                return render(request,"admin_editprofile.html",context)
        else:    #if admin email address is not in session/cache(Invalid access to this page)
            return redirect('landingpage')
    else:    #if admin email address is not in session/cache(Invalid access to this page)
        return redirect('landingpage')



def add_questions(request):
    if 'A_email' in request.session:  #if admin email address is in session/cache. This is done to make sure this page is accessed by a legitimate admin that has logged in successfully
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            form=add_questions_form(request.POST or None,request.FILES or None)
            if request.method=="POST":   #if post request was made by the user
                if form.is_valid():  #if form is valid
                    form.save()  #save from(entered question to ActualQuestion table)
                    return redirect('admin_home')
                else:  #if form is invalid(invalid input)
                    form=add_questions_form()
                    context={'form':form,'invalid_input':True,'logged_in':True,'username':username}
                    return render(request, 'add_questions.html',context) #render same page with "invalid input" alert
            else:   #if post request was not made by the user(first time loading page/refresh)
                form=add_questions_form()
                context={'form':form,'invalid_input':False,'logged_in':True,'username':username}
                return render(request, 'add_questions.html',context)


def questionnairesetup(request):
    if 'A_email' in request.session:  #if admin email address is in session/cache. This is done to make sure this page is accessed by a legitimate admin that has logged in successfully
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            s=ActualQuestion.objects.all()  #fetch all questions from ActualQuestion table
            no=ActualQuestion.objects.all().values_list('Actual_Question',flat=True)
            dat=[x for x in no]
            data=dumps({'questions':dat})
            form=create_questionnaire_form(request.POST or None,request.FILES or None)
            form2=add_questions_form(request.POST or None,request.FILES or None)
            
            if request.method=="POST": 
                if 'form2' in request.POST:
                    if form2.is_valid(): 
                        form2.save()  
                        return redirect('questionnairesetup')
                    else:  
                        form=create_questionnaire_form()
                        form2=add_questions_form()
                        context={'questions':s,'form':form,'form2':form2,'q_exists':False,'invalid':False,'noques':False,'data':data,'logged_in':True,'username':username,'invalid_input':True}
                        return render(request, 'questionnaire_setup.html',context)
                
                if 'form' in request.POST:
                    if request.POST['Questionnaire_name']!='':  #if questionnaire name field is not blank
                        zz=request.POST.getlist('selected')  #get all the selected questions for the questionnaire
                        if len(zz)>0:  #if atleast 1 question was selected
                            if not Questionnaire.objects.filter(Questionnaire_name=request.POST['Questionnaire_name']).exists():   #if entered questionnaire name  does nt match with a questionnaire name in the questionnaire table
                                form.save()  #save questionnaire n,e
                                b = Questionnaire.objects.get(Questionnaire_name=request.POST['Questionnaire_name'])
                                zz=request.POST.getlist('selected')
                                for f in zz:  #for each selected qustion
                                    e = ActualQuestion.objects.get(Actual_Question=f)  #fetch info of the question
                                    b.questions.add(e)   #assign question to the newly created questionnaire
                                return redirect('admin_home')
                            else:    #if entered questionnaire name matchs with a questionnaire name in the questionnaire table
                                form=create_questionnaire_form()
                                form2=add_questions_form()
                                context={'questions':s,'form':form,'form2':form2,'q_exists':True,'invalid':False,'noques':False,'data':data,'logged_in':True,'username':username}
                                return render(request, 'questionnaire_setup.html',context)
                        else:    #if no question was selected for the questionnaire
                            form=create_questionnaire_form()
                            form2=add_questions_form()
                            context={'questions':s,'form':form,'form2':form2,'q_exists':False,'invalid':False,'noques':True,'data':data,'logged_in':True,'username':username}
                            return render(request, 'questionnaire_setup.html',context)   
                    else:  #if questionnaire name was not provided by the user
                        form=create_questionnaire_form()
                        form2=add_questions_form()
                        context={'questions':s,'form':form,'form2':form2,'q_exists':False,'invalid':True,'noques':False,'data':data,'logged_in':True,'username':username}
                        return render(request, 'questionnaire_setup.html',context)
            else:     #if post request was not made by the user(first time loading the page/refreshing the page)
                form=create_questionnaire_form()
                form2=add_questions_form()
                context={'questions':s,'form':form,'form2':form2,'q_exists':False,'invalid':False,'noques':False,'data':data,'logged_in':True,'username':username}
                return render(request, 'questionnaire_setup.html',context)




def admin_home(request):
    if 'A_email' in request.session:
        if request.session['A_email']!='':
            request.session['delete_interview']=''
            admin=Admin.objects.get(email=request.session['A_email'])
            s=Interview.objects.filter(admin_id=admin.id)
            given=[]
            notgiven=[]
            missed=[]
            today = date.today()  
            for a in s:
                    if a.Status==True:
                        given.append(a)
                    else:
                        if a.interview_deadline>=today:
                            notgiven.append(a)
                        else:
                            missed.append(a)
            av_exist=False   #used for frontend(irrelevant for you)
            notav_exist=False   #used for frontend(irrelevant for you)
            miss=False
            if len(given)>0:
                av_exist=True
            if len(notgiven)>0:
                notav_exist=True
            if len(missed)>0:
                miss=True
            print(av_exist,notav_exist)
            username=str(admin.first_Name)+" "+str(admin.last_Name)
            if request.method=="POST":
                if 'delete' in request.POST:
                    i=Interview.objects.get(id=request.POST['delete'])
                    i.delete()
                    return redirect('admin_home')
            return render(request, 'admin_panel.html',{'logged_in':True,'username':username,'given':given,'notgiven':notgiven,'missed':missed,'av_exist':av_exist,'notav_exist':notav_exist,'miss':miss,'av_len':len(given),'notav_len':len(notgiven),'miss_len':len(missed)})
        else:
            return redirect('landingpage')
    else:
        return redirect('landingpage')




def view_questions(request):
    s=ActualQuestion.objects.all()
    context={'questions':s,'q_exists':False,'invalid':False,'noques':False}
    return render(request, 'view_questions.html',context)

def view_or_add_questions(request):
    if request.method=="POST":
        return redirect('landingpage')
    return render(request, 'view_or_add_questions.html')

def view_or_add_candidates(request):
    if request.method=="POST":
        return redirect('landingpage')
    return render(request, 'view_or_add_candidates.html')

def view_candidates(request):
    if 'A_email' in request.session:  #if admin email address is in session/cache. This is done to make sure this page is accessed by a legitimate admin that has logged in successfully
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            if request.method == "POST":
                if 'choice' in request.POST:
                    email=request.POST['choice'][request.POST['choice'].find('E',0,len(request.POST['choice']))+7:]
                    request.session['email_interview']=email
                    return redirect('create_interview')

            dd=Candidate.objects.all().values_list('email',flat=True)
            emails=[v for v in dd]
            data=dumps({'emails':emails})
            s=Candidate.objects.all().values_list('first_Name', flat=True).order_by('email')
            l=Candidate.objects.all().values_list('last_Name', flat=True).order_by('email')
            name = [str(x)+" "+str(y) for x, y in zip(s, l)]
            e=Candidate.objects.all().values_list('email', flat=True)
            info= ["Candidate:"+" "+x+"."+" "+"Email: "+y for x, y in zip(name, e)]
            context={'info':info,'invalid':False,'data':data,'logged_in':True,'username':username}
            return render(request, 'view_candidates.html',context)
        else:
            return redirect('landingpage')
    else:
            return redirect('landingpage')


def candidate_saved(request):
    if request.method=="POST":
        return redirect('landingpage')
    return render(request, 'candidate_saved.html')


def create_interview(request):
    if 'A_email' in request.session:  #if admin email address is in session/cache. This is done to make sure this page is accessed by a legitimate admin that has logged in successfully
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            dd=Candidate.objects.all().values_list('email',flat=True)
            ee=Candidate.objects.all().values_list('Position__position',flat=True).order_by('email')
            ff=Questionnaire.objects.all().values_list('Questionnaire_name',flat=True)
            emails=[v for v in dd]
            questionnaires=[s for s in ff]
            positions=[e for e in ee]
            data=dumps({'emails':emails,'questionnaires':questionnaires,'positions':positions})
            form=formm(request.POST or None,request.FILES or None)
            if request.method == "POST":  
                if "candidate_signup" in request.POST:
                    return redirect('candidate_signup')

                do=datetime.strptime(form.data['deadline'],'%m/%d/%Y')
                do.strftime("%Y-%m-%d")
                Interview.objects.create(candidate_id=Candidate.objects.get(email=form.data['candidate_name']),admin_id=Admin.objects.get(id=s.id),interview_deadline=do,interview_email=form.data['email'],Questionnaire=Questionnaire.objects.get(Questionnaire_name=form.data['Questionnaire_name'])) 
                request.session['new_user']=''
                send_mail('Technical Interview invitation',form.data['email'],'tpearls.interportal@gmail.com',[form.data['candidate_name']],fail_silently=False)   #send confirmation email to user's email address
                return redirect('admin_home')
            if 'new_user' in request.session:
                if request.session['new_user']!='': 
                    can=Candidate.objects.get(email=request.session['new_user']) 
                    return render(request,'create_interview.html',{'form':form,'data':data,'emails':emails,'questionnaires':questionnaires,'new_user':dumps({'em':can.username,'pass':can.password}),'logged_in':True,'username':username})      
            return render(request,'create_interview.html',{'form':form,'data':data,'emails':emails,'questionnaires':questionnaires,'new_user':dumps({'em':'0'}),'logged_in':True,'username':username})
        else:
            return redirect('landingpage')
    else:
        return redirect('landingpage')


def display_interview(request,pk):
    if 'A_email' in request.session:
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            inter=Interview.objects.get(id=pk)
            candidate=Candidate.objects.get(id=inter.candidate_id.id)
            questions=Questionnaire.objects.get(Questionnaire_name=inter.Questionnaire)  #get questionnnaire object that was assigned to this interview by the interviewer
            ques=[]
            for qq in questions.questions.all().values_list('Actual_Question',flat=True):   #fetch each question from the questionnaire
                ques.append(qq)
            no_video=False
            if inter.interview_video=='':
                no_video=True
            context={'data':inter,'questions':ques,'candidate':candidate,'logged_in':True,'username':username,'no_video':no_video}
            return render(request,'display_interview.html',context)
        else:
            return redirect('landingpage')
    else:
        return redirect('landingpage')


def router(request):
    if 'A_email' in request.session:
        if request.session['A_email']!='':
            return redirect('admin_home')
    elif 'C_username' in request.session:
        if request.session['C_username']!='':
            return redirect('candidate_panel')
    return redirect('landingpage')

def router1(request):
    if 'A_email' in request.session:
        if request.session['A_email']!='':
            return redirect('admin_editprofile')
    elif 'C_username' in request.session:
        if request.session['C_username']!='':
            return redirect('candidate_editprofile')
    return redirect('landingpage')


def view_questionnaires(request):
    sss=Questionnaire.objects.all().values_list('Questionnaire_name', flat=True)
    context={'sss':sss}
    return render(request,'view_questionnaires.html',context)

def view_or_create_questionnaires(request):
    if request.method=="POST":
        return redirect('landingpage')
    return render(request, 'view_or_create_questionnaires.html')


# def view_questionnaires(request):
#     q=Questionnaire.objects.all()
#     return render(request,'view_questionnaires.html',{"questionnaires":q})

# def questionnaire_details(request,pk):
#     Q=Questionnaire.objects.get(id=pk)
#     questions=Q.questions.all()
#     return render(request,'questionnaire_details.html',{'questions':questions})


# def view_questionnaires(request):
#     q=Questionnaire.objects.all()
#     return render(request,'view_questionnaires.html',{"questionnaires":q})

# def questionnaire_details(request,pk):
#     Q=Questionnaire.objects.get(id=pk)
#     questions=Q.questions.all()
#     return render(request,'questionnaire_details.html',{'questions':questions})

def View_Questionnaires(request):
    if 'A_email' in request.session:
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            q=Questionnaire.objects.all()
            return render(request,'View_Questionnaires.html',{"questionnaires":q,'logged_in':True,'username':username})
        else:
            return redirect('landingpage')
    else:
        return redirect('landingpage')

def View_Question(request,pk):
    if 'A_email' in request.session:
        if request.session['A_email']!='':
            d=request.session['A_email']  #fetch admin email address from session/cache
            s=Admin.objects.get(email=d)  #get info of admin from admin table using email address
            username=str(s.first_Name)+" "+str(s.last_Name)
            Q=Questionnaire.objects.get(id=pk)
            questions=Q.questions.all()
            return render(request,'View_Question.html',{'questions':questions,'logged_in':True,'username':username})
        else:
            return redirect('landingpage')
    else:
        return redirect('landingpage')


