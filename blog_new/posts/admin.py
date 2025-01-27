from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Category, Post, Comment, Reply

@admin.action(description="Mark active")
def make_active(self, request, queryset):
    updated = queryset.update(active=True)
    self.message_user(
        request,
        ngettext(
            "%d object was successfully marked as active.",
            "%d objects were successfully marked as active.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'body']
    list_display = ('title', 'slug', 'category', 'active', 'created_on')
    list_filter = ['category', 'active']
    # inlines = [CommentItemInline]
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = ('created_on')
    actions = [make_active]



class CommentItemInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['post']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_on', 'active']
    list_filter = ('active', 'created_on')
    search_fields = ('author', 'email', 'content')
    list_editable = ('active',)
    actions = [make_active]


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment', 'created', 'active']
    list_filter = ('active', 'created')
    search_fields = ('author', 'email', 'content')
    list_editable = ('active',)
    actions = [make_active]

class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date',)
