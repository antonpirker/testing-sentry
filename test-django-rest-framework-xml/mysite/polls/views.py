from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    1/0
    return HttpResponse("Hello, world. You're at the polls index. Body: %s" % request.body)