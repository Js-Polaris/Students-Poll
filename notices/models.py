from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Groups announcements/opportunities into clear sections (e.g. Academic Updates, Events)."""

    name = models.CharField(max_length=100, unique=True)##django string field that maps to a varchar column in the sql db.
    slug = models.SlugField(max_length=120, unique=True, blank=True) # the slug is a URL-friendly version of the category name, automatically generated from the name if not provided.
    description = models.TextField(blank=True)

    class Meta: # the Meta class is used to define metadata for the model, such as ordering and verbose name plural.
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): # the save method is overridden to automatically generate a slug from the name if it is not provided. This ensures that each category has a unique and URL-friendly identifier.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Announcement(models.Model):
    """A campus announcement/news/update/event-style post.

    Expiry is automatic: when `expires_at` passes, the announcement is treated as expired
    (removed from active feeds, available in archive) based on date comparison.
    """

    class ModerationStatus(models.TextChoices): # 
        PENDING = 'pending', 'Pending approval'
        APPROVED = 'approved', 'Active'  # approved and not expired => active
        REJECTED = 'rejected', 'Rejected'

    title = models.CharField(max_length=200)
    ##charfield is used for short strings such as titles 
    content = models.TextField()
    ##textfield is used for longer text such as the content of the announcement
    # the category is a foreign key to the Category model, which allows each announcement to be associated with a specific category.  The related_name='announcements' option allows for reverse querying from the Category model to get all announcements associated with that category.
    category = models.ForeignKey(  
        Category,
        on_delete=models.PROTECT,  #The on_delete=models.PROTECT option ensures that if a category is deleted, any associated announcements will not be deleted, and an error will be raised instead.
        related_name='announcements', # allows reverse querying from Category to get all associated announcements
    ) 
    # the author is a foreign key to the user model defined in the Django settings, allowing each announcement to be associated with a specific user. 
    author = models.ForeignKey(  
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, #The on_delete=models.CASCADE option ensures that if a user is deleted, any associated announcements will also be deleted.
        related_name='announcements',
    )
    published_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    image = models.FileField(upload_to='announcements/', blank=True, null=True) # the blank=True and null=True options allow the image field to be optional, meaning that announcements can be created without an associated image.
    # m
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
