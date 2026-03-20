from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category

POSTS_ON_MAIN_PAGE = 5


def get_posts():
    """Вспомогательная функция: возвращает только опубликованные посты."""
    return Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    """Главная страница: показывает 5 последних опубликованных постов."""
    posts = get_posts()[:POSTS_ON_MAIN_PAGE]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author', 'location'),
        pk=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )

    return render(request, 'blog/post_detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница категории: показывает посты выбранной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_posts().filter(category=category)
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'posts': posts
        }
    )
