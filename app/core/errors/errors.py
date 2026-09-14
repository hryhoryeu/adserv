from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.errors.enums import ErrorEnum


class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    status = ErrorEnum.INTERNAL


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    status = ErrorEnum.NOT_FOUND


class CampaignNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    status = ErrorEnum.CAMPAIGN_NOT_FOUND


async def exception_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, content={"messge": f"hello from {exc.status}"}
    )
