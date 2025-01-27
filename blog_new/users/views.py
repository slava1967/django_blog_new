from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from django.contrib.auth import authenticate, login
from posts.models import Post

from posts.views import PostDetailView
from .models import NewsletterUser
from users.forms import UserLoginForm, UserPasswordChangeForm, UserProfileForm, UserRegisterForm

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main:index')

    # def get_success_url(self) -> str:
    #     redirect_page = self.request.POST.get("next", None)
    #     if redirect_page and redirect_page != reverse("user:logout"):
    #         return redirect_page
    #     return reverse_lazy('main:index')

    # def form_valid(self, form):
    #     session_key = self.request.session.session_key

    #     user = form.get_user()

    #     if user:
    #         auth.login(self.request, user)
    #         if session_key:
    #             # delete old authorized user carts
    #             forgot_carts = Cart.objects.filter(user=user)
    #             if forgot_carts.exists():
    #                 forgot_carts.delete()
    #             # add new authorized user carts from anonimous session
    #             Cart.objects.filter(session_key=session_key).update(user=user)

    #             messages.success(self.request, f"{user.username}, Вы вошли в аккаунт!")

    #             return HttpResponseRedirect(self.get_success_url())


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Home - Авторизация'
    #     return context

# class UserInnerLoginView(View):
#     template_name = 'users/login-inner.html'
#     form_class = UserLoginForm

#     def form_valid(self, form):
#         # session_key = self.request.session.session_key

#         user = form.get_user()

#         if user:
#             auth.login(self.request, user)
#             # if session_key:
#                 # delete old authorized user carts
#                 # forgot_carts = Cart.objects.filter(user=user)
#                 # if forgot_carts.exists():
#                 #     forgot_carts.delete()
#                 # # add new authorized user carts from anonimous session
#                 # Cart.objects.filter(session_key=session_key).update(user=user)

#             # messages.success(self.request, f"{user.username}, Вы вошли в аккаунт!")

#             # return HttpResponseRedirect(self.get_success_url())
#             return HttpResponse("<div style='color:green;'>Спасибо! Ваш комментарий отправлен на модерацию</div>")

#     def get(self, request):
#         form = self.form_class()
#         # message = ''
#         return render(request, self.template_name, context={'form': form})

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user:
#                 auth.login(self.request, self.user)
#                 return redirect('home')
#         # message = 'Login failed!'
#         # context = {
#         #     'pk': request.Post.pk,
#         #     'form': form
#         # }
#         # return render(request, 'posts/comments/comment-form.html')
#         return HttpResponse("<div style='color:green;'>Спасибо! Ваш комментарий отправлен на модерацию</div>")

class UserInnerLoginView(LoginView):
    template_name = 'users/login-inner.html'
    form_class = UserLoginForm

    def form_valid(self, form):

        user = form.get_user()

        if user:
            auth.login(self.request, user)

            return HttpResponse(status=204, headers={'HX-Refresh':'true'})

class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        # if session_key:
        #     Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(
            self.request,
            f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт!",
        )
        return HttpResponseRedirect(self.success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'

        # orders = Order.objects.filter(user=self.request.user).prefetch_related(
        #         Prefetch(
        #             "orderitem_set",
        #             queryset=OrderItem.objects.select_related("product"),
        #         )
        #     ).order_by("-id")

        # context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60 * 2)
        return context


# class PasswordsChangeView(PasswordChangeView):
#     form_class = PasswordChangeForm
#     success_url = reverse_lazy('password_success')

#     def get_context_data(self, *args, **kwargs):
#         # cat_menu = Category.objects.all()
#         context = super(PasswordsChangeView, self).get_context_data(*args, **kwargs)
#         # context["cat_menu"] = cat_menu
#         return context


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/registration/change-password.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('users:password_success')


class PasswordChangeSuccess(TemplateView):
    template_name = 'users/registration/password_change_success.html'

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта!")
    auth.logout(request)
    return redirect(reverse("home"))


# def newsletter_signup(request):
#     if request.method == 'POST':
#         form = NewsletterUserSignUpForm()
#         newsletter_user = NewsletterUser.objects.create(
#             email=request.POST['email'],
#         )
#         messages.success(request, f'Вы подписаны на рассылку новостей!', extra_tags='subscribe')
#         return render(request, 'main/messages.html')
#     else:
#         form = NewsletterUserSignUpForm()
#     return render(request, 'users/subscribe.html', {'form': form})


# class NewsletterSignUpSuccessView(TemplateView):
#     template_name = 'users/subscribe-success.html'


# def newsletter_unsubscribe(request):
#     form = NewsletterUserSignUpForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         if NewsletterUser.objects.filter(email=instance.email).exists():
#             NewsletterUser.objects.filter(email=instance.email).delete()
#             messages.success(request, 'Your Email has been removed',
#                              'alert alert-success alert-dismissible'
#                              )
#             subject = 'You have been successfully unsubscribed'
#             from_email = settings.EMAIL_HOST_USER
#             to_email = [instance.email]
#             with open(settings.BASE_DIR / 'users/unsubscribe_email.txt') as f:
#                 signup_message = f.read()
#             message = EmailMultiAlternatives(
#                 subject=subject,
#                 body=signup_message,
#                 from_email=from_email,
#                 to=to_email
#             )
#             html_template = get_template('users/unsubscribe.html').render()
#             message.attach_alternative(html_template, 'text/html')
#             message.send()
#         else:
#             messages.warning(request, 'Your Email does not exist in our database',
#                              'alert alert-warning alert-dismissible'
#                              )

#     context = {
#         'form': form,
#     }
#     return render(request, 'users/unsubscribe.html', context)
