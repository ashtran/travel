from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import *
from django.contrib.messages import error
from django.contrib import messages

#<--- Homepage --->#
def index(request):
    return render(request, 'travel_buddy/index.html')
#<--- Process Create New User --->#
def createuser(request):
    errors= User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user= User.objects.create_user(request.POST)
        request.session['user_id']=user.id
        return redirect('/dashboard')
#<--- Process User Login --->#
def login(request):
    errors= User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user= User.objects.filter(username=request.POST['username'])[0]
        request.session['user_id']=user.id
        return redirect('/dashboard')
#<--- User Dashboard --->#
def dashboard(request):
    #<--- Check if logged in/in session --->
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    user_id=request.session['user_id']
    context={
        'user':User.objects.get(id=user_id),
        'schedules':Plan.objects.filter(planner_id=user_id),
        'others':Plan.objects.exclude(planner_id=user_id),
    }
    return render(request, 'travel_buddy/dashboard.html',context)

def delete(request,plan_id):
    cancelplan=User.objects.get(id=request.session['user_id']).plans.remove(Plan.objects.get(id=plan_id))
    print delete_review
    return redirect('/reviews/{}'.format(book_id))
#<--- Process Add Review --->#

def join(request,plan_id):
    joinplan= User.objects.get(id=request.session['user_id']).plans.add(Plan.objects.get(id=plan_id))
    return redirect('/dashboard')
#<--- User Info Page --->#

def addplan(request):
    #<--- Check if logged in/in session --->
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')

    return render(request, 'travel_buddy/addplan.html')

def processplan(request):
    # errors= Review.objects.validate_plan(request.POST,request.session['user_id'])
    # if len(errors):
    #     for field, message in errors.iteritems():
    #         error(request, message, extra_tags=field)
    #     return redirect('/addplan')
    #
    # else:
        new_plan= Plan.objects.add_plan(request.POST,request.session['user_id'])

        return redirect('/dashboard')

def destination(request,plan_id):
    plan= Plan.objects.get(id=plan_id)
    companions=Plan.objects.exclude(planner_id=request.session['user_id'])
    context={
        'plan':plan,
        'companions':companions,
    }
    return render(request, 'travel_buddy/destination.html',context)
#<--- Process Logout --->#
def logout(request):
    del request.session['user_id']
    return redirect('/')
