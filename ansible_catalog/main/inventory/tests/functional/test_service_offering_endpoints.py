""" Module to test ServiceOffering end points """
import json
import pytest
from ansible_catalog.main.inventory.tests.factories import (
    InventoryServicePlanFactory,
    ServiceOfferingFactory,
)


@pytest.mark.django_db
def test_service_offering_list(api_request):
    """Test to list ServiceOffering endpoint"""

    ServiceOfferingFactory()
    response = api_request("get", "serviceoffering-list")

    assert response.status_code == 200
    content = json.loads(response.content)

    assert content["count"] == 1


@pytest.mark.django_db
def test_service_offering_retrieve(api_request):
    """Test to retrieve ServiceOffering endpoint"""

    service_offering = ServiceOfferingFactory()
    response = api_request(
        "get", "serviceoffering-detail", service_offering.id
    )

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content["id"] == service_offering.id


@pytest.mark.django_db
def test_service_offering_patch_not_supported(api_request):
    """Test to patch ServiceOffering endpoint"""

    service_offering = ServiceOfferingFactory()
    response = api_request(
        "patch",
        "serviceoffering-detail",
        service_offering.id,
        {"name": "update"},
    )

    assert response.status_code == 405


@pytest.mark.django_db
def test_service_offering_delete_not_supported(api_request):
    """Test to delete ServiceOffering endpoint"""

    service_offering = ServiceOfferingFactory()
    response = api_request(
        "delete", "serviceoffering-detail", service_offering.id
    )

    assert response.status_code == 405


@pytest.mark.django_db
def test_service_offering_put_not_supported(api_request):
    """Test to put ServiceOffering endpoint"""

    service_offering = ServiceOfferingFactory()
    response = api_request(
        "put",
        "serviceoffering-detail",
        service_offering.id,
        {"name": "update"},
    )

    assert response.status_code == 405


@pytest.mark.django_db
def test_service_offering_service_plan_list(api_request):
    """Test to list ServicePlans by a certain ServiceOffering endpoint"""

    service_offering1 = ServiceOfferingFactory()
    service_offering2 = ServiceOfferingFactory()

    InventoryServicePlanFactory(service_offering=service_offering1)
    InventoryServicePlanFactory(service_offering=service_offering1)
    InventoryServicePlanFactory(service_offering=service_offering2)

    response = api_request(
        "get", "offering-service_plans-list", service_offering1.id
    )

    assert response.status_code == 200
    content = json.loads(response.content)

    assert content["count"] == 2
