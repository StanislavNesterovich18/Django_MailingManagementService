from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from client.models import Recipient
from mailing.forms import RecipientForm
from mailing.models import Mailing
from mailing.services import send_recipient
from send_messages.models import Message


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = "mailings"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailing/create_mailing.html"
    fields = (
        "status",
        "message",
        "recipients",
        "start_time",
        "end_time",
    )
    success_url = reverse_lazy("mailing:mailing_list")

    def post(self, request, *args, **kwargs):
        list_r = []
        data = request.POST.copy()
        print(data)
        message = data.getlist("message")
        recipients = data.getlist("recipients")
        start_time = data.getlist("start_time")
        end_time = data.getlist("end_time")
        date_time_start = datetime.fromisoformat(start_time[0])
        date_time_end = datetime.fromisoformat(end_time[0])
        if date_time_start > date_time_end:
            context = {"error": "Стартовое время должно быть, больше чем, время завершения рассылки."}
            context["recipients"] = Recipient.objects.all()
            context["messages"] = Message.objects.all()
            return render(request, self.template_name, context, status=400)
        for r in recipients:
            list_r.append(Recipient.objects.get(pk=int(r)))
        obj_maling = Mailing.objects.create(
            message=Message.objects.get(pk=int(message[0])),
            start_time=start_time[0],
            end_time=end_time[0],
            owner=request.user,
        )
        obj_maling.recipients.add(*list_r)
        data_time_now = datetime.now()
        if date_time_start <= data_time_now <= date_time_end:
            send_recipient(obj_maling)
        print(message, recipients, start_time, end_time, list_r)
        return redirect("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipients"] = Recipient.objects.all()
        context["messages"] = Message.objects.all()
        return context




class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = (
        "status",
        "message",
        "recipients",
        "start_time",
        "end_time",
    )
    success_url = reverse_lazy("mailing:mailing_list")
    context_object_name = "mailing"
    template_name = "mailing/update_mailing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipients"] = Recipient.objects.all()
        context["messages"] = Message.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        list_r = []
        self.object = self.get_object()
        data = request.POST.copy()
        print(data)
        message = data.getlist("message")
        recipients = data.getlist("recipients")
        for r in recipients:
            list_r.append(Recipient.objects.get(pk=int(r)))
        self.object.message = Message.objects.get(pk=int(message[0]))
        self.object.save()

        self.object.recipients.clear()
        self.object.recipients.add(*list_r)

        print(message, recipients, list_r)
        return redirect("mailing:mailing_list")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")
    context_object_name = "mailing"
    template_name = "mailing/delete_mailing.html"


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    context_object_name = "mailing"
    template_name = "mailing/detail_mailing.html"

class MailingStartDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    context_object_name = "mailings"
    template_name = "mailing/mailing_list.html"

    def get_context_data(self, **kwargs):
        context = super(MailingStartDetailView, self).get_context_data(**kwargs)
        obj_id = self.kwargs.get("pk", None)
        mailing = Mailing.objects.filter(pk=obj_id).first()
        context["mailings"] = Mailing.objects.all()
        send_recipient(mailing)
        return context




class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Создание получателя"""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        """При успешной валидации формы"""
        messages.success(self.request, f"Получатель {form.instance.email} успешно создан!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """При ошибке валидации формы"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование получателя"""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):
        messages.success(self.request, f"Получатель {form.instance.email} успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя"""

    model = Recipient
    template_name = "recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Получатель успешно удален!")
        return super().delete(request, *args, **kwargs)


class RecipientListView(LoginRequiredMixin, ListView):
    """Список получателей"""

    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Поиск по email или ФИО
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                models.Q(email__icontains=search_query) | models.Q(full_username__icontains=search_query)
            )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о получателе"""

    model = Recipient
    template_name = "recipient_detail.html"
    context_object_name = "recipient"
