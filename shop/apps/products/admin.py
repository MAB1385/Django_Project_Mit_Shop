from admin_decorators import order_field, short_description
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core import serializers
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.utils.html import format_html

# pip install django-admin-list-filter-dropdown
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
    RelatedOnlyDropdownFilter,
    SimpleDropdownFilter,
)

from .models import (
    Brand,
    Feature,
    FeatureValue,
    Product,
    ProductColor,
    ProductFeature,
    ProductGallery,
    ProductGroup,
)


# todo --------------------------------------------------------------------
def de_active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    if res == 1:
        message = "گروه کالای انتخاب شده غیر فعال شد."
    else:
        message = f"{res} گروه کالای انتخاب شده غیر فعال شدند."
    modeladmin.message_user(request, message)


def active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    if res == 1:
        message = "گروه کالای انتخاب شده فعال شد."
    else:
        message = f"{res} گروه کالای انتخاب شده فعال شدند."
    modeladmin.message_user(request, message)


def export_json(modeladmin, request, queryset):
    #! To create json
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


# todo --------------------------------------------------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("show_image", "title", "slug", "count_sub_group")
    # list_filter = (("title", DropdownFilter),)
    search_fields = (
        "title",
        "description",
    )
    ordering = ("title",)
    actions = [export_json]

    def get_queryset(
        self, *args, **kwargs
    ):  #!It is a function for customization queryset.
        qs = super(BrandAdmin, self).get_queryset(
            *args, **kwargs
        )  #!Returns the existing queryset
        # ? annotate --> To add a column         Count --> To count the values of a field
        qs = qs.annotate(sub_group=Count("brands"))
        return qs

    fieldsets = (
        (
            "اطلاعات برند",
            {
                "fields": (
                    "title",
                    ("slug", "image"),
                    "description",
                )
            },
        ),
    )

    @short_description("تصویر")
    def show_image(self, obj):
        return format_html(f"<img src='{obj.image.url}' style='height:100px;'/>")

    #! A method to assign a column to the list_display
    @order_field("sub_group")
    def count_sub_group(self, obj):
        return obj.sub_group

    count_sub_group.short_description = "تعداد محصولات موجود در فروشگاه"
    export_json.short_description = "خروجی json گرفتن از برند های انتخاب شده"


# todo --------------------------------------------------------------------
#! To display ForeignKey relation values as a table under the model under construction.
class ProductGroupInstanceInLineAdmin(admin.StackedInline):  # StackedInline
    model = ProductGroup
    extra = 1
    # min_num = None
    # max_num = None
    # template = None
    verbose_name = "زیر گروه کالا"
    verbose_name_plural = "زیر گروه های کالا"


# todo --------------------------------------------------------------------
class GroupFilter(SimpleDropdownFilter):
    title = "گروه محصولات"
    parameter_name = "group"

    def lookups(self, request, model_admin):
        sub_groups = ProductGroup.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.title) for item in groups]

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset


# todo --------------------------------------------------------------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        "show_image",
        "title",
        "slug",
        "group_parent",
        "is_active",
        "register_date",
        "published_date",
        "count_sub_group",
        "product_of_group",
    )
    list_filter = (
        GroupFilter,
        "is_active",
    )
    search_fields = (
        "title",
        "description",
    )
    ordering = (
        "group_parent",
        "title",
    )
    list_editable = ("is_active",)
    #! To display ForeignKey relation values as a table under the model under construction.
    inlines = [ProductGroupInstanceInLineAdmin]

    actions = [de_active_product_group, active_product_group, export_json]

    fieldsets = (
        (
            "اطلاعات گروه کالا",
            {
                "fields": (
                    "title",
                    ("image", "group_parent"),
                    "description",
                    ("slug", "is_active"),
                )
            },
        ),
        (
            "تاریخ و زمان",
            {"fields": ("published_date",)},
        ),
    )

    @short_description("تصویر")
    def show_image(self, obj):
        return format_html(f"<img src='{obj.image.url}' style='height:100px;'/>")

    def get_queryset(
        self, *args, **kwargs
    ):  #!It is a function for customization queryset.
        qs = super(ProductGroupAdmin, self).get_queryset(
            *args, **kwargs
        )  #!Returns the existing queryset
        # ? annotate --> To add a column         Count --> To count the values of a field
        qs = qs.annotate(sub_group=Count("groups"))
        qs = qs.annotate(product_of_group=Count("products_of_groups"))
        return qs

    #! A method to assign a column to the list_display
    @order_field("sub_group")
    def count_sub_group(self, obj):
        return obj.sub_group

    @short_description("تعداد کالاهای گروه")
    @order_field("product_of_group")  #! To add sorting by this field
    def product_of_group(self, obj):
        return obj.product_of_group

    #! To rename a column
    count_sub_group.short_description = "تعداد زیر گروه ها"
    de_active_product_group.short_description = (
        "غیر فعال کردن گروه های کالا های انتخاب شده"
    )
    active_product_group.short_description = "فعال کردن گروه های کالا های انتخاب شده"
    export_json.short_description = "خروجی json گرفتن از گروه های کالا های انتخاب شده"


