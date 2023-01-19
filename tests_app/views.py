from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'tests_app/home.html'
