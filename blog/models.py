from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField  # اگر ندارید، از models.TextField استفاده کنید
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:category_detail", args=[self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "پیش‌نویس"),
        (STATUS_PUBLISHED, "منتشرشده"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, allow_unicode=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    excerpt = models.TextField(blank=True)
    content = RichTextField()  # یا models.TextField()
    main_image = models.ImageField(upload_to="blog/main_images/", blank=True, null=True)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        # اگر slug خالیه از title بساز
        if not self.slug:
            base = slugify(self.title, allow_unicode=True)[:240]
            slug = base
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog/images/")
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.post.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120, blank=True)   # اگر کاربر لاگین نیست
    email = models.EmailField(blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "دیدگاه"
        verbose_name_plural = "دیدگاه‌ها"

    def __str__(self):
        return f"Comment by {self.name or self.author} on {self.post}"
