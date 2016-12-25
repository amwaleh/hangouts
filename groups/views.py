from django.shortcuts import render
from django.core.paginator import Paginator
from .group import save_groups, create_groups
from django.conf import settings
from .models import  Groups




def Home(request):
    # set default page to 1
    page = 1
    # set how many records to show per page
    groups_per_page = settings.GROUPS_PER_PAGE

    if request.method == "POST":
        # get the maximum number per group
        groups_of = int(request.POST.get('group'))
        if request.FILES['file']:
            uploaded_file = request.FILES['file']
            for chunk in uploaded_file.chunks():
                data = chunk.decode("utf-8").replace('\"','').replace(" ", "_").split()
        # create groups
        groups = create_groups(data,groups_of)
        # Save the created groups to mongodb
        mongo_result = save_groups(groups)
        paginator = Paginator(groups, groups_per_page)
        content_to_view = paginator.page(page)
        return render (request, context={"context":content_to_view, "id":mongo_result.id, "groups_of": groups_of},template_name="index.html")

    page = int(request.GET.get('page') or 0)
    if page:
        groups = Groups.objects.order_by('-created').first()
        paginator = Paginator(groups.groups, groups_per_page)
        content_to_view = paginator.page(page)
        content = {
            "context":content_to_view,
            "date_generated" : groups.created,
                   }
        return render(request, context=content, template_name="index.html")
    return render (request, template_name="index.html")

def get_collections(request):
    '''
    Gets all the collections in the database
    :param request: request object
    :return: returns a list of all Documents
    '''
    page = int(request.GET.get('page') or 1)

    start = (page-1) * 10
    stop = page * 10
    groups = Groups.objects[start:stop].order_by('-created')
    paginator = Paginator(groups, 10)
    content_to_view = paginator.page(page)
    context = {"context":content_to_view}
    return render(request, context=context, template_name="collections.html")


def get_group(request, id):
    '''
    Function gets a single group
    :param request:
    :param id: the ID of the Document you want to view
    :return: returns the details in the document
    '''
    page = int(request.GET.get('page') or 1)
    groups_per_page = settings.GROUPS_PER_PAGE
    group = Groups.objects.filter(id=id).first()
    paginator = Paginator(group.groups, groups_per_page)
    content_to_view = paginator.page(page)
    content = {
        "context": content_to_view,
        "date_generated": group.created,
        "id":group.id
    }
    return render(request, context=content, template_name="index.html")

def get_whole_list(request,id ):
    page = int(request.GET.get('page') or 1)
    group = Groups.objects.filter(id=id).first()
    groups_per_page = 15
    paginator = Paginator(group.groups, groups_per_page)
    content_to_view = paginator.page(page)

    content = {
        "context": content_to_view,
    }

    return render(request, context=content, template_name="list.html")

