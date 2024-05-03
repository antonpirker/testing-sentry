import random

from django.core.cache import cache
from django.shortcuts import render


def index(request):
    context = {
        "items": [str(hash(str(x)))*10 for x in random.sample(range(1, 100), 20)],
    }

    # Low level Django caching API
    cache.set("X1", str(hash("X1"))*10)
    cache.set("X2", str(hash("X2"))*10)
    cache.set("X3", str(hash("X3"))*10)
    cache.get_many(["X1", "X2", "X3"])
    cache.set_many({"Y1": str(hash("Y1"))*10, "Y2": str(hash("Y2"))*10, "Y3": str(hash("Y3"))*10})
    cache.get("Y1")
    cache.get("Y2")
    cache.get("Y3")
    cache.get_many(["Z1", "Z2"])

    # Will use Django caching in the templates
    return render(request, "index.html", context)
