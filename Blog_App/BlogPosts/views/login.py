

from datetime import datetime, timedelta

from django.contrib.auth import authenticate,login

from django.contrib import messages

from django.shortcuts import render, redirect



def Signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user is restricted and restriction duration has passed
        if 'restriction_start_timestamp' in request.session:
            restriction_duration = timedelta(minutes=1)  # Adjust as needed
            restriction_start_timestamp = request.session['restriction_start_timestamp']
            restriction_end_timestamp = restriction_start_timestamp + restriction_duration.total_seconds()
            current_timestamp = datetime.now().timestamp()

            if current_timestamp < restriction_end_timestamp:
                remaining_time = int(restriction_end_timestamp - current_timestamp)
                return render(request, "Blog_App/postlist.html", {'user_under_restriction': True, 'remaining_time_in_seconds': remaining_time})

            # If the restriction duration has passed, remove the session variable
            del request.session['restriction_start_timestamp']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.pop('failed_attempts', None)  # Reset failed attempts upon successful login
            return render(request, "BlogApp/postlist.html")
        else:
            if 'failed_attempts' not in request.session:
                request.session['failed_attempts'] = 0

            request.session['failed_attempts'] += 1

            if request.session['failed_attempts'] >= 3:
                request.session['restriction_start_timestamp'] = datetime.now().timestamp()  # Store restriction start timestamp
                messages.error(request, "You have attempted wrong credentials multiple times. You are now restricted from entering credentials for 1 minute.")
                return render(request, "BlogApp/login.html", {'user_under_restriction': True, 'remaining_time_in_seconds': 60})  # 180 seconds = 3 minutes

            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, "BlogApp/login.html", {'user_under_restriction': False})

