from personal_blog.models import Category, Post, Tag


def navigation(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    top_posts = Post.objects.filter(status="published").order_by("-views_count")[:6]
    return {
        "categories": categories,
        "tags": tags,
        "top_posts": top_posts,
    }
