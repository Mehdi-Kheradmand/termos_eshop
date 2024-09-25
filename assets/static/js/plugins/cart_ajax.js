
function product_amount_change(id){
    let crf =$('input[name=csrfmiddlewaretoken]').val();
    let product_count = parseInt(document.getElementById(id).value);

    $.ajax({
        url: '/orders/cart/json/amount/',
        type: 'post',
        data: {
            product_id: id,
            product_count,
            csrfmiddlewaretoken: crf,
        },
        success: function (response) {
            if (product_count <= 0){
                                // if product is deleted
                let flex_div = document.getElementById('cart_products_flex')
                flex_div.outerHTML = response["outer"];
                alert(response["amount_of_cart_products"]);
                document.getElementById('header_cart_count').innerText = response["amount_of_cart_products"];
            }
            else
            {
                let total_price_id = 'total_price' + id;
                let single_price_id = 'single_price' + id;
                document.getElementById(single_price_id).innerHTML = response["single_price"] + " <span class=\"amount text-secondary\">تومان</span>";
                document.getElementById(total_price_id).innerHTML = response["total_price"] + " <span class=\"amount text-secondary\">تومان</span>";
                document.getElementById('cart_price').innerHTML = response["final_price"] + " <span class=\"amount\">تومان</span>";
                document.getElementById('header_cart_count').innerText = response["amount_of_cart_products"];
                document.getElementById(id).value = response["product_count"];
                let final_price = response["final_price"];


                if (parseInt(response["transport_price"]) > 0){
                    document.getElementById('transport').innerText = response["transport_price"] + " تومان";

                    // remove comma for transport_price
                    let sp = response["transport_price"].split(',');
                    let transport_price = '0';
                    for (let spKey in sp) {
                        transport_price += sp[spKey];
                    }
                    // remove comma for Final_price
                    let sp_f = final_price.split(',');
                    let final_prc = '0'
                    for (let spFKey in sp_f) {
                        final_prc += sp_f[spFKey];
                    }
                    final_price = parseInt(final_prc) + parseInt(transport_price);
                }else {
                    document.getElementById('transport').innerText = "رایگان";
                }


                document.getElementById('final_price').innerHTML = "<b>" + final_price.toLocaleString('en-US') + "</b>" + " <span class=\"amount\">تومان</span>";
            }
        },
        error: function (response) {
            alert('درخواست نامعتبر');
            window.location.reload();
        }
    });
}


    // ==============================================================================================================
    // ========================================== Ajax_Delete_from cart_page ========================================
    // ==============================================================================================================


    function ajax_cart_delete_product(product_id){
        let crf =$('input[name=csrfmiddlewaretoken]').val();

        // Change i (fa icon) icon to spin ---------------------------------
        let fa_elm = document.getElementById('remove_link_' + product_id);
        fa_elm.removeAttribute('class');
        fa_elm.setAttribute('class', "fal fas fa-spinner fa-spin");

        $.ajax({
            url: '/orders/cart/ajax/c-delete/',
            type: 'post',
            data: {
                product_id,
                csrfmiddlewaretoken: crf,
            },
            success: function (response) {
                let flex_div = document.getElementById('cart_products_flex')
                flex_div.outerHTML = response["outer"];
                document.getElementById('header_cart_count').innerText = response["amount_of_cart_products"];
                qny();
            },
            error: function (response) {
                fa_elm.removeAttribute('class');
                fa_elm.setAttribute('class', "remove");
                alert('خطا! لطفا مجددا تلاش نمایید');
                window.location.reload();
            }
        });
    }

    function qny(){
            jQuery('.quantity').each(function () {
        var spinner = jQuery(this),
            input = spinner.find('input[type="number"]'),
            btnUp = spinner.find('.quantity-up'),
            btnDown = spinner.find('.quantity-down'),
            min = input.attr('min'),
            max = input.attr('max');

        btnUp.click(function () {
            var oldValue = parseFloat(input.val());
            if (oldValue >= max) {
                var newVal = oldValue;
            } else {
                var newVal = oldValue + 1;
            }
            spinner.find("input").val(newVal);
            spinner.find("input").trigger("change");
        });

        btnDown.click(function () {
            var oldValue = parseFloat(input.val());
            if (oldValue <= min) {
                var newVal = oldValue;
            } else {
                var newVal = oldValue - 1;
            }
            spinner.find("input").val(newVal);
            spinner.find("input").trigger("change");
        });

    });

    }