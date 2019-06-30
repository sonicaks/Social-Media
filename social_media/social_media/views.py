from django.views.generic import TemplateView

class LoggedInPage(TemplateView):
    template_name = 'logged_in.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = 'index.html'