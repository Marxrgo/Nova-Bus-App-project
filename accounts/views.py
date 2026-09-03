from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def account_home(request):
    return render(request, "accounts/account_home.html")
