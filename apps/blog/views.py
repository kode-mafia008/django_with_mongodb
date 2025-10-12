from django.http import HttpResponse

def blog_list(request):
    return HttpResponse("Blog List")