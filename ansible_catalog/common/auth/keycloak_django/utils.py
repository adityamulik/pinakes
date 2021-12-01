from typing import Protocol, Sequence


class GroupProto(Protocol):
    id: str
    path: str


class KeycloakResourceProto(Protocol):
    keycloak_id: str

    def keycloak_type(self) -> str:
        ...

    def keycloak_actions(self) -> Sequence[str]:
        ...


def make_permission_name(obj: KeycloakResourceProto, group: GroupProto):
    return "group_{resource_type}_{resource_id}_{group_id}".format(
        resource_type=obj.keycloak_type(),
        resource_id=obj.keycloak_id,
        group_id=group.id,
    )


def make_scope(
    obj: KeycloakResourceProto, action: str, *, validate: bool = True
):
    type_ = obj.keycloak_type()
    if validate and action not in obj.keycloak_actions():
        raise ValueError(f"Invalid action '{action}' for resource '{type_}'.")
    return f"{type_}:{action}"


def parse_scope(obj: KeycloakResourceProto, scope: str):
    prefix = obj.keycloak_type() + ":"
    if scope.startswith(prefix):
        return scope[len(prefix) :]
    else:
        raise ValueError("Unexpected scope. Must begin with '{prefix}'.")
