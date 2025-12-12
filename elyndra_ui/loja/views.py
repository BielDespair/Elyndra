from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    lista = ["João", "Maria", "José"]
    template = loader.get_template("loja/index.html")
    context = {"lista": lista}
    return HttpResponse(template.render(context, request))
