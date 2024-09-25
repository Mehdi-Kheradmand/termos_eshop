$(document).ready(function () {

    $('button[name=btn_send]').click(function () {
        email_phone();
    });
});


// ====================================================================================================================
// ====================================================================================================================


function email_phone(){

    document.getElementById("btn_send").disabled = true;
    document.getElementById("btn_send").innerText = "درحال پردازش ...";

    let crf = $('input[name=csrfmiddlewaretoken]').val();
    let input_email_phone = document.getElementById('id_input_email_phone').value;
    let g_recaptcha_response = document.getElementById('g-recaptcha-response').value;
    let error_viewer = document.getElementById("error_viewer");
    let p_tag = document.createElement('p');
    let next_req_addr = document.getElementById('id_input_next_req_addr').value;

    p_tag.setAttribute("class", "h5");

// let back_address = document.getElementById('back-address').value;

    $.ajax({
        url: next_req_addr,
        type: 'post',
        data: {
            input_email_phone,
            g_recaptcha_response,
            csrfmiddlewaretoken: crf,
        },
        success: function(response) {
            document.getElementById("btn_send").disabled = false;
            document.getElementById("btn_send").innerText = "ورود به حساب کاربری";

            if(response["is_there_error"]) {
                if(response['reload_recaptcha']){
                    grecaptcha.reset();
                }
                for (let er_message in response["error_list"]) {
                    p_tag.innerText = response["error_list"][er_message];
                    set_error(error_viewer, p_tag);
                }
            }else{
                document.getElementById('user_flex_form').outerHTML = response["outer"];
                show_timer(response['otp_timer']);
            }
        },
        error: function (response) {
            document.getElementById("btn_send").disabled = false;
            document.getElementById("btn_send").innerText = "ورود به حساب کاربری";
            alert('خطا! لطفا مجددا تلاش نمایید Error 1');
            window.location.reload();
        }
    });
}


// ====================================================================================================================
// ====================================================================================================================


function password_exchange(btn_id){

    document.getElementById("btn_send").disabled = true;
    document.getElementById("btn_send").innerText = "درحال پردازش ...";
    const crf = $('input[name=csrfmiddlewaretoken]').val();

    let input_password = document.getElementById('id_input_password').value;
    let input_hidden_email = document.getElementById('id_input_hidden_email').value;
    let error_viewer = document.getElementById("error_viewer");
    let p_tag = document.createElement('p');
    let next_req_addr = document.getElementById('id_input_next_req_addr').value;

        $.ajax({
            url: next_req_addr,
            type: 'post',
            data: {
                input_password,
                input_hidden_email,
                csrfmiddlewaretoken: crf,
            },
            success: function(response) {
                document.getElementById("btn_send").disabled = false;
                document.getElementById("btn_send").innerText = "ورود به حساب کاربری";

                if(response["is_there_error"]) {
                    error_viewer.innerHTML = null;
                    for (let er_message in response["error_list"]) {
                        p_tag.innerText = response["error_list"][er_message];
                        set_error(error_viewer, p_tag);
                    }
                }else{
                    // there is no error for password then user is logged in > show the next url
                    goto_next_url();
                }
            },
            error: function (response) {
                document.getElementById("btn_send").disabled = false;
                document.getElementById("btn_send").innerText = "ورود به حساب کاربری";
                alert('خطا! لطفا مجددا تلاش نمایید Error 2');
                window.location.reload();
            }
        });
}


// ====================================================================================================================
// ====================================================================================================================


function otp_func(btn_id){
    document.getElementById("btn_send").disabled = true;
    document.getElementById("btn_send").innerText = "درحال پردازش ...";
    const crf = $('input[name=csrfmiddlewaretoken]').val();

    let input_otp = document.getElementById('id_input_otp').value;
    let input_hidden_phone = document.getElementById('id_input_hidden_phone').value;
    let error_viewer = document.getElementById("error_viewer");
    let p_tag = document.createElement('p');
    let next_req_addr = document.getElementById('id_input_next_req_addr').value;

        $.ajax({
            url: next_req_addr,
            type: 'post',
            data: {
                input_otp,
                input_hidden_phone,
                csrfmiddlewaretoken: crf,
            },
            success: function(response) {
                document.getElementById("btn_send").disabled = false;
                document.getElementById("btn_send").innerText = "ورود به حساب کاربری";

                if(response["is_there_error"]) {
                    error_viewer.innerHTML = null;
                    for (let er_message in response["error_list"]) {
                        p_tag.innerText = response["error_list"][er_message];
                        set_error(error_viewer, p_tag);
                    }
                }else{
                    // goto ?next url -OR- receive user info for register
                    if (response['outer']){
                        document.getElementById('user_flex_form').outerHTML = response["outer"];
                    }else {
                        goto_next_url();
                    }
                }
            },
            error: function (response) {
                document.getElementById("btn_send").disabled = false;
                document.getElementById("btn_send").innerText = "ورود به حساب کاربری";
                alert('خطا! لطفا مجددا تلاش نمایید Error 3');
                window.location.reload();
            }
        });
}


// ====================================================================================================================
// ====================================================================================================================


