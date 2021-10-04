""" Module to test approval requests and actions """
import pytest
import json
from django.urls import reverse
from ansible_catalog.main.tests.factories import default_tenant
from ansible_catalog.main.approval.tests.factories import (
    RequestFactory,
    ActionFactory,
)
from ansible_catalog.main.approval.services.send_event import SendEvent


@pytest.mark.django_db
def test_request_list(api_request):
    RequestFactory()
    RequestFactory()
    url = reverse("request-list")
    response = api_request("get", url)

    assert response.status_code == 200
    content = json.loads(response.content)

    assert content["count"] == 2


@pytest.mark.django_db
def test_request_retrieve(api_request):
    request = RequestFactory()
    url = reverse("request-detail", args=(request.id,))
    response = api_request("get", url)

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content["id"] == request.id


@pytest.mark.django_db
def test_request_child_list(api_request):
    parent = RequestFactory()
    RequestFactory(parent=parent)
    RequestFactory(parent=parent)
    url = reverse("request-request-list", args=(parent.id,))
    response = api_request("get", url)

    assert response.status_code == 200
    content = json.loads(response.content)

    assert content["count"] == 2


@pytest.mark.django_db
def test_request_action_list(api_request):
    request = RequestFactory()
    ActionFactory(request=request, operation="Start")
    ActionFactory(request=request, operation="Complete")
    url = reverse("request-action-list", args=(request.id,))
    response = api_request("get", url)

    assert response.status_code == 200
    content = json.loads(response.content)

    assert content["count"] == 2


@pytest.mark.django_db
def test_create_request(api_request, mocker):
    mocker.patch("django_rq.enqueue")
    default_tenant()
    url = reverse("request-list")
    response = api_request(
        "post",
        url,
        {"name": "abcdef", "description": "abc", "content": {"item1": "val1"}},
    )

    assert response.status_code == 201
    content = json.loads(response.content)
    assert content["state"] == "Pending"


@pytest.mark.django_db
def test_create_request_bad(api_request, mocker):
    mocker.patch("django_rq.enqueue", side_effect=Exception("whoops"))
    default_tenant()
    url = reverse("request-list")
    response = api_request(
        "post",
        url,
        {"name": "abcdef", "description": "abc", "content": {"item1": "val1"}},
    )

    assert response.status_code == 500
    content = json.loads(response.content)
    assert content["detail"] == "Internal Error"


@pytest.mark.django_db
def test_create_action(api_request, mocker):
    mocker.patch.object(SendEvent, "process")
    request = RequestFactory(state="Notified")
    url = reverse("request-action-list", args=(request.id,))
    response = api_request(
        "post",
        url,
        {
            "operation": "Deny",
            "comments": "not good",
            "request": request.id,
        },
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_request_not_supported_methods(api_request):
    request = RequestFactory()
    url = reverse("request-detail", args=(request.id,))

    response = api_request("put", url, {"name": "update"})
    assert response.status_code == 405

    response = api_request("patch", url, {"name": "update"})
    assert response.status_code == 405

    response = api_request("delete", url)
    assert response.status_code == 405


@pytest.mark.django_db
def test_request_request_not_create(api_request):
    request = RequestFactory()
    url = reverse("request-request-list", args=(request.id,))
    response = api_request(
        "post",
        url,
        {
            "name": "child",
            "description": "child request cannot be explicitly created",
            "parent": request.id,
        },
    )

    assert response.status_code == 405


@pytest.mark.django_db
def test_request_full_action(api_request):
    parent = RequestFactory()
    child = RequestFactory(parent=parent)
    parent_action = ActionFactory(request=parent)
    child_action = ActionFactory(request=child)
    url = reverse("request-full", args=(parent.id,))

    response = api_request("get", url)
    content = json.loads(response.content)
    assert response.status_code == 200
    print(content)
    assert content["subrequests"][0]["name"] == child.name
    assert content["subrequests"][0]["id"] == child.id
    assert content["actions"][0]["operation"] == parent_action.operation
    assert content["actions"][0]["id"] == parent_action.id
    assert (
        content["subrequests"][0]["actions"][0]["operation"]
        == child_action.operation
    )
    assert content["subrequests"][0]["actions"][0]["id"] == child_action.id
