from urllib.parse import urlencode

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .compare import CompareProduct
from .filters import ProductsFilter
from .models import Brand, FeatureValue, Product, ProductColor, ProductGroup

#! To base address root
BASE_PRODUCTS = "products/"
BASE_PARTIALS = "products/partials/"


def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))


# todo --------------------------------------------------------------------
#! The cheapest products
class CheapestProducts(View):
    def get(self, *args, **kwargs):
        products = Product.objects.filter(is_active=True).order_by("price")[:5]
        product_groups = get_root_group()
        context = {"products": products, "product_groups": product_groups}
        return render(self.request, "products/partials/cheapest_products.html", context)


# todo --------------------------------------------------------------------
#! The lase products
class LastProducts(View):
    def get(self, *args, **kwargs):
        products = Product.objects.filter(is_active=True).order_by("-published_date")[
            :5
        ]
        product_groups = get_root_group()
        context = {"products": products, "product_groups": product_groups}
        return render(self.request, "products/partials/last_products.html", context)

    # def post(self):
    #     if self.request.is_ajax():
    #         id = self.request.POST.get("id")
    #         if id == "all" or id == False:
    #             products = Product.objects.filter(is_active=True).order_by(
    #                 "-published_date"
    #             )[:5]
    #         else:
    #             current_group = ProductGroup.objects.get(id=id)
    #             products = Product.objects.filter(
    #                 Q(is_active=True) & Q(product_group=current_group)
    #             ).order_by("-published_date")[:5]
    #         context = {
    #             "products": products,
    #         }
    #         return JsonResponse(context)


# todo --------------------------------------------------------------------
#! The popular product group
class PopularProductGroups(View):
    def get(self, *args, **kwargs):
        product_groups = (
            ProductGroup.objects.filter(Q(is_active=True) & ~Q(group_parent=None))
            .annotate(count=Count("products_of_groups"))
            .order_by("-count")[:6]
        )
        context = {"product_groups": product_groups}
        return render(
            self.request, "products/partials/popular_product_group.html", context
        )


# todo --------------------------------------------------------------------
#! The detail product
class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            price = int(product.price)
            comments = product.comments_product.filter(is_active=True).order_by(
                "-register_date"
            )
            # if request.POst('color_id'):
            #     color=ProductColor.objects.get(id=request.GET.get('color_id'))
            #     price+=int(color.value_added)
            context = {"product": product, "price": price, "comments": comments}
            return render(request, "products/product_detail.html", context)

    def post(self, *args, **kwargs):

        slug = self.request.POST["slug"]
        color_id = self.request.POST["color_id"]
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            price = int(product.price)
            color = ProductColor.objects.get(id=color_id)
            price += int(color.value_added)
            context = {"price": price}
            return JsonResponse(context, status=200)


# todo --------------------------------------------------------------------
#! The related product
class RelatedProduct(View):
    def get(self, *args, **kwargs):
        current_product = get_object_or_404(Product, slug=kwargs["slug"])
        related_products = []
        for group in current_product.product_group.all():
            related_products.extend(
                Product.objects.filter(
                    Q(product_group=group)
                    & Q(is_active=True)
                    & ~Q(id=current_product.id)
                )
            )
        return render(
            self.request,
            "products/partials/related_products.html",
            {"related_products": list(set(related_products))[:10]},
        )


# todo --------------------------------------------------------------------
#! The list of product groups
class ProductGroupsView(View):
    def get(self, *args, **kwargs):
        product_groups = (
            ProductGroup.objects.filter(Q(is_active=True) & ~Q(group_parent=None))
            .annotate(count=Count("products_of_groups"))
            .order_by("-count")
        )
        context = {"product_groups": product_groups}
        return render(self.request, "products/product_groups.html", context)


# todo --------------------------------------------------------------------
#! The list of product of group
class ProductsByGroupView(View):
    def get(self, *args, **kwargs):
        current_group = get_object_or_404(ProductGroup, slug=kwargs["slug"])

        id_list = [current_group.id]

        for p in ProductGroup.objects.filter(group_parent=current_group):
            id_list.append(p.id)

        products = Product.objects.filter(
            Q(is_active=True) & Q(product_group__id__in=id_list)
        )

        res_aggre = products.aggregate(min=Min("price"), max=Max("price"))

        price = res_aggre["max"]

        qs = "?"

        flag = False

        #! To price filter
        filter = ProductsFilter(self.request.GET, queryset=products)
        products = filter.qs
        if (
            self.request.GET.get("price")
            and int(self.request.GET.get("price")) != price
        ):
            price = self.request.GET.get("price")
            qs += f"price={price}&"
            flag = True

        #! To brand filter
        global brand_list
        brand_list = self.request.GET.getlist("brand")
        if brand_list:
            products = products.filter(brand__id__in=brand_list)
            flag = True
            for i in brand_list:
                qs += f"brand={i}&"

        #! To feature filter
        global feature_list
        feature_list = self.request.GET.getlist("feature")
        if feature_list:
            products = products.filter(
                product_features__filter_value__id__in=feature_list
            ).distinct()
            flag = True
            for i in feature_list:
                qs += f"feature={i}&"

        #! sort type
        sort_type = self.request.GET.get("sort_type")
        if not sort_type:
            sort_type = "0"
        elif sort_type == "1":
            products = products.order_by("price")
        elif sort_type == "2":
            products = products.order_by("-price")
        qs += f"sort_type={sort_type}&"

        #! display type
        product_per_page = 9
        display = self.request.GET.get("display")
        if not display or display == "9":
            display = "9"
            product_per_page = 9
        elif display == "2":
            product_per_page = 2
        elif display == "6":
            product_per_page = 6
        qs += f"display={display}&"

        #! To pager
        group_slug = kwargs["slug"]
        paginator = Paginator(products, product_per_page)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "product_group": current_group,
            "products": products,
            "display": display,
            "res_aggre": res_aggre,
            "price": price,
            "page_obj": page_obj,
            "group_slug": group_slug,
            "filter": filter,
            "qs": qs,
            "sort_type": sort_type,
            "flag": flag,
            "brand_flag": len(brand_list) > 0,
        }
        return render(self.request, "products/product_by_group.html", context)


