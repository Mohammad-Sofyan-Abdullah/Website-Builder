import logging
from fastapi import HTTPException, Header, Request
from services.supabase_client import get_client

logger = logging.getLogger(__name__)


def require_auth(request: Request, authorization: str = Header(...)):
    try:
        token = authorization.removeprefix("Bearer ").strip()
        client = get_client()
        response = client.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        user = response.user
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            logger.info("user=%s method=%s path=%s", user.id, request.method, request.url.path)
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
