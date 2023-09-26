from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.models import CustomUser, Courses, SessionYearModel
from .EmailBackEnd import EmailBackEnd
from .validators import validate_email_address, handle_password_validation, handle_user_error


def showDemoPage(request):
    return render(request,"demo.html")


def ShowLoginPage(request):
    if not request.user.is_authenticated:
        return render(request,"login_page.html")
    else:
        return render(request, "logout.html")


def show_signup_page(request):
    if not request.user.is_authenticated:
        return render(request, "signup_page.html")
    else:
        return render(request, "logout.html")


def doLogin(request):
    if not request.user.is_authenticated:
        if request.method != "POST":
            return HttpResponse("<h2>Method Not Allowed</h2>")
        else:
            email = request.POST.get("email")
            password = request.POST.get("password")

            email_backend = EmailBackEnd()
            user = email_backend.authenticate(request=None, username=email, password=password)

            if user is not None:
                login(request, user)
                if user.user_type == "1":
                    return HttpResponseRedirect('/admin_home')
                elif user.user_type == "2":
                    return HttpResponseRedirect(reverse("staff_home"))
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                messages.error(request, "Invalid Login Details")
                return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


def Testurl(request):
    return HttpResponse("Ok")


def signup_admin(request):
    if not request.user.is_authenticated:
        return render(request,"signup_admin_page.html")
    else:
        return render(request, "logout.html")


def signup_student(request):
    if not request.user.is_authenticated:
        courses=Courses.objects.all()
        session_years=SessionYearModel.object.all()
        return render(request,"signup_student_page.html",{"courses":courses,"session_years":session_years})
    else:
        return render(request, "logout.html")


def signup_staff(request):
    if not request.user.is_authenticated:
        return render(request,"signup_staff_page.html")
    else:
        return render(request, "logout.html")


def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    # password, email and user validation stuffs
    if not validate_email_address(email):
        messages.error(request, "Email is not valid.")
        return HttpResponseRedirect(reverse("signup_admin"))

    password_error = handle_password_validation(password=password)
    if password_error:
        messages.error(request, password_error)
        return HttpResponseRedirect(reverse("signup_admin"))

    user_error = handle_user_error(email, username)
    if user_error:
        messages.error(request, user_error)
        return HttpResponseRedirect(reverse("signup_admin"))

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))

    except:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))


def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    # password, email and user validation stuffs
    if not validate_email_address(email):
        messages.error(request, "Email is not valid.")
        return HttpResponseRedirect(reverse("signup_staff"))

    password_error = handle_password_validation(password=password)
    if password_error:
        messages.error(request, password_error)
        return HttpResponseRedirect(reverse("signup_staff"))

    user_error = handle_user_error(email, username)
    if user_error:
        messages.error(request, user_error)
        return HttpResponseRedirect(reverse("signup_staff"))

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))


def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")
    try:
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
    except:
        profile_pic_url = "/media/default.png"

    # password, email and user validation stuffs
    if not validate_email_address(email):
        messages.error(request, "Email is not valid.")
        return HttpResponseRedirect(reverse("signup_student"))

    password_error = handle_password_validation(password=password)
    if password_error:
        messages.error(request, password_error)
        return HttpResponseRedirect(reverse("signup_student"))

    user_error = handle_user_error(email, username)
    if user_error:
        messages.error(request, user_error)
        return HttpResponseRedirect(reverse("signup_student"))

    user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                          first_name=first_name, user_type=3)
    user.students.address = address
    course_obj = Courses.objects.get(id=course_id)
    user.students.course_id = course_obj
    session_year = SessionYearModel.object.get(id=session_year_id)
    user.students.session_year_id = session_year
    user.students.gender = sex
    user.students.profile_pic = profile_pic_url
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
