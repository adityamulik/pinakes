from rest_framework import routers

from rest_framework_extensions.routers import NestedRouterMixin

from ansible_catalog.main.catalog.views import (
    ApprovalRequestViewSet,
    CatalogServicePlanViewSet,
    OrderViewSet,
    OrderItemViewSet,
    PortfolioViewSet,
    PortfolioItemViewSet,
    ProgressMessageViewSet,
    TenantViewSet,
)

urls_views = {}


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass


router = NestedDefaultRouter()

router.register("tenants", TenantViewSet)
portfolios = router.register(
    r"portfolios", PortfolioViewSet, basename="portfolio"
)
portfolios.register(
    r"portfolio_items",
    PortfolioItemViewSet,
    basename="portfolio-portfolioitem",
    parents_query_lookups=["portfolio"],
)
portfolio_items = router.register(
    r"portfolio_items", PortfolioItemViewSet, basename="portfolioitem"
)
urls_views["portfolio-portfolioitem-detail"] = None  # disable
urls_views["portfolio-portfolioitem-icon"] = None
urls_views["portfolio-portfolioitem-tag"] = None
urls_views["portfolio-portfolioitem-tags"] = None
urls_views["portfolio-portfolioitem-untag"] = None
urls_views["portfolio-portfolioitem-list"] = PortfolioItemViewSet.as_view(
    {"get": "list"}
)  # read only

portfolio_items.register(
    r"service_plans",
    CatalogServicePlanViewSet,
    basename="portfolioitem-serviceplan",
    parents_query_lookups=["portfolio_item"],
)

urls_views["portfolioitem-serviceplan-detail"] = None  # disable
urls_views["portfolioitem-serviceplan-base"] = None  # disable
urls_views["portfolioitem-serviceplan-modified"] = None  # disable
urls_views["portfolioitem-serviceplan-reset"] = None  # disable

orders = router.register(r"orders", OrderViewSet, basename="order")
orders.register(
    r"order_items",
    OrderItemViewSet,
    basename="order-orderitem",
    parents_query_lookups=["order"],
)
orders.register(
    r"approval_request",
    ApprovalRequestViewSet,
    basename="order-approvalrequest",
    parents_query_lookups=["order"],
)
orders.register(
    r"progress_messages",
    ProgressMessageViewSet,
    basename="order-progressmessage",
    parents_query_lookups=["messageable_id"],
)
urls_views["order-orderitem-detail"] = OrderItemViewSet.as_view(
    {"get": "retrieve"}
)  # read only
urls_views["order-approvalrequest-detail"] = None
urls_views["order-progressmessage-detail"] = None

order_items = router.register(
    r"order_items", OrderItemViewSet, basename="orderitem"
)
order_items.register(
    r"progress_messages",
    ProgressMessageViewSet,
    basename="orderitem-progressmessage",
    parents_query_lookups=["messageable_id"],
)
urls_views["orderitem-list"] = None
urls_views["orderitem-progressmessage-detail"] = None