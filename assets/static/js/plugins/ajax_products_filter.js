$(document).ready(function () {

    $(document).on('click', '#newest-tab, #cheapest-tab, #most-expensive-tab, #btn_add_filter, #btn_add_filter2', function () {
            // دریافت مقدار "درخواست مرتب سازی بر اساس قیمت" که توی آیدی قرار دادیم
            let sort_order = this.id;

            if (sort_order.includes("btn")){
                let sort_order_text = document.getElementById("dropdownMenuLink").innerText;
                if(sort_order_text.includes("ارزان")){
                    sort_order = "cheapest-tab";
                }else if(sort_order_text.includes("جدید")){
                    sort_order = "newest-tab";
                }else if(sort_order_text.includes("گران")){
                    sort_order = "most-expensive-tab";
                }
            }

            // تبدیل نوشته مرتب سازی قیمت به درحال انجام
            // let sort_menu_text = this.innerText;
            document.getElementById('dropdownMenuLink').innerText = 'درحال‌انجام..';
            // تبدیل نوشته مرتب سازی قیمت به درحال انجام


            // ریختن دکمه های اعمال فیلتر به متغیر برای راحتی کار
            let btn1 = document.getElementById('btn_add_filter');
            let btn2 = document.getElementById('btn_add_filter2');
            // ریختن دکمه های اعمال فیلتر به متغیر برای راحتی کار

            // برای اینکه درخواست دسته بندی هم ارسال بشه به آدرس همین صفحه ای که توشیم ارسالش میکنیم
            let url = document.location.href.toString();

            // دریافت مقدار q برای زمانی که در حالت جستجو بودیم
            let q = document.getElementById('q').value;

            // disable ajax request links and buttons
            document.getElementById('dropdownMenuLink').setAttribute("style","pointer-events: none");
            btn1.innerText = 'پردازش ...';
            btn1.disabled = true;
            btn2.innerText = 'پردازش ...';
            btn2.disabled = true;

            //برای دریافت فیلتر قیمت درخواست شده از طرف کاربر باید بدانیم از اسلایدر موبایل درخواست شده یا دسکتاپ بعد مقدار رو بفرستیم به بک
            let price_limit = document.getElementById('slider-non-linear-step-value').innerText;
            if(this.id === btn2.id){
                price_limit = document.getElementById('slider-non-linear-step-value2').innerText;
            }

            $.get(url, {
                price_limit: price_limit,
                q:q,
                sort_order:sort_order,
            }).then(res =>{
                $('#ajax_products_list').html(res);
                console.log(res);
                price_slider();
                let btn1 = document.getElementById('btn_add_filter');
                let btn2 = document.getElementById('btn_add_filter2');
                btn1.innerText = 'انجام فیلتر';
                btn1.disabled = false;
                btn2.innerText = 'مرتب سازی براساس';
                btn2.disabled = false;
                // document.getElementById('dropdownMenuLink').innerText = sort_menu_text;
                document.getElementById('dropdownMenuLink').removeAttribute("style");
            });

    });

});


function price_slider() {
    let nonLinearStepSlider = document.getElementById('slider-non-linear-step');
    let nonLinearStepSlider2 = document.getElementById('slider-non-linear-step2');

    let db_max_price = document.getElementById('db_max_price').value;
    let start_price = document.getElementById('start_price').value;
    let end_price = document.getElementById('end_price').value;
    console.log('db_max_price : ' + db_max_price );
    console.log('end_price : ' + end_price );

    // calibrate price filter (Desktop Style)
    if ($('#slider-non-linear-step').length) {
        noUiSlider.create(nonLinearStepSlider, {
            start: [parseInt(start_price), parseInt(end_price)],
            connect: true,
            direction: 'rtl',
            format: wNumb({
                decimals: 0,
                thousand: ','
            }),
            range: {
                'min': [0],
                '10%': [1000, 1000],
                // '50%': [40000, 1000],
                'max': [parseInt(db_max_price)],
            }
        });
        var nonLinearStepSliderValueElement = document.getElementById('slider-non-linear-step-value');

        nonLinearStepSlider.noUiSlider.on('update', function (values) {
            nonLinearStepSliderValueElement.innerHTML = values.join(' - ');
        });
    }

    // calibrate price filter (Mobile Style)
    if ($('#slider-non-linear-step2').length) {
        noUiSlider.create(nonLinearStepSlider2, {
            start: [parseInt(start_price), parseInt(end_price)],
            connect: true,
            direction: 'rtl',
            format: wNumb({
                decimals: 0,
                thousand: ','
            }),
            range: {
                'min': [0],
                '10%': [1000, 1000],
                // '50%': [40000, 1000],
                'max': [parseInt(db_max_price)],
            }
        });
        var nonLinearStepSliderValueElement2 = document.getElementById('slider-non-linear-step-value2');

        nonLinearStepSlider2.noUiSlider.on('update', function (values) {
            nonLinearStepSliderValueElement2.innerHTML = values.join(' - ');
        });
    }
}
