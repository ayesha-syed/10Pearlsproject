from django.shortcuts import render
from django.http import HttpResponse
from .forms import Video_form
# Create your views here.
def home(request):
    # form=Video_form()
    form=Video_form(request.POST or None,request.FILES or None)
    # if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>uploaded</h1>")
        else:
            print('shit')

    # if request.method == "POST":
    #     form=Video_form(data=request.POST,files=request.FILES)
    #     if form.is_valid:
    #         # form.save()
    #         return HttpResponse("<h1>uploaded</h1>")
    #     else:
    #         form=Video_form()
    return render(request,'interviewpage.html', {"form":form})

def mainpage(request):
    return render(request,'mainpage.html')