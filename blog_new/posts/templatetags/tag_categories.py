from django import template
# from users.forms import NewsletterUserSignUpForm

from posts.models import Category


register = template.Library()

@register.simple_tag()
def tag_categories():
    return Category.objects.all()

# @register.inclusion_tag('subscribe.html')
# def show_subscribe_form():
#     form = NewsletterUserSignUpForm()
#     return {'form': form}
