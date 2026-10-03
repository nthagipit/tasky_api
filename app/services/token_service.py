from datetime import  timedelta, datetime, timezone
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token, verify_password, hash_password
from app.core.config import settings
from app.schemas.token_schema import TokenResponseSchema
from sqlalchemy.orm import Session
from fastapi import Response
from app.schemas.base_schema import DataResponse
from app.models.refresh_token_model import RefreshToken
from app.schemas.token_schema import AccessTokenResponseSchema,RefreshTokenSchema


def create_token(user_id: str, role: str):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE)
    access_token = create_access_token(
                            user_id= str(user_id), role= role, expires_delta=access_token_expires
                        )
    refresh_token = create_refresh_token(
                            user_id=str(user_id), expires_delta=refresh_token_expires
                        )
    
    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expires=access_token_expires,
        refresh_token_expires=refresh_token_expires
    )

def refresh_token(data: RefreshTokenSchema, response: Response, db: Session):
    payload = verify_refresh_token(data.refresh_token)

    if not payload:
        return DataResponse.error(
            status_code=401,
            detail="Invalid refresh token",
        )

    # 2. Get user ID
    user_id = payload.get("sub")

    if not user_id:
        response.status_code = 401
        return DataResponse.error(
            status_code=401,
            detail="Invalid refresh token",
        )

    # 3. Get active refresh tokens of this user
    refresh_tokens = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False,
        )
        .all()
    )

    # 4. Find matching token
    matched_token = None

    for stored_token in refresh_tokens:
        if verify_password(
            data.refresh_token,
            stored_token.token_hash,
        ):
            matched_token = stored_token
            break

    if not matched_token:
        response.status_code = 401
        return DataResponse.error(
            status_code=401,
            detail="Invalid refresh token",
        )

    # 5. Check expiration
    now = datetime.now(timezone.utc)

    if matched_token.expires_at <= now:
        response.status_code = 401
        return DataResponse.error(
            status_code=401,
            detail="Refresh token has expired",
        )

    # 6. Revoke old token
    matched_token.is_revoked = True

    # 7. Create new tokens
    user = matched_token.user

    token = create_token(
        user.id,
        user.role,
    )

    # 8. Store new refresh token
    new_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=hash_password(
            token.refresh_token
        ),
        expires_at=(
            now + token.refresh_token_expires
        ),
    )

    db.add(new_refresh_token)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    data_response = AccessTokenResponseSchema(
        access_token = token.access_token
    )

    return DataResponse.custom_response(
        "200",
        data=data_response,
        message="Token refreshed successfully",
    )