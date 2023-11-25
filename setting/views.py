from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'setting/main.html')

def body(request):
    return render(request, 'setting/body.html')

def goal(request):
    return render(request, 'setting/goal.html')

def myinfo(request):
    return render(request, 'setting/myinfo.html')

def withdrawal(request):
    return render(request, 'setting/withdrawal.html')