# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })

from .models import User
from .telegram_utils import get_username_from_telegram
import asyncio
import calendar
from datetime import date, timedelta, datetime

def statistics_view(request):
    query = request.GET.get('query')
    if query:
        all_users = User.objects.filter(id__icontains=query)  # Replace 'name' with the actual field name for username
    else:
        all_users = User.objects.all()

    chart_users = User.objects.exclude(joining_date=None)
    
    month_counts = {month: 0 for month in range(1, 13)}

    for user in chart_users:
        joining_date = user.joining_date
        month = joining_date.month
        month_counts[month] += 1

    monthly_data = [month_counts[month] for month in range(1, 13)]

    
   
    today = date.today()
    last_seven_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    last_seven_days_labels = [day.strftime("%Y-%d-%m") for day in last_seven_days]

    daily_data = []

    for i in range(7):
        date_to_check = today - timedelta(days=i)
        formatted_date = date_to_check.strftime("%Y-%m-%d")
        users_count = User.objects.filter(joining_date=formatted_date).count()
        daily_data.append(users_count)

    daily_data.reverse()

    total_users = all_users.count()
    displayed_users_count = 5  # Number of users displayed per page
    remaining_users = total_users - displayed_users_count

    page = request.GET.get('page')  # Get the page parameter from the URL query parameters
    if page:
        page = int(page)
        offset = (page - 1) * displayed_users_count  # Calculate the offset for the queryset
        users = all_users[::-1][offset:offset + displayed_users_count]  # Fetch the users for the current page
    else:
        page = 1
        users = all_users[::-1][:displayed_users_count]  # Fetch the first 5 users

    usernames = []
    for user in users:
        username = asyncio.run(get_username_from_telegram(user.id))
        #print(username)
        usernames.append(username)

    next_page = page + 1 if remaining_users > displayed_users_count else None  # Calculate the next page number

    context = {
        'total': total_users,
        'user_count': len(users),
        'users': zip(users, usernames),
        'remaining_users': remaining_users,
        'next_page': next_page,
        'monthly_data': monthly_data,
        'daily_data': daily_data,
        'last_seven_days': last_seven_days_labels,
        'query': query
    }
    return render(request, 'index.html', context)

from .telegram_utils import send_message_to_telegram_user
from .telegram_utils import send_message_to_telegram_user_with_image
import tempfile

def send_message_api(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        message = request.POST.get('message')
        image = request.FILES.get('image')

        # Call the function to send the message to the Telegram user
        if image:
            image_data = image.read()
            asyncio.run(send_message_to_telegram_user_with_image(user_id, message, image_data))
        else:
            asyncio.run(send_message_to_telegram_user(user_id, message))

    return render(request, 'index.html')

from .telegram_utils import broadcast_message_to_telegram_users
from .telegram_utils import broadcast_message_to_telegram_users_with_image

def broadcast_message_api(request):
    if request.method == 'POST':
        message = request.POST.get('message')  # Get the message from the form
        all_users = User.objects.all()
       
        chat_ids = [user.id for user in all_users]
        
        image = request.FILES.get('image')

        if image:
            image_data = image.read()
            asyncio.run(broadcast_message_to_telegram_users_with_image(message, chat_ids, image_data))
        else:
            # Call the function to send the message to the Telegram users
            asyncio.run(broadcast_message_to_telegram_users(message, chat_ids))

        # Optionally, you can perform any additional logic or redirect to another page
        
    return render(request, 'index.html')