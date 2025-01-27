from django import template

from main.forms import NewsletterUserSignUpForm

register = template.Library()


@register.inclusion_tag('main/subscribe.html')
def show_subscribe_form():
    form = NewsletterUserSignUpForm()
    return {'form': form}
