
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..userprofileupdate import CompositeUpdateForm
@login_required
def profile_update(request):
    user = request.user


    if request.method == 'POST':
        form = CompositeUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
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
