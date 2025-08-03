from django.contrib import admin
from .models import Bot, BotMember, Currency, TimeFrame, FrameMember, Analysis, AnalysisMember
from .forms import AnalysisForm, CurrencyForm, TimeFrameForm
from django.utils import timezone
from django.utils.html import format_html
import os
from django.conf import settings
from .signals import send_analysis_to_users
from django.contrib.admin.sites import AdminSite
from django.db.models import Count
from django.urls import path
from django.template.response import TemplateResponse
import jdatetime

def jalali_dateTime(Time):
    shamsi_datetime = jdatetime.datetime.fromgregorian(datetime=Time).strftime("%Y/%m/%d-%H:%M")
    return shamsi_datetime

class StatusFilter(admin.SimpleListFilter):
    title = 'وضعیت'
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return [
            ('1', 'فعال'),
            ('0', 'غیرفعال'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(state=1)
        if self.value() == '0':
            return queryset.filter(state=0)
        return queryset
    

# Register your models here.
botusername = ""
@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    fieldsets = (
        ("ثبت جدید" , {
            "fields" : ("username", "token"),
        }),
    )
    list_per_page = 20

    def get_list_display(self, request):
        return ("row_number", "username_fa", "state_fa", "created_at_fa")

    def changelist_view(self, request, extra_context=None):
        self.request = request  # ذخیره درخواست برای row_number
        response = super().changelist_view(request, extra_context)
        try:
            self.queryset = response.context_data['cl'].result_list
        except (AttributeError, KeyError):
            self.queryset = []
        return response

    def row_number(self, obj):
        try:
            page_number = int(self.request.GET.get('p', 0))
        except (AttributeError, ValueError):
            page_number = 0
        try:
            index = list(self.queryset).index(obj)
        except (ValueError, AttributeError):
            index = -1
        if index >= 0:
            return format_html('<div style="text-align: right;">{}</div>',page_number * self.list_per_page + index + 1)
        else:
            return '-'
    row_number.short_description = 'ردیف'

    def username_fa(self, obj):
        botusername = obj.username
        return format_html('<div style="text-align: right;">{}</div>',obj.username)
    username_fa.short_description = "یوزرنیم"

    def state_fa(self, obj):
        if obj.state == 1 :
            return format_html('<div style = "color: green; text-align: right; direction: rtl">فعال</div>')
        else:
            return format_html('<div style = "color: red; text-align: right; direction: rtl">غیرفعال</div>')
    state_fa.short_description = "وضعیت"

    def created_at_fa(self, obj):
        if obj.created_at:
            return format_html('<div style="text-align: right;">{}</div>',jalali_dateTime(obj.created_at))
        return ''
    created_at_fa.short_description = "تاریخ ایجاد"

    # برای مرتب سازی پیش‌فرض جدول
    ordering = ['id']

    list_display = ["row_number", "username_fa", "state_fa", "created_at_fa"]
    list_display_links = ["row_number", "username_fa", "state_fa", "created_at_fa"]
    list_filter = [StatusFilter, "created_at"]
    search_fields = ["id", "username",]
    def has_add_permission(self, request):
        return False
    
    
    
@admin.register(BotMember)
class BotMemberAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_list_display(self, request):
        return ("row_number", "name_fa", "bot_id_fa", "chat_id_fa", "mobile_fa", "created_at_fa")

    def changelist_view(self, request, extra_context=None):
        self.request = request  # ذخیره درخواست برای row_number
        response = super().changelist_view(request, extra_context)
        try:
            self.queryset = response.context_data['cl'].result_list
        except (AttributeError, KeyError):
            self.queryset = []
        return response

    def row_number(self, obj):
        try:
            page_number = int(self.request.GET.get('p', 0))
        except (AttributeError, ValueError):
            page_number = 0
        try:
            index = list(self.queryset).index(obj)
        except (ValueError, AttributeError):
            index = -1
        if index >= 0:
            return format_html('<div style="text-align: right;">{}</div>',page_number * self.list_per_page + index + 1)
        else:
            return '-'
    row_number.short_description = 'ردیف'

    def name_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.name)
    name_fa.short_description = "نام"

    def bot_id_fa(self, obj):
        bot = Bot.objects.get(id = obj.bot_id)
        return format_html('<div style="text-align: right;">{}</div>',bot.username)
    bot_id_fa.short_description = "ربات یوزرنیم"

    def chat_id_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.chat_id)
    chat_id_fa.short_description = "چت آیدی"

    def mobile_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.mobile)
    mobile_fa.short_description = "شماره موبایل"

    def created_at_fa(self, obj):
        if obj.created_at:
            return format_html('<div style="text-align: right;">{}</div>',jalali_dateTime(obj.created_at))
        return ''
    created_at_fa.short_description = "تاریخ ایجاد"

    # برای مرتب سازی پیش‌فرض جدول
    ordering = ['id']

    list_display = ["row_number", "name_fa", "bot_id_fa", "chat_id_fa", "mobile_fa", "created_at_fa"]
    list_display_links = ["row_number", "name_fa", "bot_id_fa", "chat_id_fa", "mobile_fa", "created_at_fa"]
    list_filter = ("created_at", "bot_id",)
    search_fields = ["name", "chat_id",]
    ordering = ["id"]
    def has_add_permission(self, request):
        return False



