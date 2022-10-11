from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from personal_blog.forms import CommentForm, ContactForm, NewsLetterForm, PostForm
from personal_blog.models import Category, Post, Tag

one_week_ago = timezone.now() - timedelta(days=7)
PAGINATE_BY = 1


class HomeView(ListView):
    model = Post
    template_name = "aznews/index.html"
    # template_name = "blog/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status="published").order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_posts"] = Post.objects.filter(status="published").order_by(
            "-views_count"
        )[:3]
        context["most_viewed"] = (
            Post.objects.filter(status="published").order_by("-views_count").first()
        )
        context["recent_posts"] = Post.objects.filter(status="published").order_by(
            "-published_at"
        )[:6]
        context["weekly_top_posts"] = Post.objects.filter(
            status="published", published_at__gte=one_week_ago
        ).order_by("-views_count")[:6]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/main/post/post_detail/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        obj.views_count += 1
        obj.save()

        context = super().get_context_data(**kwargs)
        context["previous_post"] = (
            Post.objects.filter(status="published", id__lt=obj.id)
            .order_by("-id")
            .first()
        )

        context["next_post"] = (
            Post.objects.filter(status="published", id__gt=obj.id)
            .order_by("id")
            .first()
        )
        return context


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "aznews/main/post/post_list/post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")
    paginate_by = PAGINATE_BY


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("drafts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect("post-list")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("post-list")


class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.status = "published"
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")


# class PostUpdateView(View):
#     def get(self, request, pk, *args, **kwargs):
#         post = get_object_or_404(Post, pk=pk)
#         form = PostForm(instance=post)
#         return render(
#             request,
#             "blog/post_create.html",
#             {"form": form},
#         )

#     def post(self, request, pk, *args, **kwargs):
#         post = get_object_or_404(Post, pk=pk)
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect("post-detail", pk=post.pk)


class PostListByCategory(ListView):
    model = Post
    template_name = "aznews/main/post/post_list/post_list.html"
    context_object_name = "posts"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="published",
            category=self.kwargs["cat_id"],
        )
        return queryset


class PostListByTag(ListView):
    model = Post
    template_name = "aznews/main/post/post_list/post_list.html"
    context_object_name = "posts"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="published",
            tag=self.kwargs["tag_id"],
        )
        return queryset


class PostSearchView(View):
    template_name = "aznews/main/post/post_list/post_list.html"

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status="published") # ORM => object relational mapping
        return render(
            request,
            self.template_name,
            {
                "posts": posts,
            },
        )

    def post(self, request, *args, **kwargs):
        query = request.POST["query"]
        posts = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query))
            & Q(status="published")
        )
        return render(
            request,
            self.template_name,
            {
                "posts": posts,
                "query": query,
            },
        )


# class AboutView(View):
#     template_name = "aznews/about.html"

#     def get(self, request, *args, **kwargs):
#         return render(
#             request,
#             self.template_name,
#         )


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class ContactView(View):
    template_name = "aznews/contact.html"
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":  # ajax or not
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True}, status=200)
        return JsonResponse({"success": False}, status=400)


class NewsLetterView(View):
    form_class = NewsLetterForm

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":  # ajax or not
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Congratulation. You have successfully subscribed to our Newsletter.",
                    },
                    status=200,
                )
        return JsonResponse(
            {
                "success": False,
                "message": "Sorry! Something went wrong. Please make sure your email address is valid.",
            },
            status=400,
        )


class CommentCreateView(View):
    form_class = CommentForm
    template_name = "aznews/main/post/post_detail/post_detail.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post_id = request.POST["post"]
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)
        else:
            post = get_object_or_404(Post, pk=post_id)
            return render(
                request,
                self.template_name,
                {"form": form, "post": post},
            )
