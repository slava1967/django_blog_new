from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from .forms import ContactForm, NewsletterUserSignUpForm
from users.models import NewsletterUser

from posts.models import Post


class IndexView(ListView):
    model = Post
    template_name = "main/index.html"
    paginate_by = 2
    queryset = Post.objects.filter(active='True').order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["title"] = "Home - Каталог"
        context["slug_url"] = self.kwargs.get("category_slug")
        return context

class SearchView(ListView):
    context_object_name = 'posts'
    model = Post
    template_name = 'main/search.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        posts = Post.objects.filter(active=True).filter(Q(title__icontains=query) | Q(body__icontains=query))
        return posts

    def get_context_data(self, *args, **kwargs):
        query = self.request.GET.get('query')
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context["query"] = query
        return context


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterUserSignUpForm()
        newsletter_user = NewsletterUser.objects.create(
            email=request.POST['email'],
        )
        messages.success(request, f'Вы подписаны на рассылку новостей!', extra_tags='subscribe')
        return render(request, 'main/messages.html')
    else:
        form = NewsletterUserSignUpForm()
    return render(request, 'main/subscribe.html', {'form': form})


class NewsletterSignUpSuccessView(TemplateView):
    template_name = 'main/subscribe-success.html'


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')

        full_message = f"""
                    Получено письмо через контактную форму сайта pythonframeworkf.ru
                            От: {name},
                            E-mail: {email},
                            Тема: {subject}
                    ________________________


                    {message}
                    """

        send_mail(
            subject="Получено письмо через контактную форму сайта pythonframeworkf.ru",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'main/contact-success.html'


def robots_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")