@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    
    fieldsets = (
        ("ثبت ارز جدید" , {
            "fields" : (("title", "state"),),
        }),
    )
    form = CurrencyForm
    list_display = ["title_fa", "state_fa", "created_at_fa"]
    list_display_links = ["title_fa", "state_fa", "created_at_fa"]

    def title_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.title)
    title_fa.short_description = "عنوان"
    def state_fa(self, obj):
        if obj.state == 1 :
            return format_html('<div style = "color: green; text-align: right; direction: rtl">فعال</div>')
        else:
            return format_html('<div style = "color: red; text-align: right; direction: rtl">غیرفعال</div>')
        
    state_fa.short_description = "وضعیت"

    def created_at_fa(self, obj):
        if obj.created_at:
            return format_html('<div style="text-align: right;">{}</div>',jalali_dateTime(obj.created_at))
        return ''
    created_at_fa.short_description = "تاریخ ایجاد"
    
    list_filter = [StatusFilter, "created_at"]
    search_fields = ["title"]
    

@admin.register(TimeFrame)
class TimeFrameAdmin(admin.ModelAdmin):
    fieldsets = (
        ("ثبت جدید" , {
            "fields" : (("title", "state"),),
        }),
    )
    form = TimeFrameForm

    list_per_page = 20

    def get_list_display(self, request):
        return ("row_number", "title_fa", "state_fa", "created_at_fa")

    def changelist_view(self, request, extra_context=None):
        self.request = request  # ذخیره درخواست برای row_number
        response = super().changelist_view(request, extra_context)
        try:
            self.queryset = response.context_data['cl'].result_list
        except (AttributeError, KeyError):
            self.queryset = []
        return response

    def row_number(self, obj):
        try:
            page_number = int(self.request.GET.get('p', 0))
        except (AttributeError, ValueError):
            page_number = 0
        try:
            index = list(self.queryset).index(obj)
        except (ValueError, AttributeError):
            index = -1
        if index >= 0:
            return format_html('<div style="text-align: right;">{}</div>',page_number * self.list_per_page + index + 1)
        else:
            return '-'
    row_number.short_description = 'ردیف'
    def title_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.title)
    title_fa.short_description = "عنوان"

    def state_fa(self, obj):
        if obj.state == 1 :
            return format_html('<div style = "color: green; text-align: right; direction: rtl">فعال</div>')
        else:
            return format_html('<div style = "color: red; text-align: right; direction: rtl">غیرفعال</div>')
    state_fa.short_description = "وضعیت"

    def created_at_fa(self, obj):
        if obj.created_at:
            return format_html('<div style="text-align: right;">{}</div>',jalali_dateTime(obj.created_at))
        return ''
    created_at_fa.short_description = "تاریخ ایجاد"

    # برای مرتب سازی پیش‌فرض جدول
    ordering = ['id']

    list_display = ["row_number", "title_fa", "state_fa", "created_at_fa"]
    list_display_links = ["row_number", "title_fa", "state_fa", "created_at_fa"]
    list_filter = [StatusFilter, "created_at"]
    search_fields = ["id", "title"]
    ordering = ["id"]

