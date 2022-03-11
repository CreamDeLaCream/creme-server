import os
import uuid

import nanoid


def get_uuid_path(instance, filename: str) -> str:
    """
    파일이름 앞 uuid를 추가한다.
    """
    uuid4 = uuid.uuid4()
    new_path = os.path.join("upload/", f"{uuid4}_{filename}")
    return new_path


def generate_nanoid(
    size: int = 8,
    alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_",
):
    """
    랜덤 문자열 생성
    """
    return nanoid.generate(alphabet, size)
