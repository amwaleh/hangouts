from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.core.urlresolvers import reverse
from .group import save_groups, create_groups
from .models import Groups
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import RegistratioForm


class UserRegisterView(CreateView):
    form_class = RegistratioForm
    model = User
    template_name = 'register.html'
    success_url = '/'

    def form_valid(self, form):
        """
        override the normal form.save
        this enables us to hash the password
        form.cleaned_data is a dict so change it to kwargs
        :return: redirect to thr success_url
        """
        cpassword = form.cleaned_data.pop('password_confirm')
        if cpassword == form.cleaned_data.get('password'):
            User.objects.create_user(**form.cleaned_data)
            return redirect(self.success_url)

        # add error to the form context
        form.add_error('password_confirm', 'The passwords do not match')
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def Home(request):
    if request.method == "POST":
        # get the maximum number per group
        groups_of = int(request.POST.get('group'))
        if request.FILES['file']:
            uploaded_file = request.FILES['file']
            for chunk in uploaded_file.chunks():
                data = chunk.decode("utf-8").replace('\"', '').replace(" ", "_").split()
        # create groups
        groups = create_groups(data, groups_of)
        # Save the created groups to mongodb
        mongo_result = save_groups(groups)
        return redirect(reverse('group', args=[mongo_result.id]))
    return render(request, template_name="index.html")


@login_required
def get_collections(request):
    """
    Gets all the collections in the mongo database
    :param request: request object
    :return: returns a list of all Documents
    """

    page = int(request.GET.get('page') or 1)
    content_per_page = 10
    start = (page - 1) * content_per_page
    stop = page * content_per_page
    groups = Groups.objects[start:stop].order_by('-created')
    paginator = Paginator(groups, content_per_page)
    content_to_view = paginator.page(page)
    context = {"context": content_to_view}
    return render(request, context=context, template_name="collections.html")


@login_required
def get_group(request, id):
    """
    Function gets a single group
    :param request:
    :param id: the ID of the Document you want to view
    :return: returns the details in the document
    """

    page = int(request.GET.get('page') or 1)
    groups_per_page = settings.GROUPS_PER_PAGE
    group = Groups.objects.filter(id=id).first()
    paginator = Paginator(group.groups, groups_per_page)
    content_to_view = paginator.page(page)
    content = {
        "context": content_to_view,
        "date_generated": group.created,
        "id": group.id
    }
    return render(request, context=content, template_name="index.html")


@login_required
def get_whole_list(request, id):
    """
     Gets a single Document from mongo
    :param request: request object
    :param id: ID of the document to view
    :return: returns a document
    """
    page = int(request.GET.get('page') or 1)
    group = Groups.objects.filter(id=id).first()
    groups_per_page = 15
    paginator = Paginator(group.groups, groups_per_page)
    content_to_view = paginator.page(page)

    content = {
        "context": content_to_view,
    }
    return render(request, context=content, template_name="list.html")
