from cloudinary.uploader import upload
from ..signupform import SignUpForm
from ..userprofileform import UserProfileForm
from django.views import View
from django.shortcuts import render, redirect




class SignUpView(View):
    template_name = 'BlogApp/Sign_Up_Form.html'

    def get(self, request, *args, **kwargs):
        user_form = SignUpForm()
        profile_form = UserProfileForm()
        return render(request, self.template_name, {'signupform': user_form, 'userprofileform': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)

            # Upload profile image to Cloudinary
            uploaded_file = request.FILES.get('image_field_name')  # Replace with your image field name
            if uploaded_file:
                result = upload(uploaded_file)
                profile.image = result['secure_url']

            profile.user = user
            profile.save()
            return redirect('login')  # Redirect to a success page

        return render(request, self.template_name, {'signupform': user_form, 'userprofileform': profile_form})

