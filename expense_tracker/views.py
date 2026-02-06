from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Expense


def user_login(request):

    if request.method == "POST":
        
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        sign = request.POST.get("sign")
        
        
        
        if sign == "up":
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists")
                
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect("expense_tracker:home")

    
        elif sign =="in":
            user = authenticate(request, username=username, password=password)
            if user is  None:
                messages.error(request,"Incorrect Information.")
            else:
                login(request, user)
                messages.success(request,"Successfully signed in.")
                return redirect( "expense_tracker:home")
                
        
    return render(request, "expense_tracker/login.html")

      


def user_passwordchange(request):
    if request.method == "POST":
        old_password = request.POST.get("old")
        new_password = request.POST.get("new")
        user = request.user
  
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect")
            place = "wrong old password"
            return render(request, "expense_tracker/passwordchange.html",{"place":place})

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)
        place = "inpost"
        messages.success(request, f"Password changed successfully for {user.username}")
        return render(request, "expense_tracker/home.html",{"place":place})
    
    place ="not inpost"
    return render(request, "expense_tracker/passwordchange.html",{"place":place})



def user_logout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect( "expense_tracker:login")
      

def user_home(request):
    user= request.user
    if user is None:
        return redirect("expense_tracker:login")
    
    return render(request, "expense_tracker/home.html") 

def addexpense(request):
    
    user= request.user
    user_id =user.id
    date = timezone.now()
    
    if request.method == "POST":
        exp_category = request.POST.get("category")
        exp_amount = request.POST.get("amount")
        
        Expense.objects.create(user_id=user_id,exp_amount=exp_amount,exp_category=exp_category,date=date)
        return redirect( "expense_tracker:displayexpense")

        
    return render(request,"expense_tracker/addexpense.html")

def displayexpense(request):
    user= request.user
    sortby = request.GET.get("sortby")
    expenselist = Expense.objects.filter(user_id =user.id).order_by("-date")
    if sortby == "date":
        expenselist = Expense.objects.filter(user_id =user.id).order_by("-date")
    elif sortby == "category":
        expenselist = Expense.objects.filter(user_id =user.id).order_by("-exp_category")
    elif sortby == "amount":
        expenselist = Expense.objects.filter(user_id =user.id).order_by("-exp_amount")
    
    
    monthexpense= Expense.objects.filter(date__gte=timezone.now()-timedelta(days=30),user_id=user.id)
    totalexpense=0
    for i in monthexpense:
        totalexpense+=i.exp_amount




    return render(request,"expense_tracker/displayexpense.html",{"expenses":expenselist,"totalexpense":totalexpense})
