$(document).ready(function () {


    $('.products-gallery').magnificPopup({
        delegate: 'a.image-popup-vertical-fit',
        type: 'image',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
        }
    });

    if ($('.gallery-slider').length) {
        var gallerySlider = new Swiper('.gallery-slider', {
            centeredSlides: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
            },
        });
        var gallerySliderThumbs = new Swiper('.gallery-slider-thumbs', {
            slidesPerView: 5,
            touchRatio: 0.2,
            slideToClickedSlide: true,
            centeredSlides: true,
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });
        gallerySlider.controller.control = gallerySliderThumbs;
        gallerySliderThumbs.controller.control = gallerySlider;
    }


    const csrf = $('input[name=csrfmiddlewaretoken]').val();

    $('button[name=submit-comment]').click(function () {
    let msg = document.getElementById('comment-box').value;
    let product_id = document.getElementById('id_product_id').value;
    let g_recaptcha_response = document.getElementById('g-recaptcha-response').value;

        $.ajax({
            url: '/product_comments/ajax/',
            type: 'post',
            data: {
                msg,
                product_id,
                csrfmiddlewaretoken: csrf,
                'g-recaptcha-response': g_recaptcha_response,
            },
            success: function(response) {
                document.getElementById('comment_list').innerHTML = response.ol_tag;
                document.getElementById('comment-box').value='';
                document.getElementById('comment_added').innerText = 'دیدگاه شما دریافت شد و پس از تایید نمایش داده خواهد شد - با تشکر';
                document.getElementById('submit-comment').disabled=true;

            },
            error: function (response) {
                if (response.status === 401){
                    let _alert = document.getElementById('comment-alert');
                    _alert.innerText = "عبارت امنیتی تایید نشد";
                    document.getElementById('des-tab').scrollIntoView({behavior: 'smooth'});

                }else if (response.status === 400){
                    let _alert = document.getElementById('comment-alert');
                    _alert.innerText = "دیدگاه را بنویسید (حداقل ۱۰ حرف) ";
                    document.getElementById('des-tab').scrollIntoView({behavior: 'smooth'});
                }else{
                    alert(response.status);
                }
            }
        });

    });

});


$(document).ready(function () {
    document.getElementById('comment-box').addEventListener('change', comment_box_alert);


    function comment_box_alert(force = false) {
        let elem = document.getElementById('comment-box');
        let _alert = document.getElementById('comment-alert');
        if (elem.value === '' || force === true || elem.value.length<10 ) {
            _alert.innerText = " متن دیدگاه را بنویسید (حداقل ۱۰ حرف) ";
            document.getElementById('des-tab').scrollIntoView({behavior: 'smooth'});
        } else {
            _alert.innerText = "";
        }
    }
});
