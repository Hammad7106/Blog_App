from django.core.mail import send_mail

def mail(request):

    send_mail(
        'Email Verification',
        'Please Verify your Email',
        'hammadmubeen430@gmail.com',
        ['hadii711175@gmail.com'],
        fail_silently=True,
    )