# todo --------------------------------------------------------------------
#! Two dropdown in admin panel
class FilterValueForFeature(View):
    def get(self, *args, **kwargs):
        feature_id = self.request.GET["feature_id"]
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)


# todo --------------------------------------------------------------------
#! The list of product groups for filter
class ProductGroupsFilter(View):
    template_name = BASE_PARTIALS + "product_groups.html"

    def get(self, *args, **kwargs):
        product_groups = (
            ProductGroup.objects.annotate(count=Count("products_of_groups"))
            .filter(Q(is_active=True) & ~Q(count=0))
            .order_by("-count")
        )
        context = {"product_groups": product_groups}
        return render(self.request, self.template_name, context)


# todo --------------------------------------------------------------------
#! The detail brand
class BrandDetailView(View):
    template_name = BASE_PRODUCTS + "brand_detail.html"

    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug)
        context = {"brand": brand}
        return render(request, self.template_name, context)


# todo --------------------------------------------------------------------
#! The filter brand
class BrandsFilter(View):
    template_name = BASE_PARTIALS + "brands.html"

    def get(self, *args, **kwargs):
        product_group = get_object_or_404(ProductGroup, slug=kwargs["slug"])
        brand_id = []
        for i in product_group.products_of_groups.filter(is_active=True):
            brand_id.append(i.brand.id)
        for p in ProductGroup.objects.filter(group_parent=product_group):
            for j in p.products_of_groups.filter(is_active=True):
                brand_id.append(j.brand.id)
        brands = (
            Brand.objects.filter(pk__in=brand_id)
            .annotate(count=Count("brands"))
            .filter(~Q(count=0))
            .order_by("-count")
        )
        context = {
            "brands": brands,
            "brand_list": brand_list,
        }
        return render(self.request, self.template_name, context)


# todo --------------------------------------------------------------------
#! The filter colors
class ColorsFilter(View):
    template_name = BASE_PARTIALS + "colors.html"

    def get(self, *args, **kwargs):
        product_group = get_object_or_404(ProductGroup, slug=kwargs["slug"])
        products = product_group.products_of_groups.filter(is_active=True).values("id")
        colors = ProductColor.objects.filter(product_id__in=products)
        col = []
        for color in colors:
            col.append(color.color)

        context = {"colors": set(col)}
        return render(self.request, self.template_name, context)


# todo --------------------------------------------------------------------
#! The filter features
class FeaturesFilter(View):
    template_name = BASE_PARTIALS + "features_filter.html"

    def get(self, *args, **kwargs):
        product_group = get_object_or_404(ProductGroup, slug=kwargs["slug"])
        features = product_group.features_of_groups.all()
        feature_dict = dict()

        for feature in features:
            feature_dict[feature] = feature.feature_values.all()

        context = {
            "feature_dict": feature_dict,
            "feature_list": feature_list,
        }
        return render(self.request, self.template_name, context)


# todo --------------------------------------------------------------------
#! Show compare table ---> ajax
def compare_table(request):
    compare_list = CompareProduct(request)

    products = []
    for product_id in compare_list.compare_product:
        product = Product.objects.get(id=product_id)
        products.append(product)

    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)

    context = {
        "products": products,
        "features": features,
    }
    return render(request, BASE_PARTIALS + "compare_table.html", context)


# todo --------------------------------------------------------------------
#! Show compare list
class ShowCompareListView(View):
    def get(self, *args, **kwargs):
        compare_list = CompareProduct(self.request)
        context = {
            "compare_list": compare_list,
        }
        return render(self.request, BASE_PRODUCTS + "compare_list.html", context)


# todo --------------------------------------------------------------------
#! Add to compare list
class AddToCampareList(View):
    def get(self, *args, **kwargs):
        productId = self.request.GET.get("productId")
        try:
            product = Product.objects.get(id=productId)
            fainaly_set = product.get_product_groups()
            compare_list = CompareProduct(self.request)
            for product_id in compare_list.compare_product:
                fainaly_set = (
                    fainaly_set
                    & Product.objects.get(id=product_id).get_product_groups()
                )
            if len(fainaly_set) != 0:
                rec = compare_list.add_to_compare_product(int(productId))
            else:
                rec = "کالا انتخاب شده با کالاهای موجود در لیست هم گروه نمی باشد"
        except ObjectDoesNotExist:
            rec = "این کالا وجود ندارد"
        return HttpResponse(rec)


# todo --------------------------------------------------------------------
#! Delete from compare list
class DeleteFromCampareList(View):
    def get(self, *args, **kwargs):
        productId = self.request.GET.get("productId")
        compare_list = CompareProduct(self.request)
        compare_list.delete_from_compare_product(int(productId))
        return redirect("products:compare_table")


# todo --------------------------------------------------------------------
#! Status of compare list
def status_of_compare_list(request):
    compare_list = CompareProduct(request)
    return HttpResponse(compare_list.count)


# todo --------------------------------------------------------------------
class ShowProductGroupsNavbar(View):
    def get(self, *args, **kwargs):
        main_groups = get_root_group()
        return render(
            self.request,
            BASE_PARTIALS + "product_groups_navbar.html",
            {"main_groups": main_groups},
        )
