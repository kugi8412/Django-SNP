from django.urls import path
from comments.views import add_comment, comment_success, list_comments,\
                           edit_comment, delete_comment

urlpatterns = [
    path("", add_comment, name="add_comment"),
    path("success/", comment_success, name="comment_success"),
    path("edit/<int:comment_id>/", edit_comment, name="edit_comment"),
    path("delete/<int:comment_id>/", delete_comment, name="delete_comment"),
    path("list/", list_comments, name="list_comments"),
]