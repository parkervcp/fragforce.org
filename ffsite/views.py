from django.shortcuts import render


def home(request):
    """ Home page """
    return render(request, 'ff/root/home.html', {})


def donate(request):
    """ How to donate page """
    return render(request, 'ff/root/donate.html', {})


def join(request):
    """ How to join ff page """
    return render(request, 'ff/root/join.html', {})


def contact(request):
    """ Contact page """
    return render(request, 'ff/root/contact.html', {})
