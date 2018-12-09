from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import datetime,timedelta,time

NAME_REGEX=re.compile(r'^[a-zA-Z+ ]+$')


class UserManager(models.Manager):
# <--- Validate User Login---> #
    def validate_login(self,post_data):
        errors={}
        login=self.filter(username=post_data['username'])
        # <- Get Login username -> #
        if len(login)>0:
            user=login[0]
            # <- Password -> #
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['login']="username/password is incorrect"
        # <- Blank Field -> #
        else:
            errors['login']="username/password is incorrect"

        return errors

# <--- Validate User Registration---> #
    def validate_registration(self,post_data):
        errors={}
        for field,value in post_data.items():
            # <- Blank Entry -> #
            if len(value)<1:
                errors[field]="{} field is required".format(field.replace('_',' '))
            # <- Name Length & Alpha Format -> #
            if field == "name":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',' '))
                elif not field in errors and not re.match(NAME_REGEX,post_data[field]):
                    errors[field]="Invalid characters in {} field".format(field.replace('_',' '))
            # <- Password Length & Match-> #
            if field == "password":
                if not field in errors and len(value) <8:
                    errors[field]="{} field must be at least 8 characters".format(field.replace('_',' '))
                elif post_data['password'] != post_data['confirmpw']:
                    errors[field]="{} do not match".format(field.replace('_',''))
            # <- username Format & Exists -> #
            if field == "username":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',' '))
                if len(self.filter(username=post_data['username']))> 0:
                    errors[field]= "{} is already in use".format(field)

        return errors

# <--- Create User Account ---> #
    def create_user(self,post_data):
        # <- Encode Password w/ Bcrypt -> #
        hashed= bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt(5))
        new_user= self.create(
            name= post_data['name'],
            username= post_data['username'],
            password= hashed
        )
        return new_user

class User(models.Model):
# <--- User Attributes ---> #
    name= models.CharField(max_length=255)
    username= models.CharField(max_length=255)
    password= models.CharField(max_length=255)

    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()
    # <- Print class attributes -> #
    def __repr__(self):
        return "id:{} name:{} username:{} created_at:{} updated_at:{}".format(self.id,self.name,self.username,self.created_at,self.updated_at)


class PlanManager(models.Manager):
    def validate_plan(self,post_data):
        errors={}
        for field,value in post_data.items():
            # <- Blank Field -> #
            if len(value)<1:
                errors[field]="{} field is required".format(field.replace('_',' '))
            # <- Trip Future -> #
            if field == "start":
                if not field in errors and datetime.strptime(post_data[field], '%Y-%m-%d').date() < datetime.today().date():
                    errors[field]= "Travel Date from should be Future Dated"
            # <- Trip Future -> #
            elif field == "end":
                if not field in errors and datetime.strptime(post_data[field], '%Y-%m-%d').date() < datetime.strptime(post_data['end'], '%Y-%m-%d').date():
                    errors[field]= "Travel End Date must be after Start Date"
        return errors

    def add_plan(self,post_data,planner_id):
        new_plan= self.create(
            dest= post_data['dest'],
            desc= post_data['desc'],
            start= post_data['start'],
            end= post_data['end'],
            planner_id=planner_id,
        )

        return new_plan

    def join_plan(self,plan_id,user_id):
        join_plan=self.get(id=plan_id).companions.add(User.objects.get(id=user_id))

        return join_plan

class Plan(models.Model):
# <--- Plan attributes ---> #
    dest= models.CharField(max_length=255)
    desc= models.TextField()
    start= models.DateTimeField()
    end= models.DateTimeField()

    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    planner=models.ForeignKey(User, related_name="user_plans", null=True)
    companions=models.ManyToManyField(User, related_name="plans", default="")
    objects = PlanManager()
    # <- Print class attributes -> #
    def __repr__(self):
        return "id:{} dest:{} desc:{} start:{} end:{} created_at:{} planner:{}".format(self.id,self.dest, self.desc,self.start,self.end,self.created_at,self.planner_id)
