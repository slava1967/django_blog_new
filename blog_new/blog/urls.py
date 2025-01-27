from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from blog import settings

from main.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('', include('main.urls', namespace='main')),
    path('', include('posts.urls', namespace='posts')),
    # path('', include('comments.urls', namespace='comments')),
    path('', IndexView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
