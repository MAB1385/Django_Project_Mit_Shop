function showVal(x) {

    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

    document.getElementById('sel_price').innerText = x;
}
function removeURLParameter(url, parameter) {

    var urlparts = url.split('?');

    if (urlparts.length >= 2) {

        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}
//! ---------------------------------------- Filter ----------------------------------------
function select_sort() {
    var select_sort_value = $("#select_sort").val();
    var url = removeURLParameter(window.location.href, "sort_type");
    if ((i = url.indexOf('?')) >= 0) {
        window.location = url + "&sort_type=" + select_sort_value;
    }
    else {
        window.location = url + "?sort_type=" + select_sort_value;
    }
}
function display() {
    var select_sort_value = $("#display").val();
    var url = removeURLParameter(window.location.href, "display");
    var url = removeURLParameter(url, "page");
    if ((i = url.indexOf('?')) >= 0) {
        window.location = url + "&display=" + select_sort_value;
    }
    else {
        window.location = url + "?display=" + select_sort_value;
    }
}
function remove_brand() {
    var url = removeURLParameter(window.location.href, "brand");
    var url = removeURLParameter(url, "page");
    window.location = url;
}
function remove_feature(features) {
    var url = removeURLParameter(window.location.href, "feature");
    var url = removeURLParameter(url, "page");
    for (let i in features) {
        url += '&feature=X'.replace('X', features[i]);
    }
    window.location = url;
}
//! ---------------------------------------- Shop_cart ----------------------------------------
function status_of_shop_cart() {
    $.ajax({
        type: "GET",
        url: "/orders/status_of_shop_cart/",
        success: function (res) {
            if (Number(res) === 0) {
                $('#indicator__value').hide();
            } else {
                $('#indicator__value').show();
                $('#indicator__value').text(res);
            }

        }
    });
}

status_of_shop_cart();

function add_to_shop_cart(product_id, qty, color_id = 0) {
    if (qty === 0) {
        qty = $('#product-quantity').val();
    }
    if (color_id === 0) {
        if ($('#product-color').length) {
            if ($("#product-form input[name='color']:checked").length > 0) {
                color_id = $("#product-form input[name='color']:checked").val();
            }
            else {
                color_id = 'None';
            }

        }
    }
    $.ajax({
        type: "GET",
        url: "/orders/add_to_shop_cart/",
        data: {
            product_id: product_id,
            qty: qty,
            color_id: color_id,
        },
        success: function (res) {
            status_of_shop_cart();
            $('#' + product_id.toString()).text(qty.toString() + ' عدد افزوده شد');
            $('#' + product_id.toString()).attr('style', 'width:110%;');
        },
        error: function (res) {
            if (res["responseJSON"]["error"] === 'color') {
                alert("لطفا رنگ مورد نظر خود را انتخاب کنید.");
            }
            else if (res["responseJSON"]["error"] === 'user') {
                alert("لطفا وارد حساب کاربری خود شوید.");
            }
            status_of_shop_cart();
        }
    });
}
function delete_from_shop_cart(shopcart_id) {
    $.ajax({
        type: "GET",
        url: "/orders/delete_from_shop_cart/",
        data: {
            shopcart_id: shopcart_id,
        },
        success: function (res) {
            $('#shop_cart_list').html(res);
            status_of_shop_cart()
        }
    });
}
function update_shop_cart(shopcart_id, qty) {
    $.ajax({
        type: "GET",
        url: "/orders/update_shop_cart/",
        data: {
            shopcart_id: shopcart_id,
            qty: qty,
        },
        success: function (res) {
            $('#shop_cart_list').html(res);
            status_of_shop_cart()
        }
    });
}

function CreateComment(slug, comment_id) {
    $.ajax({
        type: "POST",
        url: "/csf/create_comment/" + slug + '/',
        data: $('#create-comment-form-' + comment_id).serialize(),
        success: function (res) {
            $('#create-comment-form-' + comment_id)[0].reset()
            alert("نظر شما با موفقیت ثبت شد");
            // $('#create-comment-form' + comment_id).closest('form').find("textarea").val("");
        },
        error: function (res) {
            alert("خطا در ثبت نظر");
        },
    });
}

function showCreateCommentForm(product_id, comment_id, slug) {
    $.ajax({
        type: "GET",
        url: "/csf/create_comment/" + slug,
        data: { productId: product_id, commentId: comment_id },
        success: function (res) {
            $('#btn-' + comment_id).hide();
            $('#btn-close-' + comment_id).attr('style', '');
            $('#comment-form-' + comment_id).html(res);

        },
    });
}

function hideCommentForm(comment_id) {

    $('#btn-close-' + comment_id).hide();
    $('#btn-' + comment_id).attr('style', '');
    $('#comment-form-' + comment_id).html('');

}

function test(slug) {
    alert(slug);
}

function addScore(score, productId) {
    var starRatings = document.querySelectorAll('.fa-star');
    starRatings.forEach(element => {
        element.classList.remove('checker');
    });
    for (let i = 1; i <= score; i++) {
        const element = document.getElementById('star_' + i);
        element.classList.add('checked');
    }
    $.ajax({
        type: "GET",
        url: "/csf/add_score/",
        data: { productId: productId, score: score },
        success: function (res) {
            var s = $('#score').text();
            if (s == 0) {
                $('#score').text(score);
            } else {
                $('#score').text((Number(s) + score) / 2.0);
            }
            alert(res);
        },
    });
    starRatings.forEach(element => {
        element.classList.remove('disable');
    });
    starRatings.forEach(element => {
        element.attributes.removeNamedItem('onclick');
    });
}
function addToFavorites(productId) {
    $.ajax({
        type: "GET",
        url: "/csf/add_to_favorite/",
        data: { productId: productId },
        success: function (res) {
            $('#wishlist').text(res);
            $('.favorite' + productId).attr('style', 'padding: 0px;color:red;');
            $('.favorite' + productId).attr('onclick', 'deleteFromFavorites(' + productId + ')');
            $('.favorite-i' + productId).attr('class', 'fa fa-heart favorite-i' + productId);
            alert("به لیست علاقه مندی شما اضافه شد");
            status_of_favorite();
        },
    });
}
function deleteFromFavorites(productId) {
    $.ajax({
        type: "GET",
        url: "/csf/delete_from_favorite/",
        data: { productId: productId },
        success: function (res) {
            $('#wishlist').text(res);
            $('.favorite' + productId).attr('style', 'padding: 0px;');
            $('.favorite' + productId).attr('onclick', 'addToFavorites(' + productId + ')');
            $('.favorite-i' + productId).attr('class', 'fa fa-heart-broken favorite-i' + productId);
            alert("از لیست علاقه مندی شما حذف شد");
            status_of_favorite();
        },
    });
}

status_of_favorite()

function status_of_favorite() {
    $.ajax({
        type: "GET",
        url: "/csf/status_of_favorite/",
        success: function (res) {
            if (Number(res) === 0) {
                $('#wishlist').hide();
            } else {
                $('#wishlist').show();
                $('#wishlist').text(res);
            }

        }
    });
}
//! ------------------------------------------ Campare --------------------------------------------
status_of_compare_list()

function status_of_compare_list() {
    $.ajax({
        type: "GET",
        url: "/products/status_of_compare_list/",
        success: function (res) {
            if (Number(res) === 0) {
                $('#compare').hide();
            } else {
                $('#compare').show();
                $('#compare').text(res);
            }

        }
    });
}

function addToCampareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/add_to_campare_list/",
        data: {
            productId: productId,
        },
        success: function (res) {
            alert(res);
            $('#compare-' + productId).hide();
            $('#compare-i' + productId).hide();

            status_of_compare_list();
        },
    });
}

function deleteFromCampareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/delete_from_campare_list/",
        data: {
            productId: productId,
        },
        success: function (res) {
            $('#compare-list').html(res)
            status_of_compare_list();
        },
    });
}