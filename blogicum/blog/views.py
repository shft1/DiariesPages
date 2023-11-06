from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from .constans import LIMIT


def get_published_posts(manager=Post.objects):
    return manager.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    post_list = Post.published.select_related(
        'author', 'location', 'category'
    ).order_by('-pub_date')[:LIMIT]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_published_posts(), pk=id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = get_published_posts(category.categorized_records.all())
    context = {'post_list': post_list, 'category': category}
    return render(request, template, context)
