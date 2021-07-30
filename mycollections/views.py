from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Collection
from .forms import CollectionTitleFormSet, CollectionForm


class HomePageView(TemplateView):
    template_name = "mycollections/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collections'] = Collection.objects.order_by('id')
        return context


#######################################################################
#                   Collection Views

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'mycollections/collection_detail.html'


class CollectionCreateView(CreateView):
    model = Collection
    template_name = 'mycollections/collection_create.html'
    form_class = CollectionForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(CollectionCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            print("--post--")
            data['titles'] = CollectionTitleFormSet(self.request.POST)
        else:
            print("--not   post--")
            data['titles'] = CollectionTitleFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(CollectionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('collection_detail', kwargs={'pk': self.object.pk})


class CollectionUpdateView(UpdateView):
    model = Collection
    template_name = 'mycollections/collection_create.html'
    form_class = CollectionForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(CollectionUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = CollectionTitleFormSet(self.request.POST, instance=self.object)
        else:
            data['titles'] = CollectionTitleFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(CollectionUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('collection_detail', kwargs={'pk': self.object.pk})


class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'mycollections/confirm_delete.html'
    success_url = reverse_lazy('homepage')
