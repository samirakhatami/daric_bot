from .models import BotMember, FrameMember, AnalysisMember

def dashboard_callback(request, context):
    
    context['bot_count'] = BotMember.objects.count()
    context['frame_count'] = FrameMember.objects.count()
    context['analysis_count'] = AnalysisMember.objects.count()
    return context
