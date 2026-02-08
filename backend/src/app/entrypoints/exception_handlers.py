"""Exception handlers for FastAPI."""

from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.shared.domain.exceptions import InvalidDomainId


def invalid_domain_id_exception_handler(request: Request, exc: Exception) -> Response:
    """Handle invalid domain ID errors."""
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(exc))


def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to the FastAPI app."""
    app.add_exception_handler(InvalidDomainId, invalid_domain_id_exception_handler)
