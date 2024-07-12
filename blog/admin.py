from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

class PostAdminForm(forms.ModelForm):
    """Форма CKEditor"""
    content = forms.CharField(widget=(CKEditorUploadingWidget), label='Контент')
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post) #регистрирует модель в админке заместо admin.site.register(Category, PostAdmin)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} #создается слаг на основе тайтла
    form = PostAdminForm #подключаем скедитор
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'get_photo', 'views')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category','tags', 'created_at')
    readonly_fields = ('views','created_at', 'get_photo')
    fields = ('title', 'slug', 'author', 'category', 'tags', 'content', 'photo', 'get_photo', 'created_at',)

    def get_photo(self, obj):
        """Показывает в админке миниатюрное фото которое мы выбрали"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'
    get_photo.short_description = 'Фото'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} 

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_at', 'author')

