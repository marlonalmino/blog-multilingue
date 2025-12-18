from django.conf import settings
from django.db import models
from django.db.models import Q
from blog.models import Post


class CommentStatus(models.TextChoices):
    PENDING = "pending", "pending"
    APPROVED = "approved", "approved"
    REJECTED = "rejected", "rejected"
    FLAGGED = "flagged", "flagged"
    SPAM = "spam", "spam"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    body = models.TextField()
    status = models.CharField(max_length=20, choices=CommentStatus.choices, default=CommentStatus.PENDING)
    spam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["post", "status", "created_at"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self):
        return f"Comment {self.pk}"


class ModerationAction(models.TextChoices):
    APPROVE = "approve", "approve"
    REJECT = "reject", "reject"
    FLAG = "flag", "flag"
    UNFLAG = "unflag", "unflag"


class CommentModeration(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="moderations")
    action = models.CharField(max_length=20, choices=ModerationAction.choices)
    reason = models.CharField(max_length=500, blank=True)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_moderations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["comment"]),
            models.Index(fields=["performed_by"]),
            models.Index(fields=["created_at"]),
        ]


class ReactionType(models.TextChoices):
    LIKE = "like", "like"
    CLAP = "clap", "clap"
    LOVE = "love", "love"


class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="post_reactions")
    type = models.CharField(max_length=20, choices=ReactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user", "type"], name="unique_post_user_reaction", condition=Q(user__isnull=False)),
        ]
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["type"]),
        ]


class CommentReaction(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="comment_reactions")
    type = models.CharField(max_length=20, choices=ReactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["comment", "user", "type"], name="unique_comment_user_reaction", condition=Q(user__isnull=False)),
        ]
        indexes = [
            models.Index(fields=["comment"]),
            models.Index(fields=["type"]),
        ]


# Create your models here.
