from django.shortcuts import render


def home(request):
    """ Home page """
    return render(request, 'ff/root/home.html', {})
