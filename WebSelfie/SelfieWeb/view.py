from django.http import HttpResponse
 
def get(request):
    return HttpResponse("Hello world ! ")