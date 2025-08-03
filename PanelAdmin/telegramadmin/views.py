from django.shortcuts import render
from jalali_date import datetime2jalali, date2jalali

import os
from django.http import FileResponse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from .models import Analysis
from .forms import AnalysisForm



def my_view(request):
	jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

def safe_download(request, file_path):
	file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
	if os.path.exists(file_full_path):
		return FileResponse(open(file_full_path, 'rb'), as_attachment=True)
	else:
		messages.error(request, "فایل مورد نظر یافت نشد.")
		return redirect(request.META.get("HTTP_REFERER", "/"))
