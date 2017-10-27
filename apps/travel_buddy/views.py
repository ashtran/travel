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
    context={}
    return render(request, 'travel_buddy/dashboard.html',context)

def addplan(request):
    # #<--- Check if logged in/in session --->
    # try:
    #     request.session['user_id']
    # except KeyError:
    #     return redirect('/')
    #
    # context={
    #     'authors':Author.objects.all()
    # }
    return render(request, 'travel_buddy/addplan.html')
def processplan(request):
    # errors= Review.objects.validate_newreview(request.POST,request.session['user_id'])
    # if len(errors):
    #     for field, message in errors.iteritems():
    #         error(request, message, extra_tags=field)
    #     return redirect('/addbook')
    #
    # else:
    #     new_author= Author.objects.create_author(request.POST)
    #     new_book= Book.objects.create_book(request.POST,new_author.id)
    #     newentry= Review.objects.add_review(request.POST,new_book.id,request.session['user_id'])

        return redirect('/dashboard')
#<--- Book Review Page --->#

def destination(request,user_id):
    # user= User.objects.get(id=user_id)
    # context={
    #     'user':user,
    #     'reviewedbooks':Review.objects.filter(reviewer_id=user.id)
    # }
    return render(request, 'travel_buddy/destination.html')
#<--- Process Logout --->#
def logout(request):
    del request.session['user_id']
    return redirect('/')
