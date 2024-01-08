from django.shortcuts import render, redirect, HttpResponse
from . models import user,survey
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
import re
import csv, io
import math, random
import pandas as pd


# Create your views here.
def listToString(s):
    str1 = " " 
    return (str1.join(s)) 

def index(request):
    return render(request,'login.html')

def signuppage(request):
    return render(request,'signup.html')

def logout(request):
    request.session['uid'] = None
    return redirect('index')

def home(request):
    return render(request,'home.html')

def userlogin(request):
    if request.method=='POST':
        mail = request.POST['email']
        pwd = request.POST['password']

        try:
            u = user.objects.get(email=mail, password=pwd)
            request.session['uid'] = u.id
            print(u.id)
            return redirect('home')

        except ObjectDoesNotExist:
            # uid = None
            request.session['uid'] = None
            messages.info(request,'Invalid credentials')
            return redirect('index')
         
    return redirect('index')

def usersignup(request):
    if request.method=='POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        mail = request.POST['email']
        ph = request.POST['phone']
        dob = request.POST['dob']
        gender = request.POST['gender']
        dist = request.POST['district']
        state = request.POST['state']
        country = request.POST['country']
        pwd = request.POST['password']
        cpwd = request.POST['confirmpassword']

        try:
            u = user.objects.get(email=mail)
            messages.info(request,'Email Address already Taken')
            return redirect('index')

        except ObjectDoesNotExist:
            if cpwd == pwd:
                ux = {'firstname':fname,'lastname':lname,'email':mail,'phone':ph,'dob':dob,'gender':gender,'country':country,'state':state,'district':dist,'password':pwd}
                request.session['userverification'] = ux


                digits = "0123456789"
                OTP = ""
                for i in range(4):
                    OTP += digits[math.floor(random.random() * 10)]
                print(OTP)
                request.session['otp'] = OTP

                text = []
                text.append(OTP)
                text.append(" This is Your OTP and Please Don't share this with others ")

                Subject = "Anti-TB OTP"
                Main_Text = listToString(text)
                From_mail = settings.EMAIL_HOST_USER
                To_mail = [mail]

                send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
                messages.info(request,'OTP is sent to Gmail')

                return render(request,'otppage.html')
            else:
                messages.info(request,'Confirm Password does not Match')

    return redirect('index')

def checkotp(request):
    if request.method=='POST':
        mail_otp = request.POST['otpinput']
        ux = request.session['userverification']
        OTP = request.session['otp']
        if mail_otp == OTP:
            usignup = user(firstname=ux['firstname'],lastname=ux['lastname'],email=ux['email'],phone=ux['phone'],dob=ux['dob'],gender=ux['gender'],country=ux['country'],state=ux['state'],district=ux['district'],password=ux['password'])
            usignup.save()
            messages.info(request,'Successfully Registered')
            return redirect('index')
        else:
            messages.info(request,'Something Went Wrong')
            return redirect('index')
        
def resendotp(request):
    ux = request.session['userverification']

    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    print(OTP)
    request.session['otp'] = OTP
    
    text = []
    text.append(OTP)
    text.append(" This is Your OTP and Please Don't share this with others ")

    Subject = "Anti-TB OTP"
    Main_Text = listToString(text)
    From_mail = settings.EMAIL_HOST_USER
    To_mail = [ux['email']]

    send_mail(Subject, Main_Text, From_mail, To_mail, fail_silently=False)
    messages.info(request,'OTP is sent to Gmail')

    return render(request,'otppage.html')


def surveypage(request):
    uid = request.session['uid']

    try:
        sur = survey.objects.get(uid=uid)
        print(sur)
        messages.info(request,'You Already Submitted Survey Form')
        return render(request,'survey.html',{'x': "off"})

    except survey.DoesNotExist:
        return render(request,'survey.html',{'x': "on"})

    return render(request,'survey.html')

