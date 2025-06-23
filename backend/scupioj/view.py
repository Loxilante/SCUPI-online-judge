from django.shortcuts import render
def rootView(request):
    return render(request, 'index.html')
