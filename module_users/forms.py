from django import forms
from django.contrib.auth.models import User

from termos_eshop.Utilities import is_it_email, is_it_phone_number, is_it_first_or_last_name, is_it_numeric, \
    is_it_password_with_nums_and_letters

# ---------------------------------------------------------------------------------------------------------------------


class EmailPhoneForm(forms.Form):
    my_default_errors = {
        'required': 'خطا: ایمیل یا شماره همراه وارد نشده',
        'invalid': 'خطا: مقدار ایمیل یا شماره همراه درست نیست'
    }

    input_email_phone = forms.CharField(max_length=50, label="شماره همراه یا ایمیل خود را وارد کنید :", min_length=10, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'ایمیل یا شماره همراه',
        'name': "email_phone",
    }), error_messages=my_default_errors)

    def clean_input_email_phone(self):
        ep = self.cleaned_data.get('input_email_phone')
        if is_it_phone_number(ep) or is_it_email(ep):
            return ep
        raise forms.ValidationError("فرمت ایمیل یا شماره همراه درست نیست! (فرمت صحیح شماره همراه : ۱۱ رقمی و شروع با ۰۹)")


# ---------------------------------------------------------------------------------------------------------------------


class Form_Password(forms.Form):
    my_default_errors = {
        'required': 'خطا: مقدار گذرواژه وارد نشده',
        'invalid': 'خطا: مقدار گذرواژه درست نیست',
        'min_length': "طول گذرواژه باید حداقل ۸ کاراکتر باشد"
    }

    input_password = forms.CharField(max_length=50, label="گذرواژه خودرا وارد کنید :", min_length=8, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'گذرواژه',
        'name': "input_password",
    }), error_messages=my_default_errors)

    input_hidden_email = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_input_password(self):
        password = self.cleaned_data.get('input_password')
        if len(str(password)) < 8 or len(str(password)) > 50:
            raise forms.ValidationError("خطا: مقدار گذرواژه باید حداقل ۸ و حداکثر ۵۰ کاراکتر باشد")
        return password

# ---------------------------------------------------------------------------------------------------------------------


class FormOTP(forms.Form):
    my_default_errors = {
        'required': 'خطا: کد تایید وارد نشده',
        'invalid': 'خطا: کد تایید درست نیست',
        'min_length': "خطا: کد تایید درست نیست",
        'max_length': "خطا: کد تایید درست نیست",
    }

    input_otp = forms.CharField(max_length=6, label="کد تایید پیامک شده را وارد کنید :", min_length=6, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'کد تایید ۶ رقمی',
        'name': "input_otp",
    }), error_messages=my_default_errors)

    input_hidden_phone = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_input_otp(self):
        password = self.cleaned_data.get('input_otp')
        if len(str(password)) != 6 or not is_it_numeric(password):
            raise forms.ValidationError("خطا: کد تایید درست نیست")
        return password


# ---------------------------------------------------------------------------------------------------------------------


class Form_UserRegister(forms.Form):
    my_default_errors = {
        'required': 'خطا: پر کردن فیلد های ستاره‌دار الزامی هستند',
        'invalid': 'خطا: مقادیر وارد شده درست نیست. لطفا مجددا بررسی کنید',
        'min_length': "خطا: مقادیر وارد شده کوتاه تر از حد مجاز است",
        'max_length': "خطا: مقادیر وارد شده طولانی تر از حد مجاز است",
    }
    input_hidden_hash_code = forms.CharField(required=True, widget=forms.HiddenInput())

    input_phone_number = forms.CharField(max_length=11, min_length=11, required=False, disabled=True, widget=forms.TextInput(attrs={
        'name': "input_phone_number",
    }), error_messages=my_default_errors, label='شماره همراه (ضروری)* :')

    input_first_name = forms.CharField(max_length=20, min_length=3, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'نام (فقط حروف فارسی)',
        'name': "input_first_name",
    }), error_messages=my_default_errors, label="نام (ضروری)* :")

    input_last_name = forms.CharField(max_length=20, min_length=3, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'نام خانوادگی (فقط حروف فارسی)',
        'name': "input_last_name",
    }), error_messages=my_default_errors, label="نام خانوادگی (ضروری)* :")

    input_email = forms.CharField(max_length=250, min_length=3, required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'آدرس ایمیل',
        'name': "input_email",
    }), error_messages=my_default_errors, label='آدرس ایمیل (اختیاری) :')

    input_password = forms.CharField(max_length=120, min_length=8, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'گذرواژه',
        'name': "input_password",
    }), error_messages=my_default_errors, label='گذرواژه (ضروری)* :')

    def clean_phone_number(self):
        ep = self.cleaned_data.get('input_phone_number')
        if not is_it_phone_number(ep):
            raise forms.ValidationError("شماره همراه درست نیست!")
        return ep

    def clean_first_name(self):
        x = self.cleaned_data.get('input_first_name')
        if not (is_it_first_or_last_name(x) and (len(x) > 2) and len(x) < 21):
            raise forms.ValidationError("نام درست نیست! (حداقل ۲ حرف و حداکثر ۲۰ حرف  و فقط حروف فارسی)")
        return x

    def clean_last_name(self):
        x = self.cleaned_data.get('input_last_name')
        if not (is_it_first_or_last_name(x) and (len(x) > 2) and len(x) < 21):
            raise forms.ValidationError("نام خانوادگی درست نیست! (حداقل ۲ حرف و حداکثر ۲۰ حرف  و فقط حروف فارسی)")
        return x

    def clean_input_email(self):
        received_email = self.cleaned_data.get('input_email')

        if received_email and received_email != '':
            if not (is_it_email(received_email) and (len(received_email) > 9) and len(received_email) < 50):
                raise forms.ValidationError("ایمیل درست نیست! (یک ایمیل صحیح وارد کنید و یا مقدار ایمیل را خالی بگذارید)")
            else:
                if User.objects.filter(email=received_email).count() == 0:
                    return received_email
                else:
                    raise forms.ValidationError("خطا : حساب کاربری با این ایمیل قبلا ساخته شده")
        else:
            return received_email
    #  -p---------------------------

    def clean_input_password(self):
        received_pass = self.cleaned_data.get('input_password')
        if not is_it_password_with_nums_and_letters(received_pass):
            raise forms.ValidationError("گذرواژه درست نیست! ( حداقل ۸ کاراکتر شامل حروف و اعداد )")
        return received_pass
