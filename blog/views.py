from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Post,Comment

# show all post
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'dashboard.html', {'posts':posts})

# view a post
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).select_related('author', 'parent').order_by('created_on')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        body = request.POST.get("comment_body", "").strip()
        parent_id = request.POST.get("parent_id")

        if body:
            parent_comment =None
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    parent_comment = None

            Comment.objects.create(
                post =post,
                author = request.user,
                body =body,
                parent = parent_comment
            )
        return redirect('post_detail', slug=post.slug)

    return render(request, 'post_detail.html', {'post':post, 'comments':comments})


# add post
def post_add(request):
    if not request.user.is_authenticated:
        # messages.error(request, 'you must be loged in to add a post')
        return redirect('login')

    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()

        # Validate
        errors = {'error': 'All fields are required.'}
        if not title or not body:
            return render(request, 'add_post.html', errors)

        # create post
        post = Post.objects.create(
            title=title,
            body=body,
            author=request.user,
        )
        post.save()
        return redirect('post_detail',slug=post.slug)
    return render(request,"add_post.html")


# Edit post
@login_required
def post_edit(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Post not found")

    if request.method == 'POST':
        # get the post
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()

        # validate fields
        if not title or not body:
            return render(request, 'edit_post.html', {"post":post, 'error':"All fields requide."})
        post.title = title
        post.body = body
        post.save()
        return redirect( "post_detail",slug=post.slug)
    return render(request, "edit_post.html", {"post":post})

# delete a post
@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post,slug=slug)
    if request.user != post.author:
        return redirect('post_list')

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'components/post_confirm_delete.html', {'post': post})




# show all user posts
@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_on')
    return render(request, 'user_posts.html', {'posts': posts})
