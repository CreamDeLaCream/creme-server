import os
import pathlib
import shutil
from glob import glob
from typing import List

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "미리 정의된 기본 데이터를 추가합니다."

    def handle(self, *args, **options):

        # fixture 디렉터리 경로
        fixture_directory = os.path.join(settings.BASE_DIR, "data")

        # fixtrue 디렉터리가 존재하는지 체크
        if not os.path.isdir(fixture_directory):
            raise FileNotFoundError(f"{fixture_directory} 디렉터리가 존재하지 않습니다.")

        # image_files = glob(f"{fixture_directory}/images/*")
        # self.__copy_files(image_files, os.path.join(settings.MEDIA_ROOT, "upload"))

        # json 파일만 가져온다
        files = glob(f"{fixture_directory}/*.json")
        for file in sorted(files):
            print(file)
            management.call_command("loaddata", file)

    def __copy_files(self, files: List[str], dest: str) -> None:

        # 디렉터리가 존재하지 않는 다면 생성해준다
        if not os.path.isdir(dest):
            pathlib.Path(dest).mkdir(parents=True, exist_ok=True)

        for file_path in files:
            shutil.copy(file_path, dest)
