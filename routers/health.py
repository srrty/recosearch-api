from fastapi import APIRouter

router = APIRouter()

@router.get("", summary="헬스 체크 엔드포인트")
def health_check():
    """서비스의 정상 가동 여부를 간단히 확인합니다."""
    return {"status": "ok"}