@admin.register(FrameMember)
class FrameMemberAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_list_display(self, request):
        return ("row_number", "chat_id_fa", "time_frame_id_fa", "currency_id_fa", "created_at_fa")

    def changelist_view(self, request, extra_context=None):
        self.request = request  # ذخیره درخواست برای row_number
        response = super().changelist_view(request, extra_context)
        try:
            self.queryset = response.context_data['cl'].result_list
        except (AttributeError, KeyError):
            self.queryset = []
        return response

    def row_number(self, obj):
        try:
            page_number = int(self.request.GET.get('p', 0))
        except (AttributeError, ValueError):
            page_number = 0
        try:
            index = list(self.queryset).index(obj)
        except (ValueError, AttributeError):
            index = -1
        if index >= 0:
            return format_html('<div style="text-align: right;">{}</div>',page_number * self.list_per_page + index + 1)
        else:
            return '-'
    row_number.short_description = 'ردیف'
    def chat_id_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.chat_id)
    chat_id_fa.short_description = "چت آیدی"

    def time_frame_id_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.time_frame_id)
    time_frame_id_fa.short_description = "آیدی زمانی مشخص شده"

    def currency_id_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.currency_id)
    currency_id_fa.short_description = "آیدی ارز های مشخص شده"

    def created_at_fa(self, obj):
        if obj.created_at:
            return format_html('<div style="text-align: right;">{}</div>',jalali_dateTime(obj.created_at))
        return ''
    created_at_fa.short_description = "تاریخ ایجاد"

    # برای مرتب سازی پیش‌فرض جدول
    ordering = ['id']


    list_display = ["row_number", "chat_id_fa", "time_frame_id_fa", "currency_id_fa", "created_at_fa"]
    list_display_links = ["row_number", "chat_id_fa", "time_frame_id_fa", "currency_id_fa", "created_at_fa"]
    list_filter = ["time_frame_id", "created_at"]
    search_fields = ["chat_id"]
    ordering = ["id"]
    def has_add_permission(self, request):
        return False

    




