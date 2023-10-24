from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # Новый шаблон URL-адреса, определенный с помощью функции include,
    # ссылается на шаблоны URL-адресов, определенные в приложении blog,
    # чтобы они были включены в рамки пути blog/. Указанные шаблоны вставляются
    # в рамки именного пространства blog
    path('blog/', include('blog.urls', namespace='blog')),
    # В приведенном выше исходном коде были вставлены необходимые инструкции импорта
    # и определен словарь sitemaps. На сайте может быть определено несколько карт.
    # Мы определили шаблон URL-адреса, который совпадает с шаблоном
    # sitemap.xml и в котором используется встроенное в Django
    # представление sitemap. Словарь sitemaps передается в представление sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
