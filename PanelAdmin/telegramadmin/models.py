from django.db import models

# Create your models here.

 # This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Abilities(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci')
    title = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    entity_id = models.PositiveBigIntegerField(blank=True, null=True)
    entity_type = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    only_owned = models.IntegerField()
    options = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    scope = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'abilities'


class ActivityLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    log_name = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment='نام')
    description = models.TextField(db_collation='utf8mb4_unicode_ci', db_comment='توضیحات')
    subject_id = models.PositiveBigIntegerField(blank=True, null=True, db_comment='کد رکورد تغییریافته')
    subject_type = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment='مدل رکورد تغییریافته')
    causer_id = models.PositiveBigIntegerField(blank=True, null=True, db_comment='کد کاربر فاعل')
    causer_type = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment='مدل کاربر فاعل')
    system_ip = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', db_comment='IP کاربر')
    properties = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True, db_comment='تغییرات')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True, db_comment='تاریخ حذف منطقی')
    state = models.IntegerField(db_comment='وضعیت')

    class Meta:
        managed = False
        db_table = 'activity_log'


class AdminInterfaceTheme(models.Model):
    name = models.CharField(unique=True, max_length=50)
    active = models.IntegerField()
    title = models.CharField(max_length=50)
    title_visible = models.IntegerField()
    logo = models.CharField(max_length=100)
    logo_visible = models.IntegerField()
    css_header_background_color = models.CharField(max_length=10)
    title_color = models.CharField(max_length=10)
    css_header_text_color = models.CharField(max_length=10)
    css_header_link_color = models.CharField(max_length=10)
    css_header_link_hover_color = models.CharField(max_length=10)
    css_module_background_color = models.CharField(max_length=10)
    css_module_text_color = models.CharField(max_length=10)
    css_module_link_color = models.CharField(max_length=10)
    css_module_link_hover_color = models.CharField(max_length=10)
    css_module_rounded_corners = models.IntegerField()
    css_generic_link_color = models.CharField(max_length=10)
    css_generic_link_hover_color = models.CharField(max_length=10)
    css_save_button_background_color = models.CharField(max_length=10)
    css_save_button_background_hover_color = models.CharField(max_length=10)
    css_save_button_text_color = models.CharField(max_length=10)
    css_delete_button_background_color = models.CharField(max_length=10)
    css_delete_button_background_hover_color = models.CharField(max_length=10)
    css_delete_button_text_color = models.CharField(max_length=10)
    list_filter_dropdown = models.IntegerField()
    related_modal_active = models.IntegerField()
    related_modal_background_color = models.CharField(max_length=10)
    related_modal_rounded_corners = models.IntegerField()
    logo_color = models.CharField(max_length=10)
    recent_actions_visible = models.IntegerField()
    favicon = models.CharField(max_length=100)
    related_modal_background_opacity = models.CharField(max_length=5)
    env_name = models.CharField(max_length=50)
    env_visible_in_header = models.IntegerField()
    env_color = models.CharField(max_length=10)
    env_visible_in_favicon = models.IntegerField()
    related_modal_close_button_visible = models.IntegerField()
    language_chooser_active = models.IntegerField()
    language_chooser_display = models.CharField(max_length=10)
    list_filter_sticky = models.IntegerField()
    form_pagination_sticky = models.IntegerField()
    form_submit_sticky = models.IntegerField()
    css_module_background_selected_color = models.CharField(max_length=10)
    css_module_link_selected_color = models.CharField(max_length=10)
    logo_max_height = models.PositiveSmallIntegerField()
    logo_max_width = models.PositiveSmallIntegerField()
    foldable_apps = models.IntegerField()
    language_chooser_control = models.CharField(max_length=20)
    list_filter_highlight = models.IntegerField()
    list_filter_removal_links = models.IntegerField()
    show_fieldsets_as_tabs = models.IntegerField()
    show_inlines_as_tabs = models.IntegerField()
    css_generic_link_active_color = models.CharField(max_length=10)
    collapsible_stacked_inlines = models.IntegerField()
    collapsible_stacked_inlines_collapsed = models.IntegerField()
    collapsible_tabular_inlines = models.IntegerField()
    collapsible_tabular_inlines_collapsed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_interface_theme'


