from django.views import generic
from .models import Post, Category, Tag, Comment
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from django.db.models import Count

class PostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(status=Post.STATUS_PUBLISHED).select_related("author", "category").prefetch_related("tags").annotate(num_comments=Count("comments"))


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, slug=self.kwargs.get("slug"), status=Post.STATUS_PUBLISHED)
        # افزایش بازدید (آسان)
        Post.objects.filter(pk=obj.pk).update(views=models.F("views") + 1)
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.filter(approved=True)
        ctx["comment_form"] = CommentForm()
        # پیشنهاد پست‌های مرتبط (هم دسته یا تگ مشترک)
        related = Post.objects.filter(status=Post.STATUS_PUBLISHED).exclude(pk=self.object.pk)
        if self.object.category:
            related = related.filter(category=self.object.category)
        ctx["related_posts"] = related[:3]
        return ctx

class CategoryListView(generic.ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        cat = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        return Post.objects.filter(status=Post.STATUS_PUBLISHED, category=cat)

class TagListView(generic.ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        return Post.objects.filter(status=Post.STATUS_PUBLISHED, tags=tag)

# دیدگاه جدید — تابعی برای simplicity
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

@require_POST
def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        if request.user.is_authenticated:
            comment.author = request.user
            comment.name = request.user.get_full_name() or request.user.username
        comment.post = post
        comment.approved = False  # مدیر باید تایید کند
        comment.save()
    return redirect(post.get_absolute_url())
