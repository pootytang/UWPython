from django.shortcuts import render_to_response as r2r

def index(request):
    title = "Main Page"
    return r2r('main/index.html', {'title': title})
