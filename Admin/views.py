from django.shortcuts import render

# Create your views here.
def page1(request):
    return render(request, 'dashboard.html')

def page2(request):
    return render(request, 'dshb-courses.html')

def page3(request):
    return render(request, 'dshb-listing.html')