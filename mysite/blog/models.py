from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    '''Создание модельных менеджеров'''
    '''По умолчанию в каждой модели используется менеджер objects. Этот менеджер извлекает все объекты из базы данных.
        Однако имеется возможность
        определять конкретно-прикладные модельные менеджеры.
        Давайте создадим конкретно-прикладной менеджер, чтобы извлекать все 
    посты, имеющие статус PUBLISHED.'''
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        """Очень часто в функциональность ведения блогов входит хранение постов
            в виде черновика до тех пор, пока они не будут готовы к публикации. Мы
            добавим в модель поле статуса, которое позволит управлять статусом постов
            блога. В постах будут использоваться статусы Draft (Черновик) и Published
        (Опубликован)"""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    # Теперь при использовании параметра unique_for_date поле slug должно
    # быть уникальным для даты, сохраненной в поле publish. Обратите внимание,
    # что поле publish является экземпляром класса DateTimeField, но проверка на
    # уникальность значений будет выполняться только по дате
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish') # генерируем уникальный slug
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, # Параметр on_delete определяет поведение, которое следует применять при удалении объекта, на который есть ссылка. Это поведение не относится конкретно к Django; оно является стандартным для SQL. Использование ключевого слова CASCADE указывает на то, что при удалении пользователя, на которого есть ссылка, база данных также удалит все связанные с ним посты в блоге
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # Поле с типом DateTimeField, которое транслируется в столбец DATETIME в базе данных SQL. Оно будет использоваться для хранения даты и времени публикации поста
    created = models.DateTimeField(auto_now_add=True)   # При применении параметра auto_now_add дата будет сохраняться автоматически во время создания объекта
    updated = models.DateTimeField(auto_now=True) #  Оно будет использоваться для хранения последней даты и времени обновления поста. При применении параметра auto_now дата будет обновляться автоматически во время сохранения объекта
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер
    tags = TaggableManager()  # Менеджер tags позволит добавлять, извлекать и удалять теги из объектов Post

    class Meta:
        """Посты блога обычно отображаются на странице в обратном хронологическом
            порядке (от самых новых к самым старым). В нашей модели мы определим
            заранее заданный порядок. Он будет применяться при извлечении объектов
        из базы данных, в случае если в запросе порядок не будет указан."""
        ordering = ['-publish']
        """Давайте определим индекс базы данных по полю publish. Индекс повысит 
            производительность запросов, фильтрующих или упорядочивающих результаты по указанному полю. Мы ожидаем, что многие запросы извлекут преимущества из этого индекса, поскольку для упорядочивания результатов мы 
        по умолчанию используем поле publish"""
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Функция reverse() будет формировать URL-адрес динамически, применяя
        # имя URL-адреса, определенное в шаблонах URL-адресов. Мы использовали именное пространство blog,
        # за которым следуют двоеточие и URL-адрес
        # post_detail
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
