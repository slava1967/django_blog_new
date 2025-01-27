from django.urls import path

# from posts.views import IndexView

from main import views

app_name = 'main'

urlpatterns = [
    # path('', IndexView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('subscribe/', views.newsletter_signup, name='subscribe'),
    path('subscribe-success/', views.NewsletterSignUpSuccessView.as_view(), name='subscribe_success'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact-success/', views.ContactSuccessView.as_view(), name='contact_success'),
]
