

    // ==============================================================================================================
    // ========================================== Ajax_Delete_from Sidebar ==========================================
    // ==============================================================================================================


function remove_detail(product_id) { // 11/04/2022 - m/d/y
    let crf =$('input[name=csrfmiddlewaretoken]').val();

    // Change i (fa icon) icon to spin ---------------------------------
    let fa_elm = document.getElementById('cross_fa_' + product_id);
    fa_elm.removeAttribute('class');
    fa_elm.setAttribute('class', "fal fas fa-spinner fa-spin");
    fa_elm.disabled=true;

    $.ajax({
        url: '/orders/cart/ajax/s-delete/',
        type: 'post',
        data: {
            product_id,
            csrfmiddlewaretoken: crf,
        },
        success: function (response) {
            $('#ajax_sidebar_cart').html(response["outer"]);
            document.getElementById('header_cart_count').innerText = response["amount_of_cart_products"];
            qny();
        },
        error: function (response) {
            alert('خطا! لطفا مجددا تلاش نمایید');
            window.location.reload();
        }
    });
}




// ajax - get
// function remove_detail(pd){
//     $.get('/orders/cart/json/delete/', {
//         product_id: pd,
//     }).then(res =>{
//         $('#ajax_sidebar_cart').html(res);
//
//
//         if (document.getElementById('side_cart_count') != null){
//             let count = document.getElementById('side_cart_count').innerHTML;
//             $('#header_cart_count').html(count);
//         }
//         else {
//             $('#header_cart_count').html(0);
//         }
//     });
// }



// get a tag value command
// let input_val = $('#id').val();

// refresh the page
//location.reload()


// scroll sample
//window.scrollTo()
// document.getElementById('id').scrollIntoView( {behavior: "smooth"})