from django import forms


class contact_us_form(forms.Form):
    name = forms.CharField(label="نام ", max_length=50, min_length=3, required=True, widget=(forms.TextInput(attrs={
        'id': "form_name",
        'class': "input-contact your-name",
    })))

    email = forms.EmailField(label="ایمیل ", max_length=120, min_length=6, required=True, widget=(forms.EmailInput(attrs={
        'id': "form_email",
        'class': "input-contact your-email",
    })))

    title = forms.CharField(label="عنوان ", label_suffix='blabla', max_length=120, min_length=2, required=True, widget=(forms.TextInput(attrs={
        'id': "form_title",
        'class': "input-contact your-subject",
    })))
    message = forms.CharField(label="پیام شما ", max_length=1000, min_length=3, required=True, widget=(forms.Textarea(attrs={
        'id': "form_message",
        'class': "textarea-contact your-message",
        'cols': "40",
        'rows': "10",
    })))
