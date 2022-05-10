"""Copy portfolio item service"""
import copy
import logging
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from pinakes.main.catalog.models import (
    ServicePlan,
    Portfolio,
    PortfolioItem,
)
from pinakes.main.catalog.services import (
    name,
)
from pinakes.main.catalog.services.copy_image import (
    CopyImage,
)
from pinakes.main.inventory.services.get_service_offering import (
    GetServiceOffering,
)

logger = logging.getLogger("catalog")


class CopyPortfolioItem:
    """Copy portfolio item service"""

    def __init__(self, portfolio_item, options):
        self.portfolio_item = portfolio_item
        self.name = options.get("portfolio_item_name", portfolio_item.name)

        portfolio_id = options.get("portfolio_id", None)
        if portfolio_id:
            self.portfolio = Portfolio.objects.get(id=portfolio_id)
        else:
            self.portfolio = self.portfolio_item.portfolio

        self.new_portfolio_item = None

    def process(self):
        self.make_copy()

        return self

    @transaction.atomic
    def make_copy(self):
        if not self._is_orderable():
            raise RuntimeError(
                _("{} is not orderable, and cannot be copied").format(
                    self.portfolio_item.name
                )
            )

        new_icon = (
            CopyImage(self.portfolio_item.icon).process().new_icon
            if self.portfolio_item.icon
            else None
        )

        self.new_portfolio_item = copy.copy(self.portfolio_item)
        self.new_portfolio_item.id = None
        self.new_portfolio_item.name = self._new_portfolio_item_name()
        self.new_portfolio_item.icon = new_icon
        self.new_portfolio_item.portfolio = self.portfolio
        self.new_portfolio_item.save()

        service_plans = ServicePlan.objects.filter(
            portfolio_item=self.portfolio_item
        )
        for plan in service_plans:
            new_plan = copy.copy(plan)
            new_plan.id = None
            new_plan.portfolio_item = self.new_portfolio_item
            new_plan.save()

    def _is_orderable(self):
        service_offering_ref = self.portfolio_item.service_offering_ref
        if service_offering_ref is None:
            return False

        svc = GetServiceOffering(service_offering_ref, True).process()
        service_offering = svc.service_offering

        if service_offering is None:
            return False

        service_plans = ServicePlan.objects.filter(
            portfolio_item=self.portfolio_item
        )

        changed_plans = [plan for plan in service_plans if plan.outdated]

        if len(changed_plans) > 0:
            logger.info(
                "Survey Changed for Portfolio Item #{@portfolio_item.name}"
            )
            return False

        return True

    def _new_portfolio_item_name(self):
        portfolio_items = PortfolioItem.objects.filter(
            portfolio=self.portfolio
        )
        portfolio_item_names = [
            portfolio_item.name for portfolio_item in portfolio_items
        ]

        return (
            name.create_copy_name(
                self.name,
                portfolio_item_names,
                PortfolioItem.MAX_PORTFOLIO_ITEM_LENGTH,
            )
            if self.name in portfolio_item_names
            else self.name
        )
