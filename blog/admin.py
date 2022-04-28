from django.contrib import admin

from .models import Post, Comment, PostReport, Like


class ReportersInline(admin.TabularInline):
    model = PostReport
    readonly_fields = ("user", 'created_at')
    extra = 0
    max_num = 0
    verbose_name = "Signalement"


class CommentsInline(admin.TabularInline):
    model = Comment
    readonly_fields = ("text", "author", 'created_at')
    fields = ("text", "author", 'created_at')
    extra = 0
    max_num = 0
    verbose_name = "Commentaire"


class LikesInline(admin.TabularInline):
    model = Like
    readonly_fields = ("user", 'created_at')
    extra = 0
    max_num = 0
    verbose_name = "Like"


class PostAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'status', 'nb_of_reports', 'is_anonymous', 'author', "created_at")
    list_filter = ('status', 'created_at', 'is_anonymous')
    search_fields = ('text', 'author__username', 'author__first_name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ["make_published", "make_hidden"]

    readonly_fields = (
        'created_at', 'updated_at', 'author', 'is_anonymous',
        'nb_of_reports', 'nb_of_likes', 'nb_of_comments',
    )

    inlines = [CommentsInline, LikesInline, ReportersInline]

    fieldsets = (
        (None, {
            'fields': ('text', 'status', 'is_anonymous', 'author')
        }),
        ('Dates', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('text', 'status', 'is_anonymous', 'author')
        }
         ),
    )

    def save_model(self, request, obj, form, change):
        """ Override the save_model method to set the author of the post as the current user for new posts """
        if not obj.id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description='Rendre les posts selections visibles')
    def make_published(request, queryset):
        queryset.update(status=Post.NORMAl)

    @admin.action(description='Masquer les posts selections')
    def make_hidden(request, queryset):
        queryset.update(status=Post.HIDDEN)

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('blog.view_post')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('blog.edit_post')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('blog.edit_post')

    def has_add_permission(self, request):
        return request.user.has_perm('blog.view_post')


admin.site.register(Post, PostAdmin)

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostReport)
