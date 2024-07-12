from typing import Any, Dict
from django.views.generic import ListView, DetailView
from blog.models import Post, Category, Tag, Comment
from django.db.models import F
from django.http import JsonResponse

class Home(ListView):
    '''
    Главная страница
    '''
    model = Post
    template_name ='blog\\index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic Blog Design'
        return context
    
class PostsByCategory(ListView):
    '''
    Список постов по категориям
    '''
    template_name ='blog\\index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

class PostsByTag(ListView):
    '''
    Список постов по тэгам
    '''
    template_name ='blog\\index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тэгу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context

class GetPost(DetailView):
    '''Полное описание поста'''
    model = Post
    template_name = 'blog\\single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['comments'] = Comment.objects.filter(post=self.object)
        return context
    
class Search(ListView):
    '''Поиск постов'''
    template_name = 'blog\\search.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context
    
def add_comment(request):
    # Получаем ajax запрос с данными от пользователя и добавляем новый коммент в базу данных.
    if request.POST.get('action') == 'post':
        post_id = int(request.POST.get('post_id'))
        post_author = str(request.POST.get('post_author'))
        post_description = str(request.POST.get('post_description'))

        post = Post.objects.get(id=post_id)
        comment = post.comments.create(author=post_author, description=post_description)
        comment.save()

        response = JsonResponse({"post_id": post_id, "post_author": post_author, "post_description": post_description})
        return response