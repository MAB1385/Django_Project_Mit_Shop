from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.accounts.models import Customer
from apps.products.models import Product

from .forms import CommentForm
from .models import Comment, Favorite, Scoring


class CommentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        productId = self.request.GET.get("productId")
        commentId = self.request.GET.get("commentId")
        slug = kwargs["slug"]
        if not productId:
            productId = get_object_or_404(Product, slug=slug).id
        if not commentId:
            commentId = None
        initial_dict = {"product_id": productId, "comment_id": commentId}
        form = CommentForm(initial=initial_dict)
        if commentId == None:
            commentId = 0
        return render(
            self.request,
            "csf/partials/create_comment.html",
            {"form": form, "slug": slug, "commentId": commentId},
        )

    def post(self, *args, **kwargs):
        slug = kwargs.get("slug")
        product = get_object_or_404(Product, slug=slug)
        print(self.request.POST)
        form = CommentForm(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parent = None
            if cd["comment_id"]:
                parentId = cd["comment_id"]
                parent = Comment.objects.get(id=parentId)
            try:
                customer = Customer.objects.get(user=self.request.user)
            except ObjectDoesNotExist:
                customer = Customer.objects.create(
                    user=self.request.user,
                )
            Comment.objects.create(
                product=product,
                commenting_user=self.request.user,
                comment_text=cd["comment_text"],
                comment_parent=parent,
            )
            # messages.success(self.request, "نظر شما با موفقیت ثبت شد", "success")
            # return redirect("products:product_detail", product.slug)
            return JsonResponse({"text": "success"}, status=200)
        else:
            # messages.error(self.request, "خطا در ثبت نظر", "danger")
            # return redirect("products:product_detail", product.slug)
            return JsonResponse({"text": "error"}, status=400)


# todo --------------------------------------------------------------------
class AddScore(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        productId = self.request.GET.get("productId")
        score = self.request.GET.get("score")
        product = get_object_or_404(Product, id=productId)
        Scoring.objects.create(
            product=product, scoring_user=self.request.user, score=score
        )

        return HttpResponse("امتیاز شما با موقیت ثبت شد.")


# todo --------------------------------------------------------------------
class AddToFavorite(View):
    def get(self, *args, **kwargs):
        productId = self.request.GET.get("productId")
        product = get_object_or_404(Product, id=productId)
        flag = Favorite.objects.filter(
            Q(favorite_user_id=self.request.user.id) & Q(product_id=productId)
        ).exists()
        if not flag:
            Favorite.objects.create(favorite_user=self.request.user, product=product)
        return HttpResponse(
            Favorite.objects.filter(Q(favorite_user_id=self.request.user.id)).count()
        )


# todo --------------------------------------------------------------------
class DeleteFromFavorite(View):
    def get(self, *args, **kwargs):
        productId = self.request.GET.get("productId")
        flag = Favorite.objects.filter(
            Q(favorite_user_id=self.request.user.id) & Q(product_id=productId)
        ).exists()
        if flag:
            Favorite.objects.filter(
                Q(favorite_user_id=self.request.user.id) & Q(product_id=productId)
            ).delete()
            return HttpResponse(
                Favorite.objects.filter(
                    Q(favorite_user_id=self.request.user.id)
                ).count()
            )


# todo --------------------------------------------------------------------
class ShowFavorite(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        favorites = Favorite.objects.filter(Q(favorite_user_id=self.request.user.id))
        return render(self.request, "csf/show_favorite.html", {"favorites": favorites})


# todo --------------------------------------------------------------------
def status_of_favorite(request):
    number_of_favorite = 0
    if request.user.is_authenticated:
        number_of_favorite = Favorite.objects.filter(
            Q(favorite_user_id=request.user.id)
        ).count()
    return HttpResponse(number_of_favorite)