# todo --------------------------------------------------------------------
def de_active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    if res == 1:
        message = "کالای انتخاب شده غیر فعال شد."
    else:
        message = f"{res} کالای انتخاب شده غیر فعال شدند."
    modeladmin.message_user(request, message)


def active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    if res == 1:
        message = "کالای انتخاب شده فعال شد."
    else:
        message = f"{res} کالای انتخاب شده فعال شدند."
    modeladmin.message_user(request, message)


# todo --------------------------------------------------------------------
class ProductFeatureInstanceInLineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 1

    class Media:
        css = {"all": ("css/style_admin.css",)}

        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js",
            "js/js_admin_feature_value.js",
        )


# todo --------------------------------------------------------------------
class ProductGalleryInstanceInLineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 3


# todo --------------------------------------------------------------------
class ProductColorInstanceInLineAdmin(admin.TabularInline):
    model = ProductColor
    extra = 1


# todo --------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "show_image",
        "name",
        "display_product_group",
        "slug",
        "brand",
        "price",
        "is_active",
        "update_date",
    )
    list_filter = (
        ("brand", RelatedDropdownFilter),
        ("product_group", RelatedDropdownFilter),
        "is_active",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = (
        "update_date",
        "name",
    )
    list_editable = ("is_active",)

    inlines = [
        ProductColorInstanceInLineAdmin,
        ProductFeatureInstanceInLineAdmin,
        ProductGalleryInstanceInLineAdmin,
    ]

    actions = [de_active_product, active_product, export_json]

    @short_description("تصویر")
    def show_image(self, obj):
        return format_html(f"<img src='{obj.image.url}' style='height:100px;'/>")

    def display_product_group(self, obj):  #! To display many to many field
        return ", ".join([group.title for group in obj.product_group.all()])

    def formfield_for_manytomany(
        self, db_field, request, **kwargs
    ):  #! To manegmant many to many fields in create and edite the model
        if db_field.name == "product_group":
            kwargs["queryset"] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    fieldsets = (
        (
            "اطلاعات کالا",
            {
                "fields": (
                    "name",
                    ("image", "price"),
                    ("product_group", "brand"),
                    "summery_description",
                    "description",
                    ("slug", "is_active"),
                )
            },
        ),
        (
            "تاریخ و زمان",
            {"fields": ("published_date",)},
        ),
    )

    de_active_product.short_description = "غیر فعال کردن کالا های انتخاب شده"
    active_product.short_description = "فعال کردن کالا های انتخاب شده"
    export_json.short_description = "خروجی json گرفتن از داده های انتخاب شده"
    display_product_group.short_description = "گروه های کالا"


# todo --------------------------------------------------------------------
class FeatureValueInstanceInLineAdmin(admin.TabularInline):
    model = FeatureValue
    extra = 1


# todo --------------------------------------------------------------------
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "display_groups", "display_feature_values")
    list_filter = (("product_group", RelatedDropdownFilter),)
    search_fields = ("name",)
    ordering = ("name",)

    inlines = [FeatureValueInstanceInLineAdmin]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "product_group":
            kwargs["queryset"] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    @short_description("گروه های دارای ویژگی")
    def display_groups(self, obj):
        return ", ".join([group.title for group in obj.product_group.all()])

    @short_description("مقادیر ممکن برای ویژگی")
    def display_feature_values(self, obj):
        return ", ".join([value.value_title for value in obj.feature_values.all()])
