from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """Мы сообщаем сайту администрирования, что модель зарегистрирована на
            сайте с использованием конкретно-прикладного класса, который наследует
    от ModelAdmin. В этот класс можно вставлять информацию о том, как показывать модель на сайте и как с ней взаимодействовать"""
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}  #Заполение поля slug из поля title
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
