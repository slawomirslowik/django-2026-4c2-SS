from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def landingPage(request):
    return HttpResponse("Hello, You're at the polls landing page. Available endpoints: admin, polls")