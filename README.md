# MODELFORM
### 1. 폴더 생성 및 파일 설치
```bash
- python -m venv venv
- source venv/Scripts/activate
- pip install django
```
- .gitignore 파일 생성
- gitignore.io 붙여넣기
```bash
- git init
- django-admin startproject modelForm . # 프로젝트 생성
- django-admin startapp articles # 앱 생성
```
- modelForm > settings.py 안에 INSTALLED_APPS에 `articles` 추가
```bash
python manage.py runserver
```

### 2. 공통 base.html 설정
- 최상단에 templates 만들고 안에 base.html 만들고 기본 구조 잡아주기
```html
<body>
    <h1>여기는 base 입니다.</h1>
    {% block body %}
    {% endblock %}
</body>
```
- 이렇게 만들어준 최상단 `templates` 를 장고가 인식하게 만들기위해 `modelFom > settings.py`들어가기
- 55번줄 TEMPLATES 코드 중 `'DIRS': [],` 대괄호 안에 코드 추가하여 `'DIRS': [BASE_DIR / 'templates'],` 설정

### 3. 모델링 추가
- 데이터베이스에 데이터 저장하기 위해 구조잡으러 가기
(어제 만든 코드에 크리에이트 하고 아무것도 안적고 저장하면 빈 값이 저장됨
이게 데이터 베이스에 빈칸이 들어가는 것 이기에 좋은 행동은 아님.
빈값을 검사하는 유효성 검사를 하는 단계를 만들기.)
- articles > models.py 에 Article(models.Model) class 모델링 추가
```python
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = mpdels.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 4. 마이그레이션
- 서버 실행 종료(ctrl + c)
- 파이썬 코드로 작성한 위 모델링을 sql 번역본 만들기 위한 코드
python manage.py makemigrations
- sql 번역본 적용하기
python manage.py migrate

### 5. admin에 Article 추가
- 데이터 생성을 위한 admin.py에 모델 등록
- `articles` > `admin.py` 에 등록
```python
from .models import Article

admin.site.register(Article)
```

### 6. superuser
- 관리하기 위한 슈퍼유저 생성
```bash
python manage.py createsuperuser
```
- 아이디: admin, 비번:
> 데이터 베이스에 비밀번호는 암호화 되어 저장됨.(비밀번호 1234로 했지만 읽을 수 없음.)