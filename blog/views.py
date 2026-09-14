from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'dashboard.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})


@login_required
@require_POST
def add_comment_htmx(request, slug):
    post = get_object_or_404(Post, slug=slug)
    body = request.POST.get("body", "").strip()
    parent_id = request.POST.get("parent_id")

    if body:
        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                parent_comment = None

        Comment.objects.create(
            post=post,
            author=request.user,
            body=body,
            parent=parent_comment
        )

    comments = Comment.objects.filter(post=post).select_related('author', 'parent').order_by('created_on')
    response = render(request, 'blog/comment_list.html', {
        'post': post,
        'comments': comments,
    })
    response['HX-Trigger'] = 'commentAdded'
    return response


def comment_list(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).select_related('author', 'parent').order_by('created_on')
    return render(request, 'blog/comment_list.html', {
        'post': post,
        'comments': comments,
    })


@login_required
def reply_form(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return render(request, 'blog/reply_form.html', {'comment': comment})


def post_add(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()

        if not title or not body:
            return render(request, 'add_post.html', {'error': 'All fields are required.'})

        post = Post.objects.create(
            title=title,
            body=body,
            author=request.user,
        )
        return redirect('blog:post_detail', slug=post.slug)
    return render(request, "add_post.html")


@login_required
def post_edit(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Post not found")

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()

        if not title or not body:
            return render(request, 'edit_post.html', {"post": post, 'error': "All fields required."})
        post.title = title
        post.body = body
        post.save()
        return redirect("blog:post_detail", slug=post.slug)
    return render(request, "edit_post.html", {"post": post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return redirect('blog:post_list')

    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'components/post_confirm_delete.html', {'post': post})


@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_on')
    return render(request, 'user_posts.html', {'posts': posts})
