import random

from django.core.cache import cache
from django.shortcuts import render


def index(request):
    context = {
        "items": random.sample(range(1, 100), 20),
    }

    # cache.set("X1", 1)
    # cache.set("X2", 2)
    # cache.set("X3", 3)
    # cache.get_many(["X1", "X2", "X3"])
    # cache.set_many({"Y1": 1, "Y2": 2, "Y3": 3})
    # cache.get("Y1")
    # cache.get("Y2")
    # cache.get("Y3")
    # cache.get_many(["Z1", "Z2"])

    return render(request, "index.html", context)
