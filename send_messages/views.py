from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from send_messages.forms import MessageForm
from send_messages.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    """Список сообщений текущего пользователя"""

    model = Message
    context_object_name = "messages"
    template_name = "send_messages/message_list.html"
    paginate_by = 10

    def get_queryset(self):
        """Показываем только сообщения текущего пользователя"""
        queryset = Message.objects.filter(owner=self.request.user)

        # Поиск по теме или телу письма
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                models.Q(subject_letter__icontains=search_query) | models.Q(body_letter__icontains=search_query)
            )

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        context["total_messages"] = self.get_queryset().count()
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""

    model = Message
    form_class = MessageForm
    template_name = "send_messages/message_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        """При успешной валидации сохраняем владельца"""
        form.instance.owner = self.request.user
        messages.success(self.request, f'Сообщение "{form.instance.subject_letter}" успешно создано!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """При ошибке валидации выводим сообщения"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Детальная информация о сообщении"""

    model = Message
    context_object_name = "message"
    template_name = "send_messages/message_detail.html"

    def test_func(self):
        """Проверяем, что пользователь имеет доступ к сообщению"""
        message = self.get_object()
        return self.request.user == message.owner

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет доступа к этому сообщению")
        return redirect("mailing:mailing_list")


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование сообщения"""

    model = Message
    form_class = MessageForm
    template_name = "send_messages/message_form.html"
    success_url = reverse_lazy("send_messages:mailing_list")
    context_object_name = "message"

    def test_func(self):
        """Проверяем, что пользователь имеет доступ к сообщению"""
        message = self.get_object()
        return self.request.user == message.owner

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет доступа к этому сообщению")
        return redirect("mailing:mailing_list")

    def form_valid(self, form):
        messages.success(self.request, f'Сообщение "{form.instance.subject_letter}" успешно обновлено!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление сообщения"""

    model = Message
    template_name = "send_messages/message_confirm_delete.html"
    success_url = reverse_lazy("send_messages:mailing_list")
    context_object_name = "message"

    def test_func(self):
        """Проверяем, что пользователь имеет доступ к сообщению"""
        message = self.get_object()
        return self.request.user == message.owner

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет доступа к этому сообщению")
        return redirect("mailing:mailing_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Сообщение успешно удалено!")
        return super().delete(request, *args, **kwargs)
