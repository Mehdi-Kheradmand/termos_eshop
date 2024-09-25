$(document).ready(function () {

    // sliderMain
    var swiper = new Swiper(".mainSlider", {
        spaceBetween: 30,
        effect: "fade",
        loop: true,
        centeredSlides: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        keyboard: true,
    });

    // sliderAmazing
    var swiper = new Swiper(".sliderAmazing", {
        slidesPerView: 5,
        spaceBetween: 3,
        slidesPerGroup: 1,
        loop: true,
        loopFillGroupWithBlank: true,
        breakpoints: {
            300: {
                slidesPerView: 1,
                spaceBetween: 1,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            470: {
                slidesPerView: 2,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            640: {
                slidesPerView: 2,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            1400: {
                slidesPerView: 5,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });

    // sliderProduct
    var swiper = new Swiper(".sliderProduct", {
        slidesPerView: 4,
        spaceBetween: 10,
        slidesPerGroup: 1,
        loopFillGroupWithBlank: true,
        breakpoints: {
            300: {
                slidesPerView: 1,
                spaceBetween: 1,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            470: {
                slidesPerView: 2,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            640: {
                slidesPerView: 2,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
            1400: {
                slidesPerView: 5,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
            },
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });

    // sliderMoments
    var swiper = new Swiper(".slider-moments", {
        autoplay: {
            delay: 5000,
            disableOnInteraction: false
        },
        speed: 500,
        loop: true,
        pagination: {
            el: ".swiper-pagination",
            type: "fraction"
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev"
        },
        on: {
            init: function () {
                $(".swiper-progress-bar").removeClass("animate");
                $(".swiper-progress-bar").removeClass("active");
                $(".swiper-progress-bar").eq(0).addClass("animate");
                $(".swiper-progress-bar").eq(0).addClass("active");
            },
            slideChangeTransitionStart: function () {
                $(".swiper-progress-bar").removeClass("animate");
                $(".swiper-progress-bar").removeClass("active");
                $(".swiper-progress-bar").eq(0).addClass("active");
            },
            slideChangeTransitionEnd: function () {
                $(".swiper-progress-bar").eq(0).addClass("animate");
            }
        }
    });
    $('.slider-moments').hover(function () {
        swiper.autoplay.stop();
        $('.swiper-progress-bar').removeClass('animate');
    }, function () {
        swiper.autoplay.start();
        $('.swiper-progress-bar').addClass('animate');
    });

});