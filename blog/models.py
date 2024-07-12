from django.db import models
from django.urls import reverse
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='Category URL', unique=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ['title']
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название тега')
    slug = models.SlugField(max_length=50, verbose_name='Tag URL', unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
        db_table = 'Tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='post URL', unique=True)
    author = models.CharField(max_length=100, verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos\\%Y\\%m\\%d\\', blank=True, verbose_name='Фото',)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Тег')

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'Post'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья', blank=True, null=True)
    author = models.CharField(max_length=80, verbose_name='Имя')
    description = models.TextField(verbose_name='Комментарии')
    to_comment = models.ManyToManyField('Comment', related_name='comments', verbose_name='Комментарии', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    class Meta:
        db_table = 'Comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.author
