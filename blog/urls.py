from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('<int:post_id>', views.detail, name="detail"),
    path('new' , views.create_post , name="create_post"),
    path('delete/<int:post_id>' , views.delete_post , name="delete_post"),
    path('update/<int:post_id>' , views.update_post , name="update_post"),
    path('search' , views.search , name="search"),
    path('comment/delete/<int:comment_id>' , views.comment_delete_not_api , name="comment_delete_not_api"),
    path('api/comment/new/<int:post_id>' , views.comment_create , name="comment_create"),
    path('api/comment/update/<int:comment_id>' , views.comment_update , name="comment_update"),
    path('api/comment/delete/<int:comment_id>' , views.comment_delete , name="comment_delete"),
    path('api/comment/get/<int:post_id>' , views.get_comment , name="comment_get"),
]
