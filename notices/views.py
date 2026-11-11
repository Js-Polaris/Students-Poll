from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Announcement


@login_required #only authenticated users can access the view
def notice_list(request):
    """Home/active feed: approved announcements that are published and not expired."""
    now = timezone.now()
    announcements = Announcement.objects.select_related('category', 'author').filter(
        moderation_status=Announcement.ModerationStatus.APPROVED,
        published_at__lte=now,
        expires_at__gt=now,
    )
    return render(request, 'notices/notice_list.html', {'announcements': announcements}) #gives the published and. Ot expired announcements


@login_required
def archive(request):
    """Archive: expired announcements (still accessible). Publishers can also find their own here."""
    now = timezone.now()
    announcements = Announcement.objects.select_related('category', 'author').filter(
        expires_at__lte=now
    )
    return render(request, 'notices/archive.html', {'announcements': announcements})


@login_required
def notice_detail(request, pk):#identify an announcement based on its primary key from db
    """Detail view. Active items visible to logged-in users; expired items remain accessible
    in archive context and are always viewable by their original publisher/author.
    Pending/rejected items are visible to their author and staff.
    """
    announcement = get_object_or_404(Announcement.objects.select_related('category', 'author'), pk=pk)
    user = request.user
    can_view = False #initial access is denied till proved or authenticated
    if announcement.is_active_item:
        can_view = True
    elif announcement.author_id == user.id or user.is_staff:
        can_view = True
    elif announcement.is_expired and announcement.is_approved:
        # Expired approved announcements remain accessible (archive).
        can_view = True

    if not can_view:
        ##when the user cannot or isn't allowed to view the announcement
        from django.http import Http404
        raise Http404('Announcement not found')

    return render(request, 'notices/notice_detail.html', {'announcement': announcement})


SECTION_TITLES = {
    'campus-news': 'Campus News',
    'announcements': 'Announcements',
    'academic-updates': 'Academic Updates',
    'events-competitions': 'Events & Competitions',
    'campus-opportunities': 'Campus Opportunities',
    'my-posts': 'My Posts',
    'profile': 'Profile',
}


@login_required
def coming_soon(request, section_name):
    """Temporary placeholder page for sections we will build in later stages."""
    title = SECTION_TITLES.get(section_name, section_name.replace('-', ' ').title())
    return render(request, 'notices/coming_soon.html', {'section_name': section_name, 'section_title': title})
