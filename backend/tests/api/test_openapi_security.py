from fastapi.routing import APIRoute

from app.main import app
from app.presentation.api.v1 import reproduction_router


PUBLIC_OPERATIONS = {
    ("GET", "/"),
    ("GET", "/test-db"),
    ("POST", "/auth/signup/send-code"),
    ("POST", "/auth/signup/verify-code"),
    ("POST", "/auth/signup/send-phone-code"),
    ("POST", "/auth/signup/verify-phone-code"),
    ("POST", "/auth/signup/register"),
    ("POST", "/auth/login"),
    ("POST", "/auth/refresh"),
    ("POST", "/auth/forgot-password"),
    ("POST", "/auth/reset-password"),
    ("POST", "/auth/login/google"),
    ("POST", "/auth/register/google"),
}


def test_openapi_has_no_duplicate_method_path_operations():
    operation_ids = [
        operation["operationId"]
        for path_item in app.openapi()["paths"].values()
        for operation in path_item.values()
    ]
    assert len(operation_ids) == len(set(operation_ids))


def test_every_non_public_operation_declares_bearer_authentication():
    schema = app.openapi()
    missing_security: list[tuple[str, str]] = []

    for path, path_item in schema["paths"].items():
        for method, operation in path_item.items():
            operation_key = (method.upper(), path)
            if operation_key in PUBLIC_OPERATIONS:
                continue
            if not operation.get("security"):
                missing_security.append(operation_key)

    assert missing_security == []


def test_static_reproduction_catalog_routes_precede_dynamic_record_route():
    get_paths = [
        route.path
        for route in reproduction_router.router.routes
        if isinstance(route, APIRoute) and "GET" in route.methods
    ]

    dynamic_index = get_paths.index("/reproductions/{reproduction_id}")
    assert get_paths.index("/reproductions/protocols") < dynamic_index
    assert get_paths.index("/reproductions/protocols/{protocol_id}") < dynamic_index
    assert (
        get_paths.index("/reproductions/protocols/{protocol_id}/steps")
        < dynamic_index
    )
