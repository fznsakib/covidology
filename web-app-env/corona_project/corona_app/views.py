from django.shortcuts import render

def corona_app(request):
    return render(request, 'corona_app.html', {})