def survey_form(request):
    if request.method=='POST':
        one = request.POST['1']
        two = request.POST['2']
        three = request.POST['3']
        four = request.POST['4']
        five = request.POST['5']
        six = request.POST['6']
        seven = request.POST['7']
        eight = request.POST['8']
        nine = request.POST['9']
        ten = request.POST['10']
        eleven = request.POST['11']
        twelve = request.POST['12']
        thirteen = request.POST['13']
        fourteen = request.POST['14']
        fifteen = request.POST['15']
        sixteen = request.POST['16']
        seventeen = request.POST['17']
        eighteen = request.POST['18']
        nineteen = request.POST['19']
        twenty = request.POST['20']

        # print(one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty)
        payload = one+ two+ three+ four+ five+ six+ seven+ eight+ nine+ ten+ eleven+ twelve+ thirteen+ fourteen+ fifteen+ sixteen+ seventeen+ eighteen
        print("pay",payload)
        
        q2 = r'1[2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3][2-3]'
        q2res = re.findall(q2, payload)
        print("q2r",q2res)

        q3 = r'1111[2-3][2-3][2-3]0000111[1-2]00'
        q3res = re.findall(q3, payload)
        print("q3r",q3res)

        q4 = r'111111112[1-2]2[1-2][1-2][1-2][1-2][1-2][1-2][1-2]'
        q4res = re.findall(q4,payload)
        print("q4r",q4res)

        q8 = r'111111111111[2-3]11[2-3][2-3]2'
        q8res = re.findall(q8,payload)
        print("q8r",q8res)

        q14 = r'1111111[2-3][2-3]221111122'
        q14res = re.findall(q14,payload)
        print("q14",q14res)

        known = ""
        group = 0
        if payload == "222222222222222222":
            print("1.Unaware - Ignorant")
            group = 1
            known = "Unaware - Ignorant"
        elif q2res != [] and payload == q2res[0]:
            print("2.Aware, low knowledge")
            group = 2
            known = "Aware, low knowledge"
        elif q3res != [] and payload == q3res[0]:
            print("3.Aware,  knowledgeable, Manages TB, not knowing the benifits")
            group = 3
            known = "Aware,  knowledgeable, Manages TB, not knowing the benifits"
        elif q4res != [] and payload == q4res[0]:
            print("4.Aware, has knowledge, Manages TB, aware of centres around but does not notify")
            group = 4
            known = "Aware, has knowledge, Manages TB, aware of centres around but does not notify"
        elif payload == "111111122222222212":
            print("5.Aware, has knowledge, doesnot manage TB, but refers")  
            group = 5
            known = "Aware, has knowledge, doesnot manage TB, but refers"
        elif payload == "122222222222222211":
            print("6.Aware, no knowledge, but refers")
            group = 6
            known = "Aware, no knowledge, but refers"
        elif payload == "111111122221111222" or payload == "111111122221111322":
            print("7.Aware, has knowledge, diagnoses, but doesnot notify")
            group = 7
            known = "Aware, has knowledge, diagnoses, but doesnot notify"
        elif q8res != [] and payload == q8res[0]:
            print("8.Aware, has knowledge, diagnoses, notifies")
            group = 8
            known = "Aware, has knowledge, diagnoses, notifies"
        elif payload == "111111111111111111":
            print("9.Aware, has knowledge, treats, monitors and notifies, 11.Aware, has knowledge, treats, donot monitor but notifies, 13.Aware, has knowledge - unintrested")
            group = 9
            known = "Aware, has knowledge, treats, monitors and notifies, 11.Aware, has knowledge, treats, donot monitor but notifies, 13.Aware, has knowledge - unintrested"
        elif payload == "111111122222112222":
            print("10.Aware, has knowledge, treats, donot monitor and donot notify")
            group = 10
            known = "Aware, has knowledge, treats, donot monitor and donot notify"
        elif payload == "111111122221111111":
            print("12.Aware, has knowledge, treats,  monitors but donot notify")
            group = 12
            known = "Aware, has knowledge, treats,  monitors but donot notify"
        elif q14res != [] and payload == q14res[0]:
            print("14.Aware - Un co-operative")
            group = 14
            known = "Aware - Un co-operative"
        else: 
            print("Other")
            group = 15
            known = "Other"

        # elif payload == "111111122221111122" or payload == "111111123221111122" or payload == "111111132221111122" or payload == "111111133221111122":
        #     print("14.Aware - Un co-operative")
        
        # elif payload == "111111111111211222" or payload == "111111111111211232" or payload == "111111111111211322" or payload == "111111111111211332":
        #     print("8.Aware, has knowledge, diagnoses, notifies")
        # elif payload == "111111111111311222" or payload == "111111111111311232" or payload == "111111111111311322" or payload == "111111111111311332":
        #     print("8.Aware, has knowledge, diagnoses, notifies")

        print(known)
        uid = request.session['uid']
        print(uid)
        ans = payload + nineteen + twenty
        survey_form = survey(uid=uid,answers=ans,group=group,knowledge=known)
        survey_form.save()

    messages.info(request,'Thanks for filling the Survey Form and Your Support')
    return render(request,'home.html')












##################################   admin   #######################################
def admin(request):
    return render(request,'adminlogin.html')

def adminlogin(request):
    if request.method=='POST':
        mail = request.POST['email']
        pwd = request.POST['password']
   
        if mail == "admin@123" and pwd == "admin@123":
            request.session['aid'] = "0"
            print(request.session['aid'])
            return redirect('adminhome')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('admin')
    return redirect('admin')

def adminlogout(request):
    request.session['aid'] = None
    return redirect('admin')

