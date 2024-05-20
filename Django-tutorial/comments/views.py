from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm
from .models import Comment

def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("comment_success")
    else:
        form = CommentForm()
    return render(request, "comments/add_comment.html", {"form": form})

def comment_success(request):
    return render(request, "comments/comment_success.html")

def list_comments(request):
    comments = Comment.objects.all()
    return render(request, "comments/list_comments.html", {"comments": comments})

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("list_comments")
    else:
        form = CommentForm(instance=comment)
    return render(request, "comments/edit_comment.html", {"form": form})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        comment.delete()
        return redirect("list_comments")
    return render(request, "comments/delete_comment.html", {"comment": comment})
