from __future__ import annotations


def leader_container_name(status_payload: list[dict[str, object]]) -> str:
    for item in status_payload:
        endpoint = str(item.get("Endpoint", ""))
        status = item.get("Status", {})
        if not isinstance(status, dict):
            continue
        header = status.get("header", {})
        if not isinstance(header, dict):
            continue
        member_id = header.get("member_id")
        leader_id = status.get("leader")
        if member_id == leader_id and endpoint:
            return endpoint.split("//", 1)[1].split(":", 1)[0]
    raise ValueError("leader endpoint not found in status payload")
