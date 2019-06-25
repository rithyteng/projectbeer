from django.shortcuts import render, HttpResponse,redirect
from .models import users
import bcrypt
from django.contrib.messages import error

def index(request):
    return render(request,'myapp/index.html')

def signup(request):
    return render(request,'myapp/signup.html')

def login(request):
    return render(request,'myapp/login.html')
    
def signupp(request):
    #adding the information into the database
    if request.method=="POST":
        errorz=users.objects.basicValid(request.POST)
        if errorz:
            for i in errorz:
                error(request,i)
            return redirect('/signup')
        else:
            new_id=users.objects.register_user(request.POST)
            print(new_id)
            print('*'*50)
            request.session['userid']=new_id
            context={
                'username':users.objects.get(id=new_id).firstname,
                'email':users.objects.get(id=new_id).email
            }
    return render(request,'myapp/reg.html',context)

def loginp(request):
    if request.method=='POST':
        login=users.objects.loginValid(request.POST)
        if login==True:
            new_id=users.objects.get(username=request.POST['username']).id
            request.session['userid']=new_id
            return redirect('/thelogin')
        else:
            for i in login:
                error(request,i)
            return redirect('/login')
    return redirect('/thelogin')

def thelogin(request):
    try:
        if not request.session['userid']:
            return redirect('/login')
    except:
        return redirect('/login')
    else:
        myid=request.session['userid']
        print('*'*50)
        print(myid)
        context={
            'myuserid':users.objects.get(id=myid).id,
            'myuserfirstname':users.objects.get(id=myid).firstname,
            'myuserlastname':users.objects.get(id=myid).lastname,
            'myuseremail':users.objects.get(id=myid).email,   
        }
    return render(request,'myapp/dashboard.html',context)

def logout(request):
    try:
        del request.session['userid']
    except:
        redirect('/')
    # del request.session['userid']
    return redirect('/')

