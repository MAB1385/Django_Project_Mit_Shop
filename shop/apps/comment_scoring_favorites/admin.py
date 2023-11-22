from django.contrib import admin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
    RelatedOnlyDropdownFilter,
    SimpleDropdownFilter,
)

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "commenting_user",
        "comment_text",
        "comment_parent",
        "is_active",
    )
    list_filter = (
        "is_active",
        ("product", RelatedOnlyDropdownFilter),
        ("commenting_user", RelatedOnlyDropdownFilter),
        ("comment_parent", RelatedOnlyDropdownFilter),
    )
    search_fields = ("comment_text",)
    ordering = ("-register_date",)
    list_editable = ("is_active",)
