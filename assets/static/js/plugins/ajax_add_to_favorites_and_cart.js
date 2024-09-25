function add_to_wishlist(p_id, tag_a_id){

    let wish_fa_tag = document.getElementById(tag_a_id.replace('_a_', '_fa_'));
    let wish_a_tag = document.getElementById(tag_a_id);
    const crf = $('input[name=csrfmiddlewaretoken]').val();
    let a_tag_class = wish_a_tag.getAttribute("class");

    // spinner
    // wish_fa_tag.removeAttribute('class');
    if (wish_fa_tag) {
        wish_fa_tag.setAttribute('class', "fal fas fa-spinner fa-spin");
    }
    wish_a_tag.removeAttribute("href");
    //btn btn-light wishlist active

    $.ajax({
        url: '/products/ajax/wishlist_add_remove/',
        type: 'post',
        data: {
            p_id,
            csrfmiddlewaretoken: crf,
        },
        success: function(response) {
            if (document.location.href.indexOf("dashboard") > -1) {  // if we are in the dashboard page
                console.log(response['outer']);
                document.getElementById('dashboard-wishlist-layout').innerHTML = response['outer'];
            }else if(response['add_remove'] === 'added' ){

                wish_a_tag.removeAttribute('class');
                wish_a_tag.setAttribute('class' ,a_tag_class+"active");
                wish_a_tag.setAttribute("href", "#wishlist");
                wish_fa_tag.removeAttribute('class');
                wish_fa_tag.setAttribute('class', "fal fa-heart");

            }else if (response['add_remove'] === 'removed'){

                if (document.location.href.indexOf("profile/wishlist") > -1) {  // if we are in the dashboard page
                    console.log(response['outer']);
                    document.getElementById('wishlist_items_row').innerHTML = response['outer'];
                }else {
                    wish_a_tag.removeAttribute('class');
                    wish_a_tag.setAttribute('class' ,a_tag_class.replace("active", ''));
                    wish_a_tag.setAttribute("href", "#wishlist");
                    wish_fa_tag.removeAttribute('class');
                    wish_fa_tag.setAttribute('class', "fal fa-heart");
                }

            }else if (response['add_remove'] === 'login'){

                window.location = response['login_url'];

            }else {
                alert('خطا! لطفا دوباره اقدام کنید ');
                window.location.reload();
            }
        //    clear spinner
        },
        error: function () {
            alert('خطا! لطفا دوباره اقدام کنید ');
            window.location.reload();
        }
    });
}

// ----------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------

function add_to_cart(p_id, tag_a_id){

    if(tag_a_id === "btn_add_to_cart"){
        // when called at the product_detail page
        add_to_cart_from_detail_page(p_id);
    } else {
        // when called in the products_list page

        // Get Elements
        let fa_elm = document.getElementById(tag_a_id.replace('_a_', '_fa_'));
        let elm_a_tag = document.getElementById(tag_a_id);


        // add from product_list
        const crf = $('input[name=csrfmiddlewaretoken]').val();

        // Change i (fa icon) icon to spin ---------------------------------
        fa_elm.removeAttribute('class');
        fa_elm.setAttribute('class', "fal fas fa-spinner fa-spin");

        // Change Tag ----------------------------------------------------
        let new_a_tag = document.createElement('a');
        new_a_tag.setAttribute('id', tag_a_id);
        new_a_tag.setAttribute('title', "افزودن به سبد");
        // without href > no click available
        // new_tag.setAttribute('onclick', "add_to_cart(" + p_id + ")");


        // new_elm.setAttribute('class', "fal fa-shopping-cart");
        // new_elm.setAttribute('style', "color:#1ff47b");
        new_a_tag.innerHTML = elm_a_tag.innerHTML;
        elm_a_tag.parentNode.replaceChild(new_a_tag, elm_a_tag);

        $.ajax({
            url: '/orders/ajax/add_to_cart/',
            type: 'post',
            data: {
                product_id: p_id,
                product_count: '1',
                csrfmiddlewaretoken: crf,
            },
            success: function (response) {

                // change cart icon
                let fa_elm = document.getElementById(tag_a_id.replace('_a_', '_fa_'));
                fa_elm.removeAttribute('class');
                fa_elm.setAttribute('class', "fal fa-shopping-cart");
                fa_elm.setAttribute('style', "color:#1ff47b");

                // add 'href' and 'onclick' to tag
                let a_tag = document.getElementById(tag_a_id);
                a_tag.setAttribute('href', "#cart");
                a_tag.setAttribute('onclick', "add_to_cart("+p_id+",this.id)");

                update_and_popup_sidebar_cart(response["out_tag"]);

            },
            error: function () {
                alert('خطا! لطفا دوباره اقدام کنید ');
                window.location.reload();
            }
        });
    }
}


function add_to_cart_from_detail_page(p_id){

    let btn_tag = document.getElementById("btn_add_to_cart");
    let order_count = document.getElementById("id_order_count").value;
    const crf = $('input[name=csrfmiddlewaretoken]').val();

    // Disable Button ----------------------------------------------------
    btn_tag.innerText = "در حال پردازش ...";
    btn_tag.disabled=true;

    $.ajax({
        url: '/orders/ajax/add_to_cart/',
        type: 'post',
        data: {
            product_id: p_id,
            product_count: order_count,
            csrfmiddlewaretoken: crf,
        },
        success: function (response) {

        if(response["out_of_stock"]){
            // out of stock
            btn_tag.removeAttribute('class');
            btn_tag.setAttribute('class', "btn btn-danger add-to-cart-btn");
            btn_tag.innerText = "حداکثر موجودی به سبد خرید افزوده شده";
        } else {
            // back the btn to normal
            btn_tag.innerText = "افزودن به سبد خرید";
            btn_tag.disabled=false;
        }

        update_and_popup_sidebar_cart(response["out_tag"]);

        },
        error: function () {
            alert('خطا! لطفا دوباره اقدام کنید ');
            window.location.reload();
        }
    });
}


function update_and_popup_sidebar_cart(outer_html){

    // put html from response
    $('#ajax_sidebar_cart').html(outer_html);
    if (document.getElementById('side_cart_count') != null) {
        let count = document.getElementById('side_cart_count').innerHTML
        $('#header_cart_count').html(count);
    } else {
        $('#header_cart_count').html(0);
    }

    // open cart popup
    $('#offcanvasCart').addClass('active');
    $('body').addClass('offcanvas-page');
    $('.offcanvas-overlay').addClass('active');
}