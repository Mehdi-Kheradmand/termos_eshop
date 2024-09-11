from django import forms


class ProductCommentsForm(forms.Form):
    msg = forms.CharField(max_length=1000, min_length=10, required=True, widget=forms.Textarea(attrs={
        'id': 'comment-box', 'name': 'comment', 'cols': '45', 'rows': '8', 'aria-required': "True",
    }))
