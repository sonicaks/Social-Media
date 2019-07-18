from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, RedirectView
from django.contrib import messages
from django.db import IntegrityError
from . import models

# Create your views here.

class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ('name', 'description')
    model = models.Group

class SingleGroup(DetailView):
    model = models.Group

class ListGroups(ListView):
    model = models.Group

class JoinGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs = {'slug' : self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(models.Group, slug = self.kwargs.get('slug'))

        try:
            models.GroupMember.objects.create(user = self.request.user, group = group)
        except IntegrityError:
            messages.warning(self.request, 'Warning alread a member!')
        else:
            messages.success(self.request, 'You are now a member')

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs = {'slug' : self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(user = self.request.user, group__slug = self.kwargs.get('slug')).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group')

        else:
            membership.delete()
            messages.success(self.request, 'You have left the group')

        return super().get(request, *args, **kwargs)