@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_list_display(self, request):
        return ("row_number", "title_fa", "file_fa", "ordering_fa", "state_fa", "created_at_fa")

    def changelist_view(self, request, extra_context=None):
        self.request = request  # ذخیره درخواست برای row_number
        response = super().changelist_view(request, extra_context)
        try:
            self.queryset = response.context_data['cl'].result_list
        except (AttributeError, KeyError):
            self.queryset = []
        return response

    def row_number(self, obj):
        try:
            page_number = int(self.request.GET.get('p', 0))
        except (AttributeError, ValueError):
            page_number = 0
        try:
            index = list(self.queryset).index(obj)
        except (ValueError, AttributeError):
            index = -1
        if index >= 0:
            return format_html('<div style="text-align: right;">{}</div>',page_number * self.list_per_page + index + 1)
        else:
            return '-'
    row_number.short_description = 'ردیف'

    def title_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.title)
    title_fa.short_description = "عنوان"

    def file_fa(self, obj):
        from django.urls import reverse
        if not obj.file:
            return format_html('<div style="text-align: right;">None</div>')
        # file_url =settings.MEDIA_URL + obj.file
        file_path = str(obj.file)
        file_name = os.path .basename(file_path).split("?")[0]
        file_ext = os.path.splitext(file_name)[-1].lower()
        download_url = reverse('safe_download', args=[file_path])

        
        if file_ext in [".jpg", ".png"]:
            return format_html('<a href="{}" target="_blank" style="text-align: right; direction: rtl;">{}</a>', download_url, file_name)
        elif file_ext == ".pdf":
            return format_html('<a href= "{}" target="_blank" style="text-align: right; direction: rtl;">{}</a>', download_url, file_name)
        




        # return format_html('<div style="text-align: right;">{}</div>',obj.file)
    file_fa.short_description = "فایل"

    def ordering_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.ordering)
    ordering_fa.short_description = "ترتیب"

    def state_fa(self, obj):
        if obj.state == 1 :
            return format_html('<div style = "color: green; text-align: right; direction: rtl">فعال</div>')
        else:
            return format_html('<div style = "color: red; text-align: right; direction: rtl">غیرفعال</div>')
    state_fa.short_description = "وضعیت"

    def created_at_fa(self, obj):
        if obj.created_at:
            return format_html('<div style="text-align: right;">{}</div>',jalali_dateTime(obj.created_at))
        return ''
    created_at_fa.short_description = "تاریخ ایجاد"

    # برای مرتب سازی پیش‌فرض جدول
    ordering = ['id']

    # جستجو روی فیلدهای واقعی مدل باشه نه row_number
    search_fields = ["title", "id"]
    list_display_links = ["row_number", "title_fa"]
    list_filter = [StatusFilter, "ordering", "created_at"]

    fieldsets = (
        (None, {
            "fields": (("title", "text"),),
        }),
        ("تاریخ و فایل", {
            "fields": (("file", "date"),),
        }),
        ("ترتیب و وضعیت", {
            "fields": (("ordering", "state"),)
        }),
    )

    form = AnalysisForm

    def save_model(self, request, obj, form, change):
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            filename = f'{timezone.now().strftime("%Y%m%d%H%M%S")}_{uploaded_file.name}'
            save_path = os.path.join('uploads/analysis/', filename)
            full_path = os.path.join(settings.MEDIA_ROOT, save_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            obj.file = save_path
        super().save_model(request, obj, form, change)

@admin.register(AnalysisMember)
class AnalysismemberAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_list_display(self, request):
        return ("row_number", "chat_id_fa", "send_analysis_fa", "created_at_fa")

    def changelist_view(self, request, extra_context=None):
        self.request = request  # ذخیره درخواست برای row_number
        response = super().changelist_view(request, extra_context)
        try:
            self.queryset = response.context_data['cl'].result_list
        except (AttributeError, KeyError):
            self.queryset = []
        return response

    def row_number(self, obj):
        try:
            page_number = int(self.request.GET.get('p', 0))
        except (AttributeError, ValueError):
            page_number = 0
        try:
            index = list(self.queryset).index(obj)
        except (ValueError, AttributeError):
            index = -1
        if index >= 0:
            return format_html('<div style="text-align: right;">{}</div>',page_number * self.list_per_page + index + 1)
        else:
            return '-'
    row_number.short_description = 'ردیف'
    def chat_id_fa(self, obj):
        return format_html('<div style="text-align: right;">{}</div>',obj.chat_id)
    chat_id_fa.short_description = "چت آیدی"

    def send_analysis_fa(self, obj):
        if obj.send_analysis == 1 :
            return format_html('<div style = "color: green; text-align: right; direction: rtl">فعال</div>')
        else:
            return format_html('<div style = "color: red; text-align: right; direction: rtl">غیرفعال</div>')
    send_analysis_fa.short_description = "وضعیت"

    def created_at_fa(self, obj):
        if obj.created_at:
            return format_html('<div style="text-align: right;">{}</div>', jalali_dateTime(obj.created_at))
        return ''
    created_at_fa.short_description = "تاریخ ایجاد"

    # برای مرتب سازی پیش‌فرض جدول
    ordering = ['id']
    
    list_display = ["row_number", "chat_id_fa", "send_analysis_fa", "created_at_fa"]
    list_display_links = ["row_number", "chat_id_fa", "send_analysis_fa", "created_at_fa"]
    list_filter = ["send_analysis", "created_at"]
    search_fields = ["chat_id"]
    ordering = ["id"]
    def has_add_permission(self, request):
        return False
    