from django.views.generic import DetailView, ListView

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        return Project.objects.filter(status=Project.Status.PUBLISHED)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(status=Project.Status.PUBLISHED)
