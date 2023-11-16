from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category, Comment
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import PostForm, EditProfileForm, EditPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .constans import COUNT_POST

User = get_user_model()


def get_page_obj(request, list):
    paginator = Paginator(list, COUNT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    post = profile.posts.all().order_by(
        '-pub_date'
    ).annotate(comment_count=Count('comments'))
    page_obj = get_page_obj(request, post)
    context = {'profile': profile, 'post': post, 'page_obj': page_obj}
    return render(request, template, context)


def get_published_posts(manager=Post.objects):
    return manager.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    post_list = Post.published.select_related(
        'author', 'location', 'category'
    ).order_by('-pub_date').annotate(comment_count=Count('comments'))
    page_obj = get_page_obj(request, post_list)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, pk=id)
    if request.user != post.author:
        post = get_object_or_404(
            get_published_posts(), pk=id
        )
    form = CommentForm(request.POST)
    comments = post.comments.all()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = get_published_posts(
        category.posts.all()
    ).order_by('-pub_date').annotate(comment_count=Count('comments'))
    page_obj = get_page_obj(request, post_list)
    context = {
        'post_list': post_list,
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def create_post(request):
    form = PostForm(
        request.POST or None, files=request.FILES or None
    )
    context = {'form': form}
    if not form.is_valid():
        return render(request, 'blog/create.html', context)
    else:
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user.username)


@login_required
def edit_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    form = EditProfileForm(request.POST or None, instance=user)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', context)


@login_required
def edit_post(request, post_id):
    template = 'blog/create.html'
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = EditPostForm(request.POST or None, instance=post)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        return redirect('blog:post_detail', post_id)
    else:
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        return redirect('blog:index')
    form = CommentForm(request.POST or None, instance=comment)
    context = {
        'form': form,
        'comment': comment,
        'post_id': post_id
    }
    if form.is_valid():
        form.save()
    return render(request, template, context)


def delete_post(request, post_id):
    template = 'blog/create.html'
    instance = get_object_or_404(Post, pk=post_id)
    if request.user != instance.author and not request.user.is_superuser:
        return redirect('blog:index')
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, template, context)


def delete_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    instance = get_object_or_404(Comment, pk=comment_id)
    if request.user != instance.author and not request.user.is_superuser:
        return redirect('blog:index')
    context = {
        'comment': instance,
        'post_id': post_id
    }
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, template, context)
