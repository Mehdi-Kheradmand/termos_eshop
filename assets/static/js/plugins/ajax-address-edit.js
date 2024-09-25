$(document).ready(function () {

    $('select.category').niceSelect();

    const crf = $('input[name=csrfmiddlewaretoken]').val();
    $('button[name=save-address]').click(function () {
    let name = document.getElementById('billing-first-name').value;
    let last_name = document.getElementById('billing-last-name').value;
    let state = document.getElementById('billing-state').value;
    let city = document.getElementById('billing-city').value;
    let address = document.getElementById('billing-address').value;
    let postcode = document.getElementById('billing-postcode').value;
    let phone = document.getElementById('billing-phone').value;
    let email = document.getElementById('billing-email').value;
    let back_address = document.getElementById('back-address').value;


        $.ajax({
            url: '/profile/address_edit/ajax/',
            type: 'post',
            data: {
                name: name,
                last_name:last_name,
                state:state,
                city:city,
                address:address,
                postcode:postcode,
                phone:phone,
                email:email,
                back_address,
                csrfmiddlewaretoken: crf,
            },
            success: function(response) {
                let error = false;

                if(response.error_list['first_name']){
                    name_info_alert(true);
                    error = true;
                }
                if(response.error_list['last_name']){
                    last_name_info_alert(true);
                    error = true;
                }
                if(response.error_list['state']){
                    state_info_alert(true);
                    error = true;
                }
                if(response.error_list['city']){
                    city_info_alert(true);
                    error = true;
                }
                if(response.error_list['address']){
                    address_info_alert(true);
                    error = true;
                }
                if(response.error_list['postcode']){
                    postcode_info_alert(true);
                    error = true;
                }
                if(response.error_list['phone']){
                    phone_info_alert(true);
                    error = true;
                }
                if(response.error_list['email']){
                    email_info_alert(true);
                    error = true;
                }

                if (! error){
                    // reaction depends on where user is come from
                    if(back_address.includes("checkouts")){
                        alert('اطلاعات با موفقیت ثبت شد');
                        window.location.href = back_address;
                    }else {
                        document.getElementById('info_alert').innerText = "اطلاعات با موفقیت ثبت شد";
                        document.getElementById('back-button').removeAttribute("type");
                        document.getElementById('back-button').setAttribute("type", "button");
                        // let info_element = document.getElementById('info_alert');
                        // window.scrollTo(0, 10,);
                        document.getElementById('save-address').disabled = true;
                        $("html, body").animate({ scrollTop: 0 }, "smooth");

                    }
                }
            },
            error: function (response) {
                alert('خطا! لطفا مجددا تلاش نمایید ');
                window.location.reload();
            }
        });

    });
});



function enable_save_button(){
    document.getElementById('save-address').disabled = false;
}

function go_back(){
    window.location.href = document.getElementById('back-address').value;
}

$(document).ready(function () {
    document.getElementById('billing-first-name').addEventListener('change', name_info_alert);
    document.getElementById('billing-first-name').addEventListener('keydown', name_info_alert);

    document.getElementById('billing-last-name').addEventListener('change', last_name_info_alert);
    document.getElementById('billing-last-name').addEventListener('keydown', last_name_info_alert);

    document.getElementById('billing-postcode').addEventListener('change', postcode_info_alert);
    document.getElementById('billing-postcode').addEventListener('keydown', postcode_info_alert);

    document.getElementById('billing-address').addEventListener('change', address_info_alert);
    document.getElementById('billing-address').addEventListener('keydown', address_info_alert);

    document.getElementById('billing-phone').addEventListener('change', phone_info_alert);
    document.getElementById('billing-phone').addEventListener('keydown', phone_info_alert);

    document.getElementById('billing-email').addEventListener('change', email_info_alert);
    document.getElementById('billing-email').addEventListener('keydown', email_info_alert);

    document.getElementById('billing-city').addEventListener('change', city_info_alert);
    document.getElementById('billing-city').addEventListener('keydown', city_info_alert);
});

    function name_info_alert(force) {
        let elem = document.getElementById('billing-first-name');
        let _alert = document.getElementById('first_name_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = " نام را وارد نمایید (فقط حروف فارسی)";
            document.getElementById('save-address').disabled = true;
        } else {
            _alert.innerText = "";
            document.getElementById('save-address').disabled = false;
        }
    }

    function last_name_info_alert(force = false) {
        let elem = document.getElementById('billing-last-name');
        let _alert = document.getElementById('last_name_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = " نام خانوادگی  را وارد نمایید (فقط حروف فارسی)";
            document.getElementById('save-address').disabled = true;
        } else {
            _alert.innerText = "";
            document.getElementById('save-address').disabled = false;
        }
    }

    function address_info_alert(force = false) {
        let elem = document.getElementById('billing-address');
        let _alert = document.getElementById('address_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = "آدرس را وارد نمایید (فقط حروف فارسی)";
            document.getElementById('save-address').disabled = true;
        } else {
            _alert.innerText = "";
            document.getElementById('save-address').disabled = false;
        }
    }

    function postcode_info_alert(force = false) {
        let elem = document.getElementById('billing-postcode');
        let _alert = document.getElementById('postcode_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = "کد پستی را وارد نمایید (فقط عدد)";
            document.getElementById('save-address').disabled = true;
        } else {
            _alert.innerText = "";
            document.getElementById('save-address').disabled = false;
        }
    }

    function phone_info_alert(force = false) {
        let elem = document.getElementById('billing-phone');
        let _alert = document.getElementById('phone_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = "شماره موبایل را وارد نمایید (فقط اعداد)";
            document.getElementById('save-address').disabled = true;
        } else {
            _alert.innerText = "";
            document.getElementById('save-address').disabled = false;
        }
    }

    function email_info_alert(force = false) {
        let elem = document.getElementById('billing-email');
        let _alert = document.getElementById('email_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = "آدرس ایمیل صحیح وارد نمایید";
            document.getElementById('save-address').disabled = true;
        } else {
            _alert.innerText = "";
            document.getElementById('save-address').disabled = false;
        }
    }

    function city_info_alert(force = false) {
        let elem = document.getElementById('billing-city');
        let _alert = document.getElementById('city_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = "شهر را وارد نمایید (فقط حروف فارسی)";
            document.getElementById('save-address').disabled = true;
        } else {
            _alert.innerText = "";
            document.getElementById('save-address').disabled = false;
        }
    }

    function state_info_alert(force = false) {
        let elem = document.getElementById('billing-state');
        let _alert = document.getElementById('state_alert');
        if (elem.value === '' || force === true) {
            _alert.innerText = "یک استان انتخاب کنید";
            document.getElementById('save-address').disabled = true;
        } else {
            document.getElementById('save-address').disabled = false;
            _alert.innerText = "";
        }
    }