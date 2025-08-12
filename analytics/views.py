from django.shortcuts import render

# Create your views here.

from django.db.models import Sum, Avg, Count
from django.http import JsonResponse
from django.utils import timezone
from .models import User, Video, WatchSession
from django.db.models import Count, Sum, Avg
from django.http import JsonResponse


def user_dashboard_template(request):
    return render(request, "analytics/user_dashboard.html")

def video_dashboard_template(request):
    return render(request, "analytics/video_dashboard.html")


def user_dashboard_data(request):
    data = {
        "total_watch_time": WatchSession.objects.aggregate(total=Sum("session_duration"))["total"] or 0,
        "avg_session_duration": WatchSession.objects.aggregate(avg=Avg("session_duration"))["avg"] or 0,
        "top_genres": list(
            WatchSession.objects.values("video__genre")
            .annotate(total=Sum("session_duration"))
            .order_by("-total")[:5]
        ),
        "top_videos": list(
            WatchSession.objects.values("video__title")
            .annotate(total=Sum("session_duration"))
            .order_by("-total")[:5]
        ),
        "device_usage": list(
            WatchSession.objects.values("device_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
    }
    return JsonResponse(data)


def video_dashboard_data(request):
    data = {
        "total_views": WatchSession.objects.count(),
        "total_watch_time": WatchSession.objects.aggregate(total=Sum("session_duration"))["total"] or 0,
        "avg_watch_duration": WatchSession.objects.aggregate(avg=Avg("session_duration"))["avg"] or 0,
        "rewatch_percentage": round(
            (WatchSession.objects.filter(is_rewatch=True).count() / WatchSession.objects.count() * 100)
            if WatchSession.objects.count() else 0, 2
        ),
        "device_usage": list(
            WatchSession.objects.values("device_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
        "daily_watch_time": list(
            WatchSession.objects.extra(select={"date": "date(start_time)"})
            .values("date")
            .annotate(total=Sum("session_duration"))
            .order_by("date")
        ),
    }
    return JsonResponse(data)


def user_analytics_api(request, user_id):
    qs = WatchSession.objects.filter(user_id=user_id)
    total_watch_time = qs.aggregate(total=Sum('session_duration'))['total'] or 0
    avg_session = qs.aggregate(avg=Avg('session_duration'))['avg'] or 0
    top_genres = qs.values('video__genre').annotate(total=Sum('session_duration')).order_by('-total')[:5]
    top_videos = qs.values('video__title').annotate(views=Count('id')).order_by('-views')[:10]
    device_usage = qs.values('device_type').annotate(count=Count('id'))

    return JsonResponse({
        'total_watch_time': total_watch_time,
        'avg_session_duration': avg_session,
        'top_genres': list(top_genres),
        'top_videos': list(top_videos),
        'device_usage': list(device_usage),
    })
def video_analytics_api(request, video_id):
    qs = WatchSession.objects.filter(video_id=video_id)
    total_views = qs.count()
    avg_watch_time = qs.aggregate(avg=Avg('session_duration'))['avg'] or 0
    rewatch_percentage = (qs.filter(is_rewatch=True).count() / total_views * 100) if total_views > 0 else 0

    return JsonResponse({
        'total_views': total_views,
        'avg_watch_time': avg_watch_time,
        'rewatch_percentage': rewatch_percentage,
    })



def general_dashboard_api(request):
    days = int(request.GET.get('days', 7))
    since = timezone.now() - timezone.timedelta(days=days)
    qs = WatchSession.objects.filter(start_time__gte=since)

    trending_videos = qs.values('video__title').annotate(views=Count('id')).order_by('-views')[:10]
    most_active_users = qs.values('user__name').annotate(sessions=Count('id')).order_by('-sessions')[:10]
    genre_trends = qs.values('video__genre').annotate(count=Count('id')).order_by('-count')

    return JsonResponse({
        'trending_videos': list(trending_videos),
        'most_active_users': list(most_active_users),
        'genre_trends': list(genre_trends),
    })

def general_dashboard_template(request):
    return render(request, "analytics/general_dashboard.html")


