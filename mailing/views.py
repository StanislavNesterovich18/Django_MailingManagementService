from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from client.models import Recipient
from mailing.forms import RecipientForm
from mailing.models import Mailing
from send_messages.models import Message


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = "mailings"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailing/create_mailing.html"
    fields = ('status', 'message', 'recipients',)
    success_url = reverse_lazy("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients'] = Recipient.objects.all()
        context['messages'] = Message.objects.all()
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")
    context_object_name = "mailing"


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")
    context_object_name = "mailing"


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    context_object_name = "mailing"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Создание получателя"""
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        """При успешной валидации формы"""
        messages.success(self.request, f'Получатель {form.instance.email} успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """При ошибке валидации формы"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование получателя"""
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        messages.success(self.request, f'Получатель {form.instance.email} успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя"""
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Получатель успешно удален!')
        return super().delete(request, *args, **kwargs)


class RecipientListView(LoginRequiredMixin, ListView):
    """Список получателей"""
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Поиск по email или ФИО
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                models.Q(email__icontains=search_query) |
                models.Q(full_username__icontains=search_query)
            )

        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о получателе"""
    model = Recipient
    template_name = 'recipient_detail.html'
    context_object_name = 'recipient'
