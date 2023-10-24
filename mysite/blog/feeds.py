import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    # В приведенном выше исходном коде мы определили новостную ленту,
    # создав подкласс класса Feed фреймворка синдицированных новостных лент.
    # Атрибуты title, link и description соответствуют элементам RSS <title>,
    # <link> и <description> в указанном порядке.
    # Функция-утилита reverse_lazy() используется для того, чтобы генерировать
    # URL-адрес для атрибута link. Метод reverse() позволяет формировать
    # URL-адреса по их имени и передавать опциональные параметры.
    title = 'Мой блог'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title
    #  методе item_description() используется функция markdown()
    #  чтобы конвертировать контент в формате Markdown в формат HTML,
    #  и функция шаблонного фильтра truncatewords_html(),
    #  чтобы сокращать описание постов
    # после 30 слов, избегая незакрытых HTML-тегов

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
