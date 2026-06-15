from fastapi import APIRouter

from app.schemas.loyalty import Voucher, BirthdayVoucherIssueResult, BirthdayVoucherStatus
from app.services.loyalty_service import LoyaltyService

router = APIRouter()
service = LoyaltyService()


@router.get("", response_model=list[Voucher])
def list_vouchers() -> list[dict]:
    return service.list_vouchers()


@router.get("/birthday/status", response_model=BirthdayVoucherStatus)
def get_birthday_voucher_status() -> dict:
    return service.get_birthday_voucher_status()


@router.post("/birthday/issue", response_model=BirthdayVoucherIssueResult)
def issue_birthday_vouchers() -> dict:
    return service.issue_birthday_vouchers()
