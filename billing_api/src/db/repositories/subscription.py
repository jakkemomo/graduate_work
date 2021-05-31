from datetime import timedelta
from typing import Optional
from uuid import uuid4

from src.db.models import Subscriptions, SubscriptionState
from tortoise import timezone


class SubscriptionRepository:
    @staticmethod
    async def get(subscription_id: str) -> Subscriptions:
        return await Subscriptions.get_or_none(pk=subscription_id).prefetch_related(
            "product"
        )

    @staticmethod
    async def get_user_subscription(user_id: str) -> Optional[Subscriptions]:
        return await Subscriptions.get_or_none(
            user_id=user_id,
            state__in=[SubscriptionState.ACTIVE, SubscriptionState.PRE_ACTIVE, SubscriptionState.CANCELLED],
        ).prefetch_related("product")

    @staticmethod
    async def create(user_id: str, product_id: str) -> Subscriptions:
        now = timezone.now()
        return await Subscriptions.create(
            id=uuid4(),
            user_id=user_id,
            product_id=product_id,
            state=SubscriptionState.INACTIVE,
            start_date=now,
            end_date=now,
            created=now,
            modified=now,
        )

    @staticmethod
    async def activate(subscription_id: str, period: int):
        await Subscriptions.filter(pk=subscription_id).update(
            state=SubscriptionState.ACTIVE,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=period),
            modified=timezone.now(),
        )

    @staticmethod
    async def deactivate(subscription_id: str):
        await Subscriptions.filter(pk=subscription_id).update(
            state=SubscriptionState.INACTIVE,
            modified=timezone.now(),
        )

    @staticmethod
    async def pre_activate(subscription_id: str):
        await Subscriptions.filter(pk=subscription_id).update(
            state=SubscriptionState.PRE_ACTIVE,
            modified=timezone.now(),
        )

    @staticmethod
    async def to_deactivate(subscription_id: str):
        await Subscriptions.filter(pk=subscription_id).update(
            state=SubscriptionState.TO_DEACTIVATE,
            modified=timezone.now(),
        )

    @staticmethod
    async def cancel(subscription_id: str):
        await Subscriptions.filter(pk=subscription_id).update(
            state=SubscriptionState.CANCELLED,
            modified=timezone.now(),
        )
