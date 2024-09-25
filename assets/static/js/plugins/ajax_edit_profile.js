
$(document).ready(function () {
    $('button[name=save-account-details]').click(function () {
        do_jobs();
    });
});



function enable_save_button(){
    document.getElementById('save-address').disabled = false;
}

$(document).ready(function () {
    document.getElementById('profile-first-name').addEventListener('change', first_name_info_alert);
    document.getElementById('profile-first-name').addEventListener('keyup', first_name_info_alert);

    document.getElementById('profile-last-name').addEventListener('change', last_name_info_alert);
    document.getElementById('profile-last-name').addEventListener('keyup', last_name_info_alert);

    document.getElementById('profile-phone').addEventListener('change', phone_info_alert);
    document.getElementById('profile-phone').addEventListener('keyup', phone_info_alert);

    document.getElementById('profile-email').addEventListener('change', email_info_alert);
    document.getElementById('profile-email').addEventListener('keyup', email_info_alert);

    document.getElementById('profile-new-password').addEventListener('change', new_password_info_alert);
    document.getElementById('profile-new-password').addEventListener('keyup', new_password_info_alert);

    document.getElementById('phone_verify_code_input').addEventListener('change', verify_code_info_alert);
    document.getElementById('phone_verify_code_input').addEventListener('keyup', verify_code_info_alert);

    // document.getElementById('profile-password').addEventListener('change', password_info_alert);
    // document.getElementById('profile-password').addEventListener('keyup', password_info_alert);

});


function show_verify_button(the_button, my_timer){
    document.getElementById("phone_verify_label").removeAttribute('hidden');
    document.getElementById("phone_verify_code_input").removeAttribute('hidden');
    document.getElementById("btn_reload").removeAttribute('hidden');
    the_button.removeAttribute('class');
    the_button.setAttribute('class', "mt-3 btn btn-success save-account");
    the_button.innerText = "تایید‌ و‌ ذخیره";
    disable_enable_all_inputs(false);

    // Set Timer

        let $countdownOptionEnd = $("#countdown-verify-end");

    $countdownOptionEnd.countdown({
        date: (new Date()).getTime() + my_timer * 1000,
        text: '<span class="day">%s</span><span class="hour">%s</span><span>%s:</span><span>%s</span>',
        end: function () {
            $countdownOptionEnd.html(
                "<input type='hidden' name='btn_resend' id='btn_resend' value='True'><a onclick='do_jobs()' class='btn btn-sm btn-warning'>ارسال مجدد کد</a>"
            );
        }
    });
}

function scroll_top_and_make_page_normal(){
    let the_button=document.getElementById("save-account-details");
    window.scrollTo(0, 0);
    document.getElementById("phone_verify_label").setAttribute('hidden', 'true');
    document.getElementById("phone_verify_code_input").setAttribute('hidden', 'true');
    document.getElementById("btn_reload").setAttribute('hidden', "true");
    the_button.removeAttribute('class');
    the_button.setAttribute('class', "mt-3 btn btn-info save-account");
    the_button.innerText = "بررسی اطلاعات"
    the_button.disabled = true;
    disable_enable_all_inputs(false);
    document.getElementById("btn_goto_dashboard").removeAttribute('hidden');
    document.getElementById("btn_goto_home").removeAttribute('hidden');
    document.getElementById("timer_element").remove();
}

function wait_message(){
    let elem = document.getElementById("success_alert");
    elem.innerText= " درخواست بیش‌از‌حد مجاز! لطفا‌دقایقی‌دیگر‌تلاش‌کنید ";
    elem.removeAttribute('class');
    elem.setAttribute('class', "alert-danger btn-block h5");
    scroll_top_and_make_page_normal();
}


function success_func(){
    let elem = document.getElementById("success_alert");
    elem.innerText=  " تغییرات با موفقیت ثبت شد ";
    elem.removeAttribute('class');
    elem.setAttribute('class', "alert-success btn-block h5");
    scroll_top_and_make_page_normal();
}

function check_and_show_errors(response){
    let error = false;

    if(response['error_list']['first_name']){
        first_name_info_alert(true);
        error = true;
    }
    if(response['error_list']['last_name']){
        last_name_info_alert(true);
        error = true;
    }
    if(response['error_list']['email']){
        email_info_alert(true);
        error = true;
    }
    if(response['error_list']['phone']){
        phone_info_alert(true);
        error = true;
    }
    if(response['error_list']['new_pass']){
        new_password_info_alert(true);
        error = true;
    }
    if(response['error_list']['verify_code']){
        verify_code_info_alert(true);
        document.getElementById("save-account-details").innerText = "تایید‌ و‌ ذخیره";
        error = true;
    }
    if(response['error_list']['wait_message']){
        wait_message();
        error = true;
    }
    return error;
}

