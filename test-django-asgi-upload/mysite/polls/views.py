from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def _handle_uploaded_file(f):
    with open("uploaded.png", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def fileupload(request):
    if request.method == "POST":
        _handle_uploaded_file(request.FILES["upload"])
        return HttpResponse("File received. Thank you!")

    return HttpResponse("File Upload View. POST something.")

