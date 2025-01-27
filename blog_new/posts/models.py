from django.db import models
from django.urls import reverse, reverse_lazy
from ckeditor.fields import RichTextField

from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name = 'Название')
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("category_detail", kwargs={"slug": self.slug})
        # return '/%s/' % self.slug


class Post(models.Model):
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, null=True, verbose_name='Категория')
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, verbose_name = 'Название')
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name='Изображение')
    intro = models.CharField(max_length=255, default='Читать')
    body = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, blank=True, default=None, related_name='likes')
    like_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created_on',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return '/%s/%s/' % (self.category.slug, self.slug)
        return reverse("posts:post_detail", kwargs={"category_slug": self.category.slug, "slug": self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=2200)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    like_count = models.PositiveBigIntegerField(default=0)
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    dislike_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_on',)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.content[:30]}'
        except:
            return f'no author : {self.body[:30]}'

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"category_slug": self.category.slug, "slug": self.slug})


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,)
    parent_reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name="parent_replies", null=True, blank=True)
    level = models.IntegerField(default=1)
    content = models.TextField(max_length=2200)
    likes = models.ManyToManyField(User, related_name='reply_likes')
    like_count = models.PositiveBigIntegerField(default=0)
    dislikes = models.ManyToManyField(User, blank=True, related_name='reply_dislikes')
    dislike_count = models.PositiveBigIntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.content[:30]}'
        except:
            return f'no author : {self.body[:30]}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['created']

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.comment.pk})
