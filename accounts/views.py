from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from django.conf import settings



@login_required
def account_home(request):
    return render(request, "accounts/account_home.html")

# accounts/views.py
def teacher_access(request):
    if request.method == "POST":
        if request.POST.get("key") == settings.TEACHER_ACCESS_KEY:
            request.session["teacher_access"] = True
            return redirect("latebus:teacher_view")
    return render(request, "accounts/teacher_access.html")