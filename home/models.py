from django.db import models
#from allauth.account.forms import LoginForm
from wagtail.models import Page


class HomePage(Page):
    pass
    # def serve(self, request, *args, **kwargs):
    #     response = super().serve(request, 'cms/article_page.html')
    #     response.context_data['login_form'] = LoginForm()
    #     return response
