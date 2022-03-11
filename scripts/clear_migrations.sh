echo "마이그레이션 파일을 삭제합니다"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete -exec echo '{}' '+'
find . -path "*/migrations/*.pyc" -delete
