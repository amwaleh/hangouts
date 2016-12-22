from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .group import create_groups
# Create your views here.

def Home(request):
    paginator = Paginator(create_groups(8), 6)
    page=request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render (request, context={"context":users},template_name="index.html")