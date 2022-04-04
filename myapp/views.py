from nntplib import ArticleInfo
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
#Django

import os
import random
from datetime import datetime
#python

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
#firebase

db_url = "https://smartfarm-28dd5-default-rtdb.firebaseio.com/"
cred = credentials.Certificate(os.getcwd() + '/myapp/serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred, {'databaseURL':db_url})
#firebase

Time = ["Day", "Night"]
current_time = datetime.now()
if 7 <= current_time.hour and current_time.hour <= 19 :
    Now_Time = Time[0]
else : 
    Now_Time = Time[1]
#global var

@csrf_exempt
def index(request): 
    global Now_Time
    ref = db.reference('DB/Status')
    dir = ref.get()
    
    if 7 <= current_time.hour and current_time.hour <= 19 :
        Now_Time = Time[0]
    else : 
        Now_Time = Time[1]

    if request.method == 'GET':
        context = {
            'Body_Time' : 'body_' + Now_Time,
            'Section_Time' : 'Section_' + Now_Time,
            'Humid_value' : dir['Humid'], 
            'Temp_value' : dir['Temp'],
            'Co2_value' : dir['Co2'],
            'Fans_value' : dir['Fans'],
        }
        return render(request, 'myproject/index.html', context)

@csrf_exempt
def edit(request):
    global Now_Time
    if request.method == 'GET':
        Time_Key = request.GET.get('Time')

        if Time_Key in Time :
            Now_Time = request.GET['Time']

        dir = db.reference('DB/' + Now_Time).get()

        context = {
            'Body_Time' : 'body_' + Now_Time,
            'Section_Time' : 'Section_' + Now_Time,
            'Humid_value' : dir['Humid'], 
            'Temp_value' : dir['Temp'],
            'Co2_value' : dir['Co2'],
        }
        return render(request, 'myproject/edit.html',context)
    elif request.method == 'POST':
        ref = db.reference('DB/' + Now_Time)
        dir = ref.get()

        arr = {"Humid" : 0,"Temp" : 0,"Co2" : 0}
        for key in arr :
            if(request.POST[key] != '') :
                arr[key] = int(request.POST[key])
            else :
                arr[key] = dir[key]
        ref.update(arr)
        return redirect(request.get_full_path()) 