function otp_reset(){
    document.getElementById("btn_send").disabled = true;
    document.getElementById("btn_send").innerText = "درحال پردازش ...";
    const crf = $('input[name=csrfmiddlewaretoken]').val();

    let input_otp = '00000';
    let input_hidden_phone = document.getElementById('id_input_hidden_phone').value;
    let error_viewer = document.getElementById("error_viewer");
    let p_tag = document.createElement('p');

        $.ajax({
            url: "/user/login/ajax_otp_reset/",
            type: 'post',
            data: {
                input_otp,
                input_hidden_phone,
                csrfmiddlewaretoken: crf,
                'reset_request': true,
            },
            success: function(response) {
                document.getElementById("btn_send").disabled = false;
                document.getElementById("btn_send").innerText = "ورود به حساب کاربری";

                if(response["is_there_error"]) {
                    error_viewer.innerHTML = null;
                    for (let er_message in response["error_list"]) {
                        p_tag.innerText = response["error_list"][er_message];
                        set_error(error_viewer, p_tag);
                    }
                }else{
                    document.getElementById('user_flex_form').outerHTML = response["outer"];
                    show_timer(response['otp_timer']);
                }
            },
            error: function (response) {
                document.getElementById("btn_send").disabled = false;
                document.getElementById("btn_send").innerText = "ورود به حساب کاربری";
                alert('خطا! لطفا مجددا تلاش نمایید Error 4');
                window.location.reload();
            }
        });
}


// ====================================================================================================================
// ====================================================================================================================


function register_func(){
    document.getElementById("btn_send").disabled = true;
    document.getElementById("btn_send").innerText = "درحال پردازش ...";
    const crf = $('input[name=csrfmiddlewaretoken]').val();
    let next_req_addr = document.getElementById('id_input_next_req_addr').value;

    // Get the form:
    let input_hidden_hash_code = document.getElementById('id_input_hidden_hash_code').value;
    let input_phone_number = document.getElementById('id_input_phone_number').value;
    let input_first_name = document.getElementById('id_input_first_name').value;
    let input_last_name = document.getElementById('id_input_last_name').value;
    let input_email = document.getElementById('id_input_email').value;
    let input_password = document.getElementById('id_input_password').value;

    // Get elements:
    let error_viewer = document.getElementById("error_viewer");
    let p_tag = document.createElement('p');

    // send Ajax Request
    $.ajax({
        url: next_req_addr,
        type: 'post',
        data: {
            input_hidden_hash_code,
            input_phone_number,
            input_first_name,
            input_last_name,
            input_email,
            input_password,
            csrfmiddlewaretoken: crf,
        },
        success: function(response) {
            document.getElementById("btn_send").disabled = false;
            document.getElementById("btn_send").innerText = "ورود به حساب کاربری";

            if(response["is_there_error"]) {
                error_viewer.innerHTML = null;
                for (let er_message in response["error_list"]) {
                    p_tag.innerText = response["error_list"][er_message];
                    set_error(error_viewer, p_tag);
                }
            }else{  // Success without Error
                // show the wellcome page
                document.getElementById('user_flex_form').outerHTML = response["outer"];
            }
        },
        error: function (response) {
            document.getElementById("btn_send").disabled = false;
            document.getElementById("btn_send").innerText = "ورود به حساب کاربری";
            alert('خطا! لطفا مجددا تلاش نمایید Error 5');
            window.location.reload();
        }
    });
}


// ====================================================================================================================
// ====================================================================================================================


function set_error(error_viewer, p_tag){
    // error_viewer.innerHTML = "";
    error_viewer.appendChild(p_tag);
    error_viewer.setAttribute("class", "h-100 alert alert-danger");
    $("html, body").animate({ scrollTop: 0 }, "smooth");
}


function show_timer(my_timer){
    let $countdownOptionEnd = $("#countdown-verify-end");
    $countdownOptionEnd.countdown({
        date: (new Date()).getTime() + my_timer * 1000, // 1 minute later
        text: '<span class="day">%s</span><span class="hour">%s</span><span>: %s</span><span>%s</span>',
        end: function () {
            $countdownOptionEnd.html(
                "<input type='hidden' name='resend' id='resend' value='True'><a onclick='otp_reset()' class='link-border-verify form-account-link'>ارسال مجدد</a>"
            );
        }
    });
}

function goto_next_url(){
    let next_url = location.search.substring(1).split('&');
    if (next_url[0].includes("next")){
        console.log("next_url[0] = " + next_url[0]);
        let next_split = next_url[0].split('=');
        let the_final_address = "";
        console.log("For Result is :");
        // for (let nextSplitKey in next_split) {
        //     console.log("next_split[" + nextSplitKey + "] = " + next_split[nextSplitKey]);
        // }
        for (let i = 1; i < next_split.length; i++) {
            // console.log("next_split[" + i + "] = " + next_split[i]);
            if (i === 1){
                the_final_address += next_split[i];
            }else {
                the_final_address += '=' + next_split[i] + '&';
            }
        }
        // console.log("----------------------");
        // console.log("Final Result is : " + the_final_address);
        window.location.href = the_final_address;
    }else {
        window.location.href = "/";
    }
}