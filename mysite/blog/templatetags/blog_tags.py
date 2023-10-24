import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


@register.simple_tag
# В функцию был добавлен декоратор @register.simple_tag,
# чтобы зарегистрировать ее как простой тег
def total_posts():
    # мы создали простой шаблонный тег, который возвращает число опубликованных
    # в блоге постов
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
# В приведенном выше исходном коде мы зарегистрировали шаблонный
# тег, применяя декоратор @register.inclusion_tag. Используя blog/post/latest_posts.html,
# был указан шаблон, который будет прорисовываться возвращенными значениями. Шаблонный тег будет принимать опциональный
# параметр count, который по умолчанию равен 5. Этот параметр позволит
# задавать число отображаемых постов. Данная переменная используется для
# того, чтобы ограничивать результаты запроса Post.published.order_by('-publish')[:count]
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
# функции annotate() формируется набор запросов QuerySet,
# чтобы агрегировать общее число комментариев к каждому посту.
# Функция агрегирования Count используется для
# сохранения количества комментариев в вычисляемом поле total_comments по
# каждому объекту Post.
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
        ).order_by('-total_comments')[:count]


#  Создание конкретно-прикладных шаблонных тегов и фильтров
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
