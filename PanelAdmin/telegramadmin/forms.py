from django import forms
from .models import Analysis, Currency, TimeFrame

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ["title", "text", "file", "date", "ordering", "state"]
       
        labels = {
            "title" : "عنوان",
            "text" : "متن تحلیل",
            "file" : "فایل پیوست",
            "date" : "تاریخ",
            "ordering": "اولویت",
            "state": "وضعیت"
        }
        widgets = {
            "title" : forms.TextInput(attrs={"class": "form-control", "placeholder" : "عنوان"}),
            "text" : forms.Textarea(attrs={"class": "form-control", "placeholder": "متن....."}),
            "file" : forms.FileInput(attrs={"class": "form-control"}),
            "date": AdminJalaliDateWidget(attrs= {"class": "form-control", "placeholder": "انتخاب تاریخ"}),
            "ordering" : forms.NumberInput(attrs={"class": "form-control", "placeholder": "ترتیب"}),
            "state": forms.RadioSelect(choices=[(1, "فعال"), (0, "غیرفعال")])
        }
    # def clean(self):
    #     cleaned_data  = super().clean()
    #     jalali = cleaned_data.get("jalali_date")
    #     if jalali:
    #         cleaned_data["date"] = jalali.strftime("%Y/%m/%d")
    #         return cleaned_data

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ["title", "state"]
       
        labels = {
            "title" : "عنوان ارز",
            "state": "وضعیت"
        }
        widgets = {
            "title" : forms.TextInput(attrs={"class": "form-control", "placeholder" : "عنوان"}),
            "state": forms.RadioSelect(choices=[(1, "فعال"), (0, "غیرفعال")])
        }
       
class TimeFrameForm(forms.ModelForm):
    class Meta:
        model = TimeFrame
        fields = ["title", "state"]
       
        labels = {
            "title" : "عنوان",
            "state": "وضعیت"
        }
        widgets = {
            "title" : forms.TextInput(attrs={"class": "form-control", "placeholder" : "عنوان"}),
            "state": forms.RadioSelect(choices=[(1, "فعال"), (0, "غیرفعال")])
        }
                