from django.contrib import admin

from .models import Post, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 2


class PostAdmin(admin.ModelAdmin):
    fields = ["author", "title", "creation_date", "upvotes_amount", ]
    readonly_fields = ["creation_date", "upvotes_amount", ]
    inlines = [CommentInline, ]


admin.site.register(Post, PostAdmin)
