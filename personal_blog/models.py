from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # does not create table for TimeStampModel


class Category(TimeStampModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Tag(TimeStampModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("published", "published"),
        ("unpublished", "unpublished"),
    ]
    title = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False, null=False
    )
    tag = models.ManyToManyField(Tag)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to="featured_images/%Y/%m/%d")
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="unpublished"
    )
    content = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def latest_comments(self):
        comments = Comment.objects.filter(post=self).order_by("-created_at")[:10]
        return comments

    @property
    def comments_count(self):
        count = Comment.objects.filter(post=self).order_by("-created_at").count()
        return count


class NewsLetter(TimeStampModel):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Contact(TimeStampModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()

    def __str__(self):
        return self.subject


class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()

    def __str__(self):
        return self.description[:100]

    class Meta:
        ordering = ["-created_at"]


################ Types of relationship ################
# 1 - 1
# 1 - M
# M - M


################ 1 - 1 relationship ################
# 1 user can have 1 profile only
# 1 profile is associated to only 1 user
# OneToOneField => anywhere

################# 1 - M relationship ################
# 1 post is associated to 1 category
# 1 category can have M posts
# ForeignKey  => M

################ M - M relationship ################
# 1 post can have M tag
# 1 tag can have M post
# ManyToManyField  => anywhere
