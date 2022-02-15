from typing import List

from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

# Must be imported that way to avoid circular imports
from .infraction import Infraction


class FilterListType(models.IntegerChoices):
    """Choice between allow or deny for a list type."""

    ALLOW = 1
    DENY = 0


# Valid special values in ping related fields
VALID_PINGS = ("everyone", "here", "moderators", "onduty", "admins")
VALID_BYPASS_ROLES = ("staff",)


def validate_ping_field(value_list: List[str]) -> None:
    """Validate that the values are either a special value or a UID."""
    for value in value_list:
        # Check if it is a special value
        if value in VALID_PINGS:
            continue
        # Check if it is a UID
        if value.isnumeric():
            continue

        raise ValidationError(f"{value!r} isn't a valid ping type.")


def validate_bypass_roles_field(value_list: List[str]) -> None:
    """Validate that the vclues are either a special value or a Role ID."""
    for value in value_list:
        if value.isnumeric() or value in VALID_BYPASS_ROLES:
            continue
        raise ValidationError(f"{value!r} isn't a valid (bypass) role.")


class FilterSettingsMixin(models.Model):
    """Mixin for common settings of a filters and filter lists."""

    dm_content = models.CharField(
        max_length=1000,
        null=True,
        help_text="The DM to send to a user triggering this filter."
    )
    dm_embed = models.CharField(
        max_length=2000,
        help_text="The content of the DM embed",
        null=True
    )
    infraction_type = models.CharField(
        choices=Infraction.TYPE_CHOICES,
        max_length=9,
        null=True,
        help_text="The infraction to apply to this user."
    )
    infraction_reason = models.CharField(
        max_length=1000,
        help_text="The reason to give for the infraction."
    )
    infraction_duration = models.DurationField(
        null=True,
        help_text="The duration of the infraction. Null if permanent."
    )

    class Meta:
        """Metaclass for settings mixin."""

        abstract = True


class FilterList(FilterSettingsMixin):
    """Represent a list in its allow or deny form."""

    name = models.CharField(max_length=50, help_text="The unique name of this list.")
    list_type = models.IntegerField(
        choices=FilterListType.choices,
        help_text="Whether this list is an allowlist or denylist"
    )
    ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers.",
        null=False
    )
    filter_dm = models.BooleanField(help_text="Whether DMs should be filtered.", null=False)
    dm_ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers on a DM.",
        null=False
    )
    delete_messages = models.BooleanField(
        help_text="Whether this filter should delete messages triggering it.",
        null=False
    )
    bypass_roles = ArrayField(
        models.CharField(max_length=100),
        help_text="Roles and users who can bypass this filter.",
        validators=(validate_bypass_roles_field,),
        null=False
    )
    enabled = models.BooleanField(
        help_text="Whether this filter is currently enabled.",
        null=False
    )
    send_alert = models.BooleanField(
        help_text="Whether alert should be sent.",
        null=False,
        default=True
    )
    # Where a filter should apply.
    #
    # The resolution is done in the following order:
    #   - enabled_channels
    #   - disabled_categories
    #   - disabled_channels
    enabled_channels = ArrayField(models.IntegerField())
    disabled_channels = ArrayField(models.IntegerField())
    disabled_categories = ArrayField(models.IntegerField())

    class Meta:
        """Constrain name and list_type unique."""

        constraints = (
            UniqueConstraint(fields=("name", "list_type"), name="unique_name_type"),
        )

    def __str__(self) -> str:
        return f"Filter {FilterListType(self.list_type).label}list {self.name!r}"


class Filter(FilterSettingsMixin):
    """One specific trigger of a list."""

    content = models.CharField(max_length=100, help_text="The definition of this filter.")
    description = models.CharField(max_length=200, help_text="Why this filter has been added.")
    additional_field = JSONField(null=True, help_text="Implementation specific field.")
    filter_list = models.ForeignKey(
        FilterList, models.CASCADE, related_name="filters",
        help_text="The filter list containing this filter."
    )
    ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers.",
        null=True
    )
    filter_dm = models.BooleanField(help_text="Whether DMs should be filtered.", null=True)
    dm_ping_type = ArrayField(
        models.CharField(max_length=20),
        validators=(validate_ping_field,),
        help_text="Who to ping when this filter triggers on a DM.",
        null=True
    )
    delete_messages = models.BooleanField(
        help_text="Whether this filter should delete messages triggering it.",
        null=True
    )
    bypass_roles = ArrayField(
        models.CharField(max_length=100),
        help_text="Roles and users who can bypass this filter.",
        validators=(validate_bypass_roles_field,),
        null=True
    )
    enabled = models.BooleanField(
        help_text="Whether this filter is currently enabled.",
        null=True
    )
    send_alert = models.BooleanField(
        help_text="Whether alert should be sent.",
        null=True
    )

    # Check FilterList model for information about these properties.
    enabled_channels = ArrayField(models.IntegerField(), null=True)
    disabled_channels = ArrayField(models.IntegerField(), null=True)
    disabled_categories = ArrayField(models.IntegerField(), null=True)

    def __str__(self) -> str:
        return f"Filter {self.content!r}"