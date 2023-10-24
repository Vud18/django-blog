from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """Мы определили первую форму Django. Форма EmailPostForm наследует от
        базового класса Form. Мы используем различные типы полей,
         чтобы выполнять валидацию данных в соответствии с ними"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    # представление, позволяющее
    # пользователям выполнять поиск постов.
    query = forms.CharField()

