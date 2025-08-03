from unfold.contrib.dashboard import Dashboard, Card
from django.utils.translation import gettext_lazy as _
from telegramadmin.models import TimeFrame, Bot, AnalysisMember

class CustomDashboard(Dashboard):
    def get_items(self, request):
        return [
            Card(title=_("بات ممبر"), value=Bot.objects.count()),
            Card(title=_("فریم تایم ممبر"), value=TimeFrame.objects.count()),
            Card(title=_("آنالیز ممبر"), value=AnalysisMember.objects.count()),
        ]

dashboard = CustomDashboard()