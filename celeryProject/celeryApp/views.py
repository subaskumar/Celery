from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from celeryApp.forms import SignUpForm,UserLoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
#import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from openpyxl import Workbook

# Create your views here.
def home(request):
    if request.method == "POST":
        file = request.FILES['excelfile']
        print(file)
        xl = pd.ExcelFile(file)
        df = xl.parse(xl.sheet_names[0])
        user_list = []

        for r in dataframe_to_rows(df, index=True, header=True):
            user_list.append(r)
        print(user_list)
        return render(request,'celeryApp/home.html',{'user_list':user_list})
    return render(request,'celeryApp/home.html')
def sinUp_view(request):
    message = ''
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            form = SignUpForm()
            message = 'Registration Successfull'
        return render(request,'celeryApp/signUp.html',{'form':form,'message': message})
    
    else:
        form = SignUpForm()        
        return render(request,'celeryApp/signUp.html',{'form':form,'message': message})

def login_view(request):
    
    if request.user.is_authenticated:
        return render(request, 'celeryApp/home.html',)
    else:
        form = UserLoginForm()
        if request.method == "POST":
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request,username=username, password=password)
                login(request, user)
                return redirect('/home')
        return render(request, 'celeryApp/LogIn_form.html',{'form':form})
        
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')