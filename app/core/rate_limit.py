import time
from fastapi import Request, HTTPException, status
from app.core.redis import redis


def get_client_ip(request: Request):
    forwarded_for = request.headers.get('X-Forwarded-For')

    if forwarded_for:
        return forwarded_for.split(',')[0].strip()

    if request.client:
        return request.client.host

    return "unknown"

def rate_limit(scope: str, limit: int, window_seconds: int):
    def dependency(request: Request):
        client_ip = get_client_ip(request)

        current_window = int(time.time() // window_seconds)

        key = f"rate_limit: {scope}:{client_ip}:{current_window}"

        count = redis.incr(key)

        if count == 1:
            redis.expire(key, window_seconds)

        if count > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
                headers={
                    "Retry-After": str(window_seconds)
                }
            )
    return dependency