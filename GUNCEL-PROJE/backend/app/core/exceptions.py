"""Ozel istisnalar."""

from fastapi import HTTPException, status


def not_found(resource: str, identifier: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} bulunamadi: {identifier}",
    )
