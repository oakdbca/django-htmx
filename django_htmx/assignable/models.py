import logging

from abc import ABC, ABCMeta, abstractmethod

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property

model_type = models.base.ModelBase

logger = logging.getLogger(__name__)


class AbstractModelMeta(ABCMeta, model_type):
    pass


class AssignableModel(models.Model, metaclass=AbstractModelMeta):
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(class)s_assignments",
    )

    class Meta:
        abstract = True

    def assign(self, user: User):
        if user is not None and not self.user_is_assignable(user):
            raise ValueError(f"{user} is not assignable to {self}")
        self.assigned_to = user
        self.save()

    def unassign(self):
        self.assigned_to = None
        self.save()

    def user_is_assignable(self, user: User) -> bool:
        return self.assignable_users().filter(pk=user.pk, is_active=True).exists()

    @abstractmethod
    def assignable_users(self) -> models.QuerySet[User]:
        """Models implementing this class must define
        a function that returns a queryset of users that are assignable to the model."""

        raise NotImplementedError("Must implement method assignable_users")


class Task(AssignableModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def assignable_users(self) -> models.QuerySet[User]:
        return User.objects.filter(is_active=True)

    def __str__(self):
        return self.title

    @cached_property
    def content_type(self):
        return ContentType.objects.get_for_model(self).id

    class Meta:
        ordering = ["title"]
