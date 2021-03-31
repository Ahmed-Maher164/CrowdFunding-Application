from users.forms import RegistraionForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.models import Users
import datetime



# Create your views here.
def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_email(
                user,
                get_current_site(request),
                form.cleaned_data.get("email"),
                "users/account_activation.html",
                "Activate your account.",
            )
            return render(request, "users/sending_email.html", {"active_code": -1})
        else:
            context["form"] = form
    else:
        form = RegistraionForm()
    return render(request, 'users/register.html', {'form': form})

def send_email(user, current_site, email, email_body, email_subject):
    mail_subject = email_subject
    message = render_to_string(
        email_body,
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "time": urlsafe_base64_encode(force_bytes(datetime.datetime.now())),
        },
    )
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

def activate(request, uidb64, time):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("user id : ", uid)
        time_sent = force_text(urlsafe_base64_decode(time))
        user = Users.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        if user.is_active == False:
            email_sent_at = time_sent
            date_diffrince = (
                datetime.datetime.now()
                - datetime.datetime.strptime(email_sent_at,
                                             "%Y-%m-%d %H:%M:%S.%f")
            ).seconds / 60

            if date_diffrince < (24 * 60):
                user.is_active = True
                user.save()
                return render(
                    request, "users/sending_email.html", {"active_code": 1}
                )
            else:
                current_site = get_current_site(request)
                email = user.email
                send_email(
                    user,
                    current_site,
                    email,
                    "users/account_activation.html",
                    "Activate your account.",
                )
                return render(
                    request, "users/sending_email.html", {"active_code": 0}
                )
        else:
            return render(request, "users/sending_email.html", {"active_code": 2})
    else:
        return render(request, "users/sending_email.html", {"active_code": 3})

def login(request):
    form = LoginForm()
    return render(request, 'users/login.html', {'form' : form})


