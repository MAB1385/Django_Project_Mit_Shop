from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Q
from django.shortcuts import redirect, render
from django.views import View

from apps.products.models import Brand, Product, ProductGroup

from .filters import ProductsFilter


class SearchResultsView(View):
    def get(self, *args, **kwargs):
        query = str(self.request.GET.get("q")).strip()
        if query == "":
            return redirect("main:home")
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(summery_description__icontains=query)
            | Q(description__icontains=query)
        )
        res_aggre = products.aggregate(min=Min("price"), max=Max("price"))

        price = res_aggre["max"]

        qs = "?q=" + query + "&"

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
        paginator = Paginator(products, product_per_page)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "product_group": query,
            "products": products,
            "display": display,
            "res_aggre": res_aggre,
            "price": price,
            "page_obj": page_obj,
            "filter": filter,
            "qs": qs,
            "sort_type": sort_type,
            "flag": flag,
            "brand_flag": len(brand_list) > 0,
        }
        return render(self.request, "search/search_view.html", context)


# todo --------------------------------------------------------------------
#! The filter features
class FeaturesFilter(View):
    template_name = "products/partials/" + "features_filter.html"

    def get(self, *args, **kwargs):
        query = kwargs.get("q")
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(summery_description__icontains=query)
            | Q(description__icontains=query)
        )
        feature_dict = dict()
        # product_groups = [i.product_group.all() for i in products]
        product_groups = ProductGroup.objects.filter(Q(products_of_groups__in=products))
        for product_group in product_groups:
            features = product_group.features_of_groups.all()

            for feature in features:
                feature_dict[feature] = feature.feature_values.all()

        context = {
            "feature_dict": feature_dict,
            "feature_list": feature_list,
        }
        return render(self.request, self.template_name, context)


# todo --------------------------------------------------------------------
#! The filter brand
class BrandsFilter(View):
    template_name = "products/partials/" + "brands.html"

    def get(self, *args, **kwargs):
        query = kwargs.get("q")
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(summery_description__icontains=query)
            | Q(description__icontains=query)
        )
        brand_id = []
        product_groups = ProductGroup.objects.filter(Q(products_of_groups__in=products))
        for product_group in product_groups:
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
