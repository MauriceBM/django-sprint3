from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def get_posts():
    return Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')


def index(request):
    posts = get_posts()[:5]
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author', 'location'),
        pk=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )

    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)

    posts = get_posts().filter(category=category)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)
