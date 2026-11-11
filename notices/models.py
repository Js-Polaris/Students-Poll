from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Groups announcements/opportunities into clear sections (e.g. Academic Updates, Events)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Announcement(models.Model):
    """A campus announcement/news/update/event-style post.

    Expiry is automatic: when `expires_at` passes, the announcement is treated as expired
    (removed from active feeds, available in archive) based on date comparison.
    """

    class ModerationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending approval'
        APPROVED = 'approved', 'Active'  # approved and not expired => active
        REJECTED = 'rejected', 'Rejected'

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='announcements',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements',
    )
    published_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    # Using FileField for now so migrations can run without Pillow installed.
    # Can be changed to ImageField later (requires Pillow) when image validation/processing is needed.
    image = models.FileField(upload_to='announcements/', blank=True, null=True)
    moderation_status = models.CharField(
        max_length=20,
        choices=ModerationStatus.choices,
        default=ModerationStatus.PENDING,
        help_text='Pending posts require approval before appearing as active (once not expired).',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_pending_approval(self):
        return self.moderation_status == self.ModerationStatus.PENDING

    @property
    def is_approved(self):
        return self.moderation_status == self.ModerationStatus.APPROVED

    @property
    def is_rejected(self):
        return self.moderation_status == self.ModerationStatus.REJECTED

    @property
    def is_active_item(self):
        """Active feed item: approved, published, and not expired."""
        return self.is_approved and (not self.is_expired) and self.published_at <= timezone.now()

    @property
    def display_status(self):
        """Human-friendly status: active, expired, or pending approval (and rejected)."""
        if self.is_expired:
            return 'Expired'
        if self.is_pending_approval:
            return 'Pending approval'
        if self.is_rejected:
            return 'Rejected'
        if self.is_active_item:
            return 'Active'
        # Approved but not yet published
        return 'Scheduled'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.expires_at and self.published_at and self.expires_at < self.published_at:
            raise ValidationError({'expires_at': 'Expiry date/time cannot be earlier than the publication date/time.'})


# Keep the old Notice model temporarily for reference/migration safety if needed.
# (No longer used by views/templates in Stage 3.)
class Notice(models.Model):
    """Legacy campus notice/news item (replaced by Announcement in Stage 3)."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text='Date and time after which this notice is considered late.')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_late(self):
        return timezone.now() > self.expires_at

    @property
    def status(self):
        return 'Late' if self.is_late else 'Current'
