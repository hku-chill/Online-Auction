from django.shortcuts import render, HttpResponse
from .models import category

# Create your views here.
def index(request):
    return HttpResponse("selam_bebeq")


def get_category_list(request):
    list_category = category.objects.all()
    return render(request, 'auction/category_list.html', {'list_category': list_category})


def get_category(request, slug=None):
    return HttpResponse(slug)
    if not slug == None:
        try:
           test = category.objects.get(slug=slug)
           print(test.image)
           return HttpResponse("category")
           
        except print(0):
            pass
    else:
        return HttpResponse("category")
