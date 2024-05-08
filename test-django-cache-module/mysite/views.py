import random

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render

LEN = 15

def index(request):
    context = {
        "items": [str(hash(str(x)))*LEN for x in random.sample(range(1, 100), 20)],
    }

    # Low level Django caching API
    cache.get_many(["X1", "X2", "X3"])
    cache.set("X1", str(hash("X1"))*LEN)
    cache.set("X2", str(hash("X2"))*LEN)
    cache.get_many(["X1", "X2", "X3"])
    
    cache.set_many({"Y1": str(hash("Y1"))*LEN, "Y2": str(hash("Y2"))*LEN, "Y3": str(hash("Y3"))*LEN})
    cache.get("Y1")
    cache.get("Y2")
    cache.get("Y3")

    # Low level Django caching API
    cache.get_many(["S1", "S2", "S3"])
    cache.set("S1", "Sensitive1")
    cache.set("S2", "Sensitive2")
    cache.get_many(["X1", "X2", "X3"])
    
    cache.set_many({"SS1": "Super Sensitive1", "SS2": "Super Sensitive2", "SS3": "Super Sensitive3"})
    cache.get("SS1")
    cache.get("SS2")
    cache.get("SS3")

    # This will use Django caching in the templates
    return render(request, "index.html", context)

    # No caching in the templates
    # return HttpResponse("Hello, world.")