function first_name_info_alert(force) {
    let elem = document.getElementById('profile-first-name');
    let _alert = document.getElementById('first_name_alert');
    if (elem.value === '' || force === true) {
        _alert.innerText = "  مقدار نام را وارد نمایید (فقط حروف فارسی) ";
        return false;
    } else {
        _alert.innerText = '';
        return true;
    }
}

function last_name_info_alert(force = false) {
    let elem = document.getElementById('profile-last-name');
    let _alert = document.getElementById('last_name_alert');
    if (elem.value === '' || force === true) {
        _alert.innerText = "   مقدار نام خانوادگی  را وارد نمایید (فقط حروف فارسی) ";
        return false;
    } else {
        _alert.innerText = "";
        return true;
    }
}

function phone_info_alert(force = false) {
    let elem = document.getElementById('profile-phone');
    let _alert = document.getElementById('phone_alert');
    if (elem.value === '' || force === true) {
        _alert.innerText = "  شماره درست نیست یا قبلا ثبت شده";
        return false;
    } else {
        _alert.innerText = "";
        return true;
    }
}

function email_info_alert(force = false) {
    let elem = document.getElementById('profile-email');
    let _alert = document.getElementById('email_alert');
    if (elem.value === '' || force === true) {
        _alert.innerText = "   آدرس ایمیل درست نیست یا قبلا ثبت شده ";
        return false;
    } else {
        _alert.innerText = "";
        return true;
    }
}


function verify_code_info_alert(force = false){
    let elem = document.getElementById('phone_verify_code_input');
    let _alert = document.getElementById('phone_verify_alert');
    if (elem.value === '' || force === true || elem.value.length !== 6 ) {
        _alert.innerText = "   کد تایید درست نیست ";
        return false;
    } else {
        _alert.innerText = "";
        return true;
    }
}

function new_password_info_alert(force = false) {
    let elem = document.getElementById('profile-new-password');
    let _alert = document.getElementById('new_password_alert');

    if (elem.getAttribute('type' ) !== "password" ){
        elem.removeAttribute('type');
        elem.setAttribute('type', "password");
    }

    if (force === true) {
        _alert.innerText = "   رمز عبور باید ۸ الی ۵۰ کاراکتر باشد ";
        return false;
    }else if ((elem.value !== '') && (elem.value.length < 8 || elem.value.length >= 50)) {
        _alert.innerText = "   رمز عبور باید ۸ الی ۵۰ کاراکتر باشد ";
        return false;
    } else {
        _alert.innerText = "";
        return true;
    }
}


// function is_all_inputs_right(){
//     return first_name_info_alert() && last_name_info_alert() &&
//         phone_info_alert() && email_info_alert() && new_password_info_alert();
// }



function disable_enable_all_inputs(en_true_dis_false){

    if (en_true_dis_false){
        document.getElementById('profile-new-password').disabled = false;
        document.getElementById('profile-email').disabled = false;
        document.getElementById('profile-phone').disabled = false;
        document.getElementById('profile-last-name').disabled = false;
        document.getElementById('profile-first-name').disabled = false;
    }else {
        document.getElementById('profile-new-password').disabled = true;
        document.getElementById('profile-email').disabled = true;
        document.getElementById('profile-phone').disabled = true;
        document.getElementById('profile-last-name').disabled = true;
        document.getElementById('profile-first-name').disabled = true;
    }
}

function reload_page(){
    window.location.reload();
}

function do_jobs(){

    const crf = $('input[name=csrfmiddlewaretoken]').val();

    let first_name = document.getElementById('profile-first-name').value;
    let last_name = document.getElementById('profile-last-name').value;
    let phone = document.getElementById('profile-phone').value;
    let email = document.getElementById('profile-email').value;
    let new_pass = document.getElementById('profile-new-password').value;
    let verify_code = document.getElementById('phone_verify_code_input').value;
    let the_button = document.getElementById("save-account-details");

    disable_enable_all_inputs(false);

    let in_verify_form = '';
    if (the_button.innerText === "تایید‌ و‌ ذخیره"){
        in_verify_form = true;
    }

    the_button.innerText = "در حال بررسی";

    $.ajax({
        url: '/profile/edit_profile/',
        type: 'post',
        data: {
            first_name,
            last_name,
            phone,
            new_pass,
            email,
            verify_code,
            in_verify_form,
            csrfmiddlewaretoken: crf,
        },

        success: function(response) {
            disable_enable_all_inputs(true);
            the_button.innerText = "بررسی اطلاعات";

            let error = check_and_show_errors(response);

            if (! error){ // If there is no Error
                if(response['success_msg']){ // Success --------------------------------------------
                    success_func();
                }else{ // show the verify button ----------------------------------------------------
                    show_verify_button(the_button, response['my_timer']);
                }
            }
        },
        error: function () {
            alert('خطا! لطفا دوباره اقدام کنید ');
            window.location.reload();
        }
    });
}