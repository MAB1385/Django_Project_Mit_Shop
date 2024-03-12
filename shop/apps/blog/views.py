from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Article, Author

#! To base address root
BASE_BLOG = "blog/"
BASE_PARTIALS = "blog/partials/"


class ShowArticlesView(View):
    template_name = BASE_BLOG + "blog.html"

    def get(self, *args, **kwargs):
        articles = Article.objects.filter(is_active=True).order_by("-publish_date")
        paginator = Paginator(articles, 8)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"page_obj": page_obj, "articles": articles}
        return render(self.request, self.template_name, context)


# todo --------------------------------------------------------------------
class ArticleDetailView(View):
    template_name = BASE_BLOG + "article_detail.html"

    def get(self, *args, **kwargs):
        article = get_object_or_404(Article, slug=kwargs["slug"])
        if not article.is_active:
            return Http404()
        article.view_number += 1
        article.save()
        article_authors = article.author.through.objects.all()
        authors = Author.objects.filter(is_active=True)
        print(authors[0].name)
        tags = [tag.strip() for tag in article.key_words.split("-")]
        context = {
            "tags": tags,
            "article": article,
            "article_authors": article_authors,
            "authors": authors,
        }
        return render(self.request, self.template_name, context)


# todo --------------------------------------------------------------------
#! The lase articles
class LastArticles(View):
    template_name = BASE_PARTIALS + "last_articles.html"

    def get(self, *args, **kwargs):
        articles = Article.objects.filter(is_active=True).order_by("-publish_date")[:6]
        return render(self.request, self.template_name, {"articles": articles})


# todo --------------------------------------------------------------------
#! The most visited articles
class MostVisitedArticles(View):
    template_name = BASE_PARTIALS + "most_visited_articles.html"

    def get(self, *args, **kwargs):
        articles = Article.objects.filter(is_active=True).order_by("-view_number")[:4]
        return render(self.request, self.template_name, {"articles": articles})


# todo --------------------------------------------------------------------
#! Search in articles
class SearchArticleView(View):
    template_name = BASE_BLOG + "search_view.html"

    def get(self, *args, **kwargs):
        if (query := str(self.request.GET.get("q")).strip()) == "":
            return redirect("blog:show_articles")
        articles = Article.objects.filter(
            Q(title__icontains=query)
            | Q(text__icontains=query)
            | Q(key_words__icontains=query)
            | Q(short_text__icontains=query)
            | Q(group__title__icontains=query)
        )
        articles = articles.filter(is_active=True).order_by("-publish_date")
        paginator = Paginator(articles, 8)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"page_obj": page_obj, "query": query, "articles": articles}
        return render(self.request, self.template_name, context)
