from admin_decorators import order_field, short_description
from django.contrib import admin
from django.core import serializers
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Article, Article_Group, Author


def de_active_article(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    if res == 1:
        message = "مقاله انتخاب شده غیر فعال شد."
    else:
        message = f"{res} مقاله انتخاب شده غیر فعال شدند."
    modeladmin.message_user(request, message)


def active_article(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    if res == 1:
        message = "مقاله انتخاب شده فعال شد."
    else:
        message = f"{res} مقاله انتخاب شده فعال شدند."
    modeladmin.message_user(request, message)


def de_active_author(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    if res == 1:
        message = "نویسنده انتخاب شده غیر فعال شد."
    else:
        message = f"{res} نویسنده انتخاب شده غیر فعال شدند."
    modeladmin.message_user(request, message)


def active_author(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    if res == 1:
        message = "نویسنده انتخاب شده فعال شد."
    else:
        message = f"{res} نویسنده انتخاب شده فعال شدند."
    modeladmin.message_user(request, message)


def export_json(modeladmin, request, queryset):
    #! To create json
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


# todo --------------------------------------------------------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "show_image",
        "title",
        "slug",
        "group",
        "display_article_authors",
        "is_active",
        "register_date",
        "publish_date",
        "update_date",
        "view_number",
    )
    list_filter = (
        "is_active",
        "author",
        "group",
        "register_date",
        "update_date",
    )
    search_fields = ("title", "short_text", "text", "key_words", "slug")
    ordering = (
        "-update_date",
        "-register_date",
        "title",
    )
    list_editable = ("is_active",)

    actions = [de_active_article, active_article, export_json]

    fieldsets = (
        (
            "اطلاعات متنی مقاله",
            {
                "fields": (
                    ("title", "slug"),
                    ("author", "group"),
                    ("main_image", "is_active"),
                    "short_text",
                    "text",
                    "key_words",
                    "view_number",
                )
            },
        ),
        (
            "تاریخ و زمان",
            {"fields": ("publish_date",)},
        ),
    )

    @short_description("نویسندگان")
    def display_article_authors(self, obj):  #! To display many to many field
        return ", ".join(
            [f"{author.name} {author.family}" for author in obj.author.all()]
        )

    @short_description("تصویر")
    def show_image(self, obj):
        return format_html(f"<img src='{obj.main_image.url}' style='height:100px;'/>")

    #! To rename a column
    de_active_article.short_description = "غیر فعال کردن مقالات انتخاب شده"
    active_article.short_description = "فعال کردن مقالات انتخاب شده"
    export_json.short_description = "خروجی json گرفتن از داده های انتخاب شده"


# todo --------------------------------------------------------------------
@admin.register(Article_Group)
class ArticleGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "articles_of_group")
    search_fields = ("title",)
    ordering = ("title",)

    def get_queryset(
        self, *args, **kwargs
    ):  #!It is a function for customization queryset.
        qs = super(ArticleGroupAdmin, self).get_queryset(
            *args, **kwargs
        )  #!Returns the existing queryset
        # ? annotate --> To add a column         Count --> To count the values of a field
        qs = qs.annotate(articles_of_group=Count("articles"))
        return qs

    @short_description("تعداد مقالات")
    @order_field("articles")  #! To add sorting by this field
    def articles_of_group(self, obj):
        return obj.articles_of_group


# todo --------------------------------------------------------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "show_image",
        "name",
        "family",
        "email",
        "mobile",
        "organizational_affiliation",
        "education",
        "is_active",
        "articles_of_author",
    )
    list_filter = (
        "is_active",
        "organizational_affiliation",
        "education",
    )
    search_fields = ("name", "family", "mobile", "email", "description")
    ordering = ("name", "family")
    list_editable = ("is_active",)

    actions = [de_active_author, active_author, export_json]

    @short_description("تصویر")
    def show_image(self, obj):
        return format_html(f"<img src='{obj.image.url}' style='height:100px;'/>")

    def get_queryset(
        self, *args, **kwargs
    ):  #!It is a function for customization queryset.
        qs = super(AuthorAdmin, self).get_queryset(
            *args, **kwargs
        )  #!Returns the existing queryset
        # ? annotate --> To add a column         Count --> To count the values of a field
        qs = qs.annotate(articles_of_author=Count("articles_of_authors"))
        return qs

    @short_description("تعداد مقالات")
    @order_field("articles_of_author")  #! To add sorting by this field
    def articles_of_author(self, obj):
        return obj.articles_of_author

    #! To rename a column
    de_active_author.short_description = "غیر فعال کردن نویسندگان انتخاب شده"
    active_author.short_description = "فعال کردن نویسندگان انتخاب شده"
    export_json.short_description = "خروجی json گرفتن از داده های انتخاب شده"
