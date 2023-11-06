from django.db import models
from django.contrib.auth import get_user_model
from .constans import max_len
from .managers import PublishedManager


User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(max_length=max_len, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Category(BaseModel):
    title = models.CharField(max_length=max_len, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True, verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы '
        'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Post(BaseModel):
    objects = models.Manager()
    published = PublishedManager()
    title = models.CharField(max_length=max_len, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в '
        'будущем — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, verbose_name='Категория', related_name='categorized_records'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('id',)

    def __str__(self):
        return self.title
