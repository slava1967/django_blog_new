import time
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import FormView

from .forms import CommentForm, CommentReplyForm

from .models import Category, Post, Comment, Reply


class CategoryPostsView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/category.html'
    paginate_by = 2

    def get_queryset(self):

        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        posts = category.posts.filter(active=True)
        return posts

    # def get_context_data(self, *args, **kwargs):

    #     cat_menu = Category.objects.all()
    #     # category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
    #     context = super(CategoryPostsView, self).get_context_data(*args, **kwargs)
    #     context["cat_menu"] = cat_menu
    #     # context["category"] = category
    #     return context


# class PostDetailView(View):
#     def get(self, request, *args, **kwargs):
#         post = get_object_or_404(Post, slug=kwargs['slug'])
#         context = {'post': post}
#         return render(request, 'posts/post-detail.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post-detail.html'
    context_object_name = 'post'

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, author=request.user, content=content)
            comment.save()

            return HttpResponse("<div style='color:green;'>Спасибо! Ваш комментарий отправлен на модерацию</div>")

        else:
            form = CommentForm()

    def delete(self, pk):
        # comment = Comment.objects.get(id=pk, author=request.user)
        Comment.objects.filter(pk=pk).delete()
        return HttpResponse("<div style='color:green;'>Ваш комментарий удалён</div>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class AddPostLikeView(View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        is_liked = False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user.id)
            post.like_count = post.like_count - 1
            is_liked = False
            post.save()
        else:
            post.likes.add(request.user.id)
            post.like_count = post.like_count + 1
            is_liked = True
            post.save()

        context = {
            'post': post,
            'is_liked': is_liked,
            'like_count': post.like_count
        }

        return render(request, 'posts/post-like.html', context)


class PostCommentsView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'posts/comments/comments-container.html'
    # paginate_by = 2

    def get_queryset(self):
        # category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        # posts = category.posts.filter(active=True)
        post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        comments = post.comments.filter(active=True)
        # post_pk = self.kwargs.get('post_pk')
        # comments = super().get_queryset().filter(post__pk=post_pk, active=True)
        return comments

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = CommentReplyForm()
    #     return context


class CommentDetailView(DetailView):
    model = Comment
    # template_name = 'posts/comments/comment-detail.html'
    # context_object_name = 'comment'

    def get(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        form = CommentReplyForm()
        context = {
            'comment': comment,
            'form': form,
        }

        return render(request, 'posts/comments/comment-detail-detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentReplyForm(request.POST)

        if form.is_valid():
            content = request.POST.get('content')
            reply = Reply.objects.create(comment=comment, author=request.user, content=content)
            reply.save()

            return HttpResponse("<div style='color:green;'>Спасибо! Ваш комментарий отправлен на модерацию</div>")

        else:
            form = CommentReplyForm()


    def delete(self, pk):
        Reply.objects.filter(pk=pk).delete()
        return HttpResponse("<div style='color:green;'>Ваш комментарий удалён</div>")

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['form'] = CommentReplyForm()
    #     return context



# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'posts/post-detail.html'
#     context_object_name = 'post'

#     def post(self, request, pk, *args, **kwargs):
#         post = get_object_or_404(Post, pk=pk)
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             content = request.POST.get('content')
#             comment = Comment.objects.create(post=post, author=request.user, content=content)
#             comment.save()

#             return HttpResponse("<div style='color:green;'>Спасибо! Ваш комментарий отправлен на модерацию</div>")

#         else:
#             form = CommentForm()

#     def delete(self, pk):
#         # comment = Comment.objects.get(id=pk, author=request.user)
#         Comment.objects.filter(pk=pk).delete()
#         return HttpResponse("<div style='color:green;'>Ваш комментарий удалён</div>")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         return context

class AddCommentLike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_liked = False
        for like in comment.likes.all():
            if like == request.user:
                is_liked = True
                break
        if not is_liked:
            comment.likes.add(request.user)
            comment.like_count = comment.like_count + 1

        is_disliked = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                comment.dislikes.remove(request.user)
                comment.dislike_count = comment.dislike_count - 1

            else:
                break

        comment.save()

        context = {
            'comment': comment,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        }
        return render(request, 'posts/comments/comment-like.html', context)


class AddCommentDislike(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_disliked = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_disliked = True
                break
        if not is_disliked:
            comment.dislikes.add(request.user)
            comment.dislike_count = comment.dislike_count + 1

        is_liked = False
        for like in comment.likes.all():
            if like == request.user:
                comment.likes.remove(request.user)
                comment.like_count = comment.like_count - 1

            else:
                break

        comment.save()

        context = {
            'comment': comment,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        }
        return render(request, 'posts/comments/comment-like.html', context)

class CommentRepliesView(ListView):
    model = Reply
    context_object_name = 'replies'
    template_name = 'posts/comments/comment-replies-container.html'
    # paginate_by = 2

    def get_queryset(self):
        # category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        # posts = category.posts.filter(active=True)
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        replies = comment.replies.filter(active=True)
        # post_pk = self.kwargs.get('post_pk')
        # comments = super().get_queryset().filter(post__pk=post_pk, active=True)
        return replies


class CommentReplyDetailView(DetailView):
    model = Reply
    template_name = 'posts/comments/reply-detail.html'
    context_object_name = 'reply'

    # def get(self, request, pk, *args, **kwargs):
    #     reply = Reply.objects.get(pk=pk)
    #     context = {
    #         'reply': reply,
    #     }

    #     return render(request, 'posts/comments/reply-detail.html', context)

    # def post(self, request, id, *args, **kwargs):
    #     comment = Comment.objects.get(id=id)
    #     form = CommentReplyForm(request.POST)

    #     if form.is_valid():
    #         content = request.POST.get('content')
    #         reply = Reply.objects.create(parent_comment=comment, author=request.user, content=content)
    #         reply.save()

    #         return HttpResponse("<div style='color:green;'>Спасибо! Ваш комментарий отправлен на модерацию</div>")

    #     else:
    #         form = CommentReplyForm()

    def delete(self, request, pk):
        # reply = Reply.objects.get(id=pk, author=request.user)
        Reply.objects.filter(pk=pk).delete()
        return HttpResponse("<div style='color:green;'>Ваш комментарий удалён</div>")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = CommentReplyForm()
    #     return context


class AddReplyLike(View):
    def post(self, request, pk, *args, **kwargs):
        reply = Reply.objects.get(pk=pk)

        is_liked = False
        for like in reply.likes.all():
            if like == request.user:
                is_liked = True
                break
        if not is_liked:
            reply.likes.add(request.user)
            reply.like_count = reply.like_count + 1

        is_disliked = False
        for dislike in reply.dislikes.all():
            if dislike == request.user:
                reply.dislikes.remove(request.user)
                reply.dislike_count = reply.dislike_count - 1

            else:
                break

        reply.save()

        context = {
            'reply': reply,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        }
        return render(request, 'posts/comments/reply-like.html', context)


class AddReplyDislike(View):
    def post(self, request, pk, *args, **kwargs):
        reply = Reply.objects.get(pk=pk)

        is_disliked = False
        for dislike in reply.dislikes.all():
            if dislike == request.user:
                is_disliked = True
                break
        if not is_disliked:
            reply.dislikes.add(request.user)
            reply.dislike_count = reply.dislike_count + 1

        is_liked = False
        for like in reply.likes.all():
            if like == request.user:
                reply.likes.remove(request.user)
                reply.like_count = reply.like_count - 1

            else:
                break

        reply.save()

        context = {
            'reply': reply,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        }
        return render(request, 'posts/comments/reply-like.html', context)

# @login_required
# def reply_sent(request, pk):
#     comment = get_object_or_404(Comment, id=pk)
#     replyform = CommentReplyForm()

#     if request.method == 'POST':
#         form = CommentReplyForm(request.POST)
#         if form.is_valid:
#             reply = form.save(commit=False)
#             reply.author = request.user
#             reply.parent_comment = comment
#             reply.save()

#     context = {
#         'reply' : reply,
#         'comment': comment,
#         'replyform': replyform
#     }

#     return render(request, 'snippets/add_reply.html', context)


    # def get_context_data(self, *args, **kwargs):
    #     category_slug = get_object_or_404(Category, slug=self.kwargs.get('slug'))
    #     slug = get_object_or_404(Post, slug=self.kwargs.get('slug'))
    #     post = get_object_or_404(Post, slug=slug)
    #     context = super(PostDetailView, self).get_context_data(*args, **kwargs)
    #     # context["form"] = CommentCreateView().get_form_class()
    #     context["category_slug"] = category_slug
    #     context["slug"] = slug
    #     return context

# def post_comment(request, category_slug, slug, *args, **kwargs):
#         post = Post.objects.get(slug=slug)
#         comments = Comment.objects.filter(post=post, parent=None)
#         form = CommentForm(request.POST)
#         # is_liked = False
#         # if post.likes.filter(id=request.user.id).exists():
#         #     is_liked = True

#         if form.is_valid():
#             content = request.POST.get('content')
#             parent_id = request.POST.get('comment_id')
#             comment_qs = None
#             if parent_id:
#                 comment_qs = Comment.objects.get(id=parent_id)
#             comment = Comment.objects.create(post=post, author=request.user, content=content, parent=comment_qs)
#             comment.save()
#             # context = {
#             #     'post': post,
#             #     # 'is_liked': is_liked,
#             #     'form': form,
#             #     # 'comments': comments,
#             #     'category_slug': get_object_or_404(Category, slug=self.kwargs.get('slug')),
#             #     'slug': get_object_or_404(Post, slug=self.kwargs.get('slug'))
#             # }
#             # messages.success(request, "Спасибо! Ваш комментарий отправлен на модерацию", extra_tags='comment')
#             # return render(request, 'main/messages.html', context)
#             return HttpResponse("<div style='color:green;'>Спасибо! Ваш комментарий отправлен на модерацию</div>")
#             # new_comment = form.save(commit=False)
#             # new_comment.author = request.user
#             # new_comment.post = post
#             # new_comment.save()
#             # messages.success(request, "Спасибо! Ваш комментарий отправлен на модерацию", extra_tags='comment')
#         else:
#             form = CommentForm()
#         # context = {
#         #     'post': post,
#         #     # 'is_liked': is_liked,
#         #     'form': form,
#         #     'comments': comments,
#         # }
#         # return HttpResponseRedirect(post.get_absolute_url())
#         # return redirect('post_detail', category_slug=slug, slug=slug)
#         # return HttpResponse("Спасибо! Ваш комментарий отправлен на модерацию")
#         # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         #     html = render_to_string('main/comments.html', context, request=request)
#         #     return JsonResponse({'form': html})
#         # return render(request, 'main/post-detail.html', context)

#         # return render(request, 'posts/post-detail.html', context)


# class PostLikeView(View):
#     def post(self, request, slug, *args, **kwargs):
#         post = Post.objects.get(slug=slug)
#         is_liked = False
#         if not post.likes.filter(id=request.user.id).exists():
#             post.likes.add(request.user)
#             post.like_count = post.like_count + 1
#             is_liked = True
#             post.save()
#         else:
#             post.likes.remove(request.user)
#             post.like_count = post.like_count - 1
#             is_liked = False
#             post.save()
#         return render(request, 'posts/like-section.html',
#                       context={'post': post, 'like_count': post.like_count, 'is_liked': is_liked})

#     def get_context_data(self, *args, **kwargs):
#         category_slug = get_object_or_404(Category, slug=self.kwargs.get('slug'))
#         context = super(PostLikeView, self).get_context_data(*args, **kwargs)
#         context["category_slug"] = category_slug
#         return context




# def post_like(request):
#     post = get_object_or_404(Post, id=request.POST.get('id'))
#     is_liked = False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user.id)
#         post.like_count = post.like_count - 1
#         is_liked = False
#         post.save()
#     else:
#         post.likes.add(request.user.id)
#         post.like_count = post.like_count + 1
#         is_liked = True
#         post.save()
#     context = {
#         'post': post,
#         'is_liked': is_liked,
#         'like_count': post.like_count

#     }
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         html = render_to_string('main/like_section.html', context, request=request)
#         return JsonResponse({'like-form': html})

# class PostCommentsView(ListView):
#     model = Comment
#     context_object_name = 'comments'
#     template_name = 'posts/comments/comments-container.html'
#     paginate_by = 2

#     def get_queryset(self):

#         post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
#         comments = post.comments.filter(active=True)
#         return comments

#     def get_context_data(self, *args, **kwargs):

#         cat_menu = Category.objects.all()
#         category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
#         context = super(CategoryPostsView, self).get_context_data(*args, **kwargs)
#         context["cat_menu"] = cat_menu
#         context["category"] = category
#         return context

# class CommentRepliesView(ListView):
#     model = Reply
#     context_object_name = 'replies'
#     template_name = 'posts/comments/comments-container.html'
#     paginate_by = 2

#     def get_queryset(self):

#         post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
#         comments = post.comments.filter(active=True)
#         return comments

#     def get_context_data(self, *args, **kwargs):

#         cat_menu = Category.objects.all()
#         category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
#         context = super(CategoryPostsView, self).get_context_data(*args, **kwargs)
#         context["cat_menu"] = cat_menu
#         context["category"] = category
#         return context




# @require_http_methods(['DELETE'])
# def delete_comment(self, request, pk):
#     # category_slug = request.POST.get('category_slug')
#     Comment.objects.filter(pk=pk).delete()
#     #     context = {
# #         'post': post,
# #         'is_liked': is_liked,
# #         'like_count': post.like_count

# #     }
#     return HttpResponse('')

# class CommentDeleteView(DeleteView):
#     model = Comment
#     template_name = 'posts/comments/comment-delete.html'
#     # success_url = reverse_lazy('posts:post_comments')
#     # def delete(request, pk):
#     #     Comment.objects.filter(pk=pk).delete()
#     #     # books = Book.objects.filter(created_by=request.user)
#     #     return HttpResponse()

#     # if request.htmx:
#     #     Comment.objects.filter(pk=pk).delete()
#     # return HttpResponse('')

#     def get_success_url(self):
#         category_slug = self.kwargs['category_slug']
#         slug = self.kwargs['slug']
#         return reverse('posts:post_comments', kwargs={'category_slug': category_slug, 'slug': slug})

#     # def test_func(self):
#     #     post = self.get_object()
#     #     return self.request.user == post.author

#     # def get_context_data(self, *args, **kwargs):

#     #     cat_menu = Category.objects.all()
#     #     category_slug = get_object_or_404(Category, slug=self.kwargs.get('slug'))
#     #     context = super(CategoryPostsView, self).get_context_data(*args, **kwargs)
#     #     context["category_slug"] = category_slug
#     #     context["category"] = category
#     #     return context