def adminhome(request):
    try:
        sur = survey.objects.all()
        users = user.objects.all()
        print("*********************************************************")
        for r in sur: 
            for u in users:
                if u.id == r.uid:
                    print(r.uid,u.id,u.firstname,u.lastname,u.phone,u.email,r.group,r.knowledge)
                    
        print("*********************************************************")  
             
        if not sur:
            messages.info(request,'Survey Not found')
            return render(request,'adminhome.html')
        else:
            return render(request,'adminhome.html', { 'sur':sur, 'users': users })

    except ObjectDoesNotExist:
        messages.info(request,'Survey Not found')
        return render(request,'adminhome.html')

    return render(request,'adminhome.html')

def surveyresult(request):
    try:
        sur = survey.objects.all()
        users = user.objects.all()
        # print("*********************************************************")
        # for r in sur: 
        #     for u in users:
        #         if u.id == r.uid:
        #             print(r.uid,u.id,u.firstname,u.lastname,u.phone,u.email,r.group,r.knowledge)
                    
        # print("*********************************************************")  
             
        if not sur:
            messages.info(request,'Survey Not found')
            return render(request,'surveyresult.html')
        else:
            return render(request,'surveyresult.html', { 'sur':sur, 'users': users })

    except ObjectDoesNotExist:
        messages.info(request,'Survey Not found')
        return render(request,'surveyresult.html')

    return render(request,'surveyresult.html')


def downloadreport(request):
    sur = survey.objects.all()
    users = user.objects.all()

    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="anti_tuberculosis_report.csv"'

    writer=csv.writer(response, delimiter=',')
    writer.writerow(['firstname','lastname','phone number','email','group number','knowledge'])

    for r in sur: 
        for u in users:
            if u.id == r.uid:
                writer.writerow([u.firstname,u.lastname,u.phone,u.email,r.group,r.knowledge])
    return response

def statistics(request):
    sur = survey.objects.all()
    users = user.objects.all()
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    g6=0
    g7=0
    g8=0
    g9=0
    g10=0
    g11=0
    g12=0
    g13=0
    g14=0
    g15=0
    print("*********************************************************")
    for r in sur: 
        for u in users:
            if u.id == r.uid:
                print(r.uid,u.id,u.firstname,u.lastname,u.phone,u.email,r.group,r.knowledge)
                if r.group == 1:
                    g1 += 1
                elif r.group == 2:
                    g2 += 1
                elif r.group == 3:
                    g3 += 1
                elif r.group == 4:
                    g4 += 1
                elif r.group == 5:
                    g5 += 1
                elif r.group == 6:
                    g6 += 1
                elif r.group == 7:
                    g7 += 1
                elif r.group == 8:
                    g8 += 1
                elif r.group == 9:
                    g9 += 1
                elif r.group == 10:
                    g10 += 1
                elif r.group == 11:
                    g11 += 1
                elif r.group == 12:
                    g12 += 1
                elif r.group == 13:
                    g13 += 1
                elif r.group == 14:
                    g14 += 1
                elif r.group == 15:
                    g15 += 1
    print("*********************************************************")  
    print(g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12,g13,g14,g15)
    return render(request,'statistics.html',{'g1':g1,'g2':g2,'g3':g3,'g4':g4,'g5':g5,'g6':g6,'g7':g7,'g8':g8,'g9':g9,'g10':g10,'g11':g11,'g12':g12,'g13':g13,'g14':g14,'g15':g15})



def reportsendgmail(request):
    sur = survey.objects.all()
    users = user.objects.all()

    fn = []
    ln = []
    ph = []
    em = []
    gno = []
    know = []
    for r in sur: 
        for u in users:
            if u.id == r.uid:
                if u.firstname != "":
                    fn.append(u.firstname)
                else:
                    fn.append('null')
                if u.lastname != "":
                    ln.append(u.lastname)
                else:
                    fn.append('null')
                if u.phone != "":
                    ph.append(u.phone)
                else:
                    fn.append('null')
                if u.email != "":
                    em.append(u.email)
                else:
                    fn.append('null')
                if r.group != "":
                    gno.append(r.group)
                else:
                    fn.append('null')
                if r.knowledge != "":
                    know.append(r.knowledge)
                else:
                    fn.append('null')
 
    response = {
        'firstname': fn,
        'lastname': ln,
        'phone number': ph,
        'email': em,
        'group number': gno,
        'knowledge': know
    }

    df = pd.DataFrame(response)
    df.to_csv(r'static/excel/anti_tuberculosis_report.csv', index=False)


    text = []
    text.append("")
    Subject = "Excel Report From Anti Tuberculosis"
    Main_Text = listToString(text)
    From_mail = settings.EMAIL_HOST_USER
    To_mail = ['ganeshn944870@gmail.com']

    mail = EmailMessage(Subject, Main_Text, From_mail, To_mail)
    mail.attach_file('static/excel/anti_tuberculosis_report.csv')
    mail.send()
    
    messages.info(request,'Report is sent to Gmail Successfully')
    return redirect(surveyresult)