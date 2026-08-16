
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..userprofileupdate import CompositeUpdateForm
from django.core.mail import send_mail
from ..models import EmailChangeRequest
import uuid
#




# @login_required
# def profile_update(request):
#     user = request.user
#
#
#     if request.method == 'POST':
#         form = CompositeUpdateForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#
#             messages.success(request, 'Your profile has been updated successfully.')
#             return redirect('list')  # Redirect to the same page after update
#     else:
#         initial_data = {
#             'username': user.username,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#
#         }
#         form = CompositeUpdateForm(initial=initial_data, instance=user)
#
#     return render(request, 'BlogApp/profile_update.html', {'userprofileupdate': form})
@login_required
def verify_email_change(request, token):
    try:
        email_change_request = EmailChangeRequest.objects.get(token=token)
        user = email_change_request.user
        user.email = email_change_request.new_email
        user.save()
        email_change_request.delete()
        messages.success(request, 'Your email has been successfully changed.')
        return redirect('list')  # Redirect to the profile update page
    except EmailChangeRequest.DoesNotExist:
        messages.error(request, 'Invalid verification token. Please contact support.')
        return redirect('profile_update')  # Redirect to the profile

@login_required
def profile_update(request):
    user = request.user

    if request.method == 'POST':
        form = CompositeUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']

            if new_email and new_email != user.email:
                token = str(uuid.uuid4())

                # Create an email change request with the token
                EmailChangeRequest.objects.create(user=user, new_email=new_email, token=token)

                # Send verification email
                send_mail(
                    'Confirm Your Email Change',
                    f'Click this link to confirm your email change: {request.build_absolute_uri("/verify-email/")}{token}/',
                    'hammadmubeen430@gmail.com',
                    [new_email],
                    fail_silently=False,
                )

                messages.success(request, 'A verification email has been sent to your new email address. Please check your inbox to confirm the email change.')
                return redirect('list')  # Redirect to the same page after update
            else:
                form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('list')  # Redirect to the same page after update
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = CompositeUpdateForm(initial=initial_data, instance=user)

    return render(request, 'BlogApp/profile_update.html', {'userprofileupdate': form})
