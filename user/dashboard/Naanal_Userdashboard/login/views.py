from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def loginpage(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print (username)
        if username=='shan':
            state='welcome'
            return render_to_response('index.html',{'password':password, 'username': username})
    
    return render_to_response('login.html')

@csrf_exempt
def index_page(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        return render_to_response('index.html',{'password':password, 'username': username})   
    
    return render_to_response('index.html',{'password':password, 'username': username})



def change_password(request):
    username = password = ''
    if request.POST:        
        password = request.POST.get('inputPassword1')
        return render_to_response('changepassword.html',{'password':password, 'username': username})   
    
    return render_to_response('changepassword.html',{'password':password, 'username': username})


def help(request):
    
    
    return render_to_response('help.html')