class Analysis(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(db_collation='utf8mb4_persian_ci')
    text = models.CharField(max_length=2000, db_collation='utf8mb4_persian_ci')
    file = models.CharField(max_length=250, blank=True, null=True)
    date = models.CharField(max_length=10)
    ordering = models.IntegerField(verbose_name="اولویت")
    state = models.IntegerField( verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'analysis'
        verbose_name = "آنالیز"
        verbose_name_plural = "آنالیزها"

    def __str__(self):
        return self.title 


class AnalysisMember(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.CharField(max_length=50)
    send_analysis = models.IntegerField(verbose_name="وضعیت")
    created_at = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'analysis_member'
        verbose_name = "کاربران آنالیز"
        verbose_name_plural = "کاربران آنالیز"
    def __str__(self):
        return f"کاربر: {self.chat_id}"


class AssignedRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    entity_id = models.PositiveBigIntegerField()
    entity_type = models.CharField(max_length=255)
    restricted_to_id = models.PositiveBigIntegerField(blank=True, null=True)
    restricted_to_type = models.CharField(max_length=255, blank=True, null=True)
    scope = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assigned_roles'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, blank=True, null=True, db_comment='نام کاربری')
    token = models.CharField(max_length=200, blank=True, null=True)
    group_link = models.CharField(max_length=200, blank=True, null=True)
    channel_link = models.CharField(max_length=200, blank=True, null=True)
    state = models.IntegerField(verbose_name="وضعیت")
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'bot'
        db_table_comment = 'اعضای ربات'
        verbose_name = "بات"
        verbose_name_plural = "ربات ها "
    def __str__(self):
        return f"{self.username}" 


class BotMember(models.Model):
    id = models.AutoField(primary_key=True)
    bot_id = models.IntegerField(db_comment='نام ربات', verbose_name="آیدی ربات")
    chat_id = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True, db_comment='نام کاربری')
    mobile = models.CharField(max_length=15, blank=True, null=True, db_comment='موبایل')
    privilege = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    invite_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(blank=True, null=True,auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'bot_member'
        db_table_comment = 'اعضای ربات'
        verbose_name = "اعضای ربات"
        verbose_name_plural = "اعضای ربات"
    def __str__(self):
        return self.name

class Currency(models.Model):
    title = models.CharField(max_length=50, db_collation='utf8mb4_persian_ci')
    state = models.IntegerField(verbose_name="وضعیت")
    created_at = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'currency'
        verbose_name = "ارز"
        verbose_name_plural ="ارزها"
    def __str__(self):
        return self.title 


class Customers(models.Model):
    personnel_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    family = models.CharField(max_length=50, blank=True, null=True)
    national_code = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    tel = models.CharField(max_length=11, blank=True, null=True)
    wallet = models.CharField(max_length=50, blank=True, null=True)
    img = models.CharField(max_length=250, blank=True, null=True)
    score = models.CharField(max_length=5, blank=True, null=True)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    register_personnel_id = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FormBuilderField(models.Model):
    bot_id = models.IntegerField()
    title = models.TextField(db_comment='عنوان ')
    type = models.IntegerField(db_comment='نوع ')
    select_value = models.TextField(blank=True, null=True, db_comment='مقادیر انتخابی')
    after_enter = models.TextField(blank=True, null=True, db_comment='پیغام بعد از وارد کردن')
    ordering = models.IntegerField(db_comment='ترتیب')
    state = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'form_builder_field'


class FormBuilderFieldMember(models.Model):
    bot_id = models.IntegerField()
    chat_id = models.CharField(max_length=20, db_comment='شخص')
    field_id = models.IntegerField(db_comment='فیلد')
    value = models.TextField(db_comment='مقدار')
    username = models.CharField(max_length=100, blank=True, null=True, db_comment='نام کاربری')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_builder_field_member'


class FormBuilderMessage(models.Model):
    bot_id = models.IntegerField()
    field_id = models.IntegerField()
    chat_id = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'form_builder_message'


class FormBuilderSetting(models.Model):
    bot_id = models.IntegerField()
    first_msg = models.TextField(db_comment='پیام ابتدائی')
    end_msg = models.TextField(db_comment='پیام انتهائی')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'form_builder_setting'


class FrameMember(models.Model):
    id = models.AutoField(primary_key=True)
    time_frame_id = models.IntegerField(blank=True, null=True, verbose_name="آیدی زمان‌ها")
    chat_id = models.CharField(max_length=50)
    currency_id = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'frame_member'
        verbose_name = "زمان کاربران"
        verbose_name_plural ="زمان های کاربران"
    def __str__(self):
        return f"کاربر: {self.chat_id}"


class Menus(models.Model):
    subsystem = models.ForeignKey('Subsystems', models.DO_NOTHING, db_comment='زیرسیستم')
    menu = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, db_comment='منوی والد')
    title = models.TextField(db_collation='utf8mb4_bin', db_comment='عنوان')
    icon_class = models.CharField(max_length=30, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment='آیکن')
    route = models.CharField(max_length=70, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment='لینک')
    ordering = models.IntegerField(db_comment='ترتیب نمایش')
    open_in_blank = models.IntegerField(db_comment='نمایش در تب جدید')
    open_in_iframe = models.IntegerField(db_comment='نمایش در iFrame')
    description = models.CharField(max_length=255, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment='توضیحات')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(db_comment='وضعیت')

    class Meta:
        managed = False
        db_table = 'menus'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Notifications(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    type = models.CharField(max_length=255)
    notifiable_type = models.CharField(max_length=255)
    notifiable_id = models.PositiveBigIntegerField()
    data = models.TextField()
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    ability = models.ForeignKey(Abilities, models.DO_NOTHING)
    entity_id = models.PositiveBigIntegerField(blank=True, null=True)
    entity_type = models.CharField(max_length=255, blank=True, null=True)
    forbidden = models.IntegerField()
    scope = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_access_tokens'


class Personnels(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    town_id = models.IntegerField(blank=True, null=True)
    cooperation_id = models.IntegerField()
    personnel_num = models.CharField(max_length=40, blank=True, null=True)
    national_code = models.CharField(max_length=12, blank=True, null=True)
    certificate_number = models.CharField(max_length=10, blank=True, null=True)
    father_name = models.CharField(max_length=40, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    registrar_id = models.IntegerField(blank=True, null=True)
    personnel_img = models.IntegerField(blank=True, null=True)
    employment_kind_id = models.SmallIntegerField(blank=True, null=True)
    office_post_id = models.SmallIntegerField(blank=True, null=True)
    place_code = models.IntegerField(blank=True, null=True)
    job_id = models.IntegerField(blank=True, null=True)
    state = models.IntegerField()
    job_rank_id = models.IntegerField(blank=True, null=True)
    job_type_id = models.IntegerField(blank=True, null=True)
    department_id = models.IntegerField(blank=True, null=True)
    work_range = models.IntegerField(blank=True, null=True)
    user_in = models.IntegerField(blank=True, null=True)
    post_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personnels'


class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    level = models.PositiveIntegerField(blank=True, null=True)
    scope = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'
        unique_together = (('name', 'scope'),)


class SmsirLogs(models.Model):
    from_field = models.CharField(db_column='from', max_length=100, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    to = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    response = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'smsir_logs'


class Subsystems(models.Model):
    title = models.TextField(db_collation='utf8mb4_bin', db_comment='عنوان')
    route = models.CharField(max_length=70, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment=' لینک مستقیم')
    icon_class = models.CharField(max_length=30, db_collation='utf8mb4_unicode_ci', blank=True, null=True, db_comment='آیکن')
    header_title = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True, db_comment='عنوان نمایشی در هدر صفحه')
    ordering = models.IntegerField(db_comment='ترتیب نمایش')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(db_comment='وضعیت')

    class Meta:
        managed = False
        db_table = 'subsystems'


class TimeFrame(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, db_collation='utf8mb4_persian_ci')
    state = models.IntegerField(verbose_name="وضعیت")
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'time_frame'
        verbose_name = "بازه‌ی زمانی"
        verbose_name_plural = "بازه های زمانی"
    def __str__(self):
        return self.title
        


class UserVerifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    ip = models.CharField(max_length=45)
    user_agent = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255)
    attempts = models.IntegerField()
    reason = models.CharField(max_length=14)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_verifications'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    personnel_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=20, blank=True, null=True)
    registrator_id = models.IntegerField(blank=True, null=True)
    accounttype_id = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    master = models.IntegerField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    google_id = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'  

