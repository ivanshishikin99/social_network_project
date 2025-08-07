from datetime import datetime, timezone, timedelta

import jwt

from core.config import settings


def encode_jwt(
        payload: dict,
        expire_minutes: int,
        algorithm: str = settings.jwt_config.algorithm,
        private_key: str = settings.jwt_config.private_key_path.read_text(encoding="UTF-8"),
        ):
    to_encode = payload.copy()
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(minutes=expire_minutes)
    to_encode.update(iat=now, exp=exp)
    return jwt.encode(payload=to_encode,
                      key=private_key,
                      algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        algorithm: str = settings.jwt_config.algorithm,
        public_key: str = settings.jwt_config.public_key_path.read_text(encoding="UTF-8"),
        ):
    return jwt.decode(jwt=token,
                      key=public_key,
                      algorithms=[algorithm])