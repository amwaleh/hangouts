from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .group import create_groups, save_groups, read_from_file
from django.conf import settings
# Create your views here.
from .models import  Groups

def Home(request):
    # set default paage to 1
    page = 1
    # Get how many records to show per page 
    groups_per_page = settings.GROUPS_PER_PAGE
    if request.method == "POST":
        # get the maximum number per group
        groups_of = int(request.POST.get('group'))
        # create groups
        groups = read_from_file(groups_of)
        # Save the created groups to mongodb
        mongo_groups = save_groups(groups)
        # paginate the view
        paginator = Paginator(mongo_groups, groups_per_page)
        content_to_view = paginator.page(page)
        return render (request, context={"context":content_to_view, "groups_of": groups_of},template_name="index.html")

    page = request.GET.get('page')
    if page:
        groups = Groups.objects.order_by('-created').first()
        paginator = Paginator(groups.groups, groups_per_page)
        content_to_view = paginator.page(page)
        content = {
            "context":content_to_view,
            "date_generated" : groups.created
                   }
        return render(request, context=content, template_name="index.html")
    return render (request, template_name="index.html")
