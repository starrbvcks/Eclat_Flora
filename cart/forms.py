from django import forms

# ایجاد یک لیست از ۱ تا ۲۰ برای منوی کشویی انتخاب تعداد گل
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label='تعداد'
    )
    # این فیلد مخفی است تا سیستم بداند باید تعداد را اضافه کند یا جایگزین (Override) کند
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)