$(document).ready(function () {
    const csrf = $('input[name=csrfmiddlewaretoken]').val();

    $('button[name=send-btn]').click(function () {
    let form_name = document.getElementById('form_name').value;
    let form_email = document.getElementById('form_email').value;
    let form_title = document.getElementById('form_title').value;
    let form_message = document.getElementById('form_message').value;
    let g_recaptcha_response = document.getElementById('g-recaptcha-response').value;

        $.ajax({
            url: '/contact-us/',
            type: 'post',
            data: {
                form_name,
                form_email,
                form_title,
                form_message,
                csrfmiddlewaretoken: csrf,
                'g-recaptcha-response': g_recaptcha_response,
            },
            success: function(response) {
                if(response.is_it_valid){
                    document.getElementById('form_name').value = '';
                    document.getElementById('form_email').value='';
                    document.getElementById('form_title').value='';
                    document.getElementById('form_message').value='';
                    document.getElementById('success_alert').innerText = " پیام شما با موفقیت ارسال شد - با تشکر ";
                    document.getElementById('captcha-info').classList.remove('alert-danger');
                    document.getElementById('captcha-info').innerText='عبارت امنیتی :';
                    document.getElementById('send-btn').disabled=true;
                }else {
                    if (response.error_list['name']){
                        document.getElementById('form_name').setAttribute("class", "border-danger");
                    }
                    if (response.error_list['email']){
                        document.getElementById('form_email').setAttribute("class", "border-danger");
                    }
                    if (response.error_list['title']){
                        document.getElementById('form_title').setAttribute("class", "border-danger");
                    }
                    if (response.error_list['message']){
                        document.getElementById('form_message').setAttribute("class", "border-danger");
                    }
                    if (response.error_list['captcha']){
                        document.getElementById('captcha-info').setAttribute("class", "alert-danger");
                        document.getElementById('captcha-info').innerText='عبارت امنیتی صحیح نیست';
                    }
                }

            },
            error: function (response) {
                alert('عملیات ناموفق');
            }
        });

    });
});


$(document).ready(function () {
    document.getElementById('form_name').addEventListener('change', name_alert);
    document.getElementById('form_email').addEventListener('change', email_alert);
    document.getElementById('form_title').addEventListener('change', title_alert);
    document.getElementById('form_message').addEventListener('change', message_alert);
    document.getElementById('form_name').addEventListener('keydown', name_alert);
    document.getElementById('form_email').addEventListener('keydown', email_alert);
    document.getElementById('form_title').addEventListener('keydown', title_alert);
    document.getElementById('form_message').addEventListener('keydown', message_alert);

    const btn = document.getElementById('send-btn');

    function message_alert(force = false) {
        let elem = document.getElementById('form_message');
        elem.classList.remove('border-danger');
        btn.disabled=false;
    }
    function name_alert(force = false) {
        let elem = document.getElementById('form_name');
        elem.classList.remove('border-danger');
        btn.disabled=false;
    }
    function title_alert(force = false) {
        let elem = document.getElementById('form_title');
        elem.classList.remove('border-danger');
        btn.disabled=false;
    }
    function email_alert(force = false) {
        let elem = document.getElementById('form_email');
        elem.classList.remove('border-danger');
        btn.disabled=false;
    }
});
