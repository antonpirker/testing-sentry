from django.urls import path

import strawberry
from strawberry.django.views import GraphQLView

from . import views


def resolve_hello(root) -> str:
    1/0
    return "Hello world!"

@strawberry.type
class Query:
    hello: str = strawberry.field(resolver=resolve_hello)

schema = strawberry.Schema(Query)


urlpatterns = [
    path("", views.index, name="index"),
    path("fileupload", views.fileupload, name="fileupload"),   
    path("graphql/", GraphQLView.as_view(schema=schema)),
]