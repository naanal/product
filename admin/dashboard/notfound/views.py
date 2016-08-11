from django.shortcuts import render


def noendpoint(request):
    context = {'title': 'Server Unavailable', 
    'reason' : 'Server/Endpoint Not Found',
    'description': "Sorry, We can't find any authentication endpoint. You either not configured the server or server stopped running :( ",
    'solution' : "Make Sure Apache Server is Running and Endpoint is configured correctly"}
    return render(request, 'notfound/index.html', context)


def keystonegone(request):
    context = {'title': 'Authentication Unavailable',
    'reason' : 'I THINK I AM LOST',
    'description': "Sorry, There is some serious problem in Authentication mechanism. You are not able to login now. ",
    'solution': "However You may find root cause from below links :"}
    return render(request, 'notfound/index.html', context)
