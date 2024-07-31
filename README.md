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

# 어제는 모델과 폼을 따로 만들었지만 이걸 한번에 관리해주는 것이 modelForm

### 7. Read(All)기능 구현
- `articles` 에 `templates` 만들고 `index.html` 생성
```html
{% extends 'base.html' %}

{% block body %}

    {% for article in articles %}
        <h5>{{article.title}}</h5>
        <p>{{article.content}}</p>
        <p>{{article.created_at}}</p>
        <hr>
    {% endfor %}

{% endblock %}
```
- `articles`에서 들어온 것을 `articles`에 들어있는 `urlse.py` 로 가라고 지정해주기 위해 `articles` 에 `urls.py` 파일 만들기
```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index')
]
```
- `articles/views.py` 함수 생성
```python
from .models import Article # 추가

# Create your views here.
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)
```
- `modelForm/urls.py` path추가하여 `articles` 경로 지정
```python
from django.contrib import admin
# from django.urls import path 아래 코드 추가
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')), # 추가
]
```

##  게시물 생성 create 기능 만들기(어제와 다르게 만들거임)
> 크게 2단계로 나뉘었었음

> 첫번째로 new로 빈 종이를 주는 단계

> 두번째로 create 로 종이를 받고 생성하는 단계

> 하지만 오늘은 두가지 기능을 한단계로 합축

### 8. Create 기능구현
- `artcles` 에 `forms.py` 파일 만들기
- 여기서 `modelForm` 만들거임(new, create를 한번에 만들어주기 위함.)
- `modelForm`은 장고의 `forms`안에 `modelforms` 불러오기
- `ArticleForm`에 어떤 모델을 쓸 것인지 설정하기위해 `class Meta()` 지정
- 최종적으로 `ArticleForm`은 `class Article()` 모델에 맞추어 자동으로 html코드를 만들어줌
```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta():
        model = Article
        fields = '__all__'
```
- `article > views.py `에서 `ArticleForm `불러오고 `create` 함수 수정
```python
from .forms import ArticleForm

def create(request):
    form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)
```
- `articles/urls.py`에 path 추가
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'), # 추가
```
- `articles/templates` 에 `create.html` 만들기
- `create.html` 파일에 {{form}} 설정하면 자동으로 input 코드를 만들어줌. `modelForm`이 만들어 준거임
```html
{% block body %}
<h1>create</h1>
{{form}}
{% endblock %}
```
- 홈페이지가서 개발자툴열어 확인해보면 어제 우리가 쓰지 않은 값이 설정되어있음
- `required`: 필수적인. 데이터를 넣지 않았을때 해주는 유효성 검사 설정.
- 근데 장고의 `modelform` 은 `input` 만 만들어 주고 `form `은 만들어 주지 않음. 우리가 따로 설정해줘야함
```html
{% block body %}
<h1>create</h1>
<form action="">
    {{form}}
    <input type="submit">
</form>
{% endblock %}
```
- 근데 `required`는 최소한의 검증만 해줌. 프론트에서 검증하는 거임
그래서 서버에서 저장할때도 검증이 필요함.
- `formeh` 수정할거임
```html
<form action="" method="POST">
    {% csrf_token %}
```
- `action` 지정.
- 어디로 가야하지? 어제는 현재 new에서 create경로로 보냈음
- 오늘은 현재 위치가 `create`임. 어디로 보낼까? 다시` create` 로 보낼거임
- 지금 `action`값은 빈값임. 빈 `action`은 현재 내 주소로 다시 요청을 보냄
```html
{% extends 'base.html' %}

{% block body %}
<h1>create</h1>
<form action="" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
{% endblock %}
```
- `article/views.py` 에서`redirect`랑 `ArticleForm` 불러오고 `create` 함수 수정
- 어제는 new라는 경로 지정
- 오늘은 `GET` 과 `POST`로 지정하여 구분
- 어제 한거랑 별 다를거 없지만, `urls` 지정만 달라지는 거임
- 그래서 `create` 함수에 `if` 문으로 `post`로 들어왔는지 `GET`문으로 들어왔는지 구분
- `create` 누르면 `GET` 방식임(어제 new 방식),
버튼을 누르든 url 검색하여 들어가든 다 `GET` 방식
`GET`이 기본값.
- 제출버튼을 누르면 `POST` 방식임(어제 `creat` 방식).
`POST` 방식은 우리가 만든 식.
- `articles > urls > views.py > create > if`문에서 코드 실행
```python
from django.shortcuts import render, redirect # redirect추가
from .forms import ArticleForm

# new/ > 빈 종이를 보여주는 기능
# create/ > 사용자가 입력한 데이터를 저장

# GET create/ > 빈 종이를 보여주는 기능
# POST create/ > 사용자가 입력한 데이터를 저장

def create(request):

    # 모든 경우의수
    # - GET : form을 만들어서 html 문서를 사용자에게 리턴
    #   => 1~4번
    # - POST invalid data (데이터 검증에 실패한 경우)
    #   => 5~9번
    # - POST valid data (데이터 검증에 성공한 경우)
    #   => 10~14번

    # 5. POST 요청 (데이터가 잘 못 들어온 경우)
    # 10. POST 요청 (데이터가 잘 들어온 경우)
    if request.method == 'POST':
        # 6. 사용자가 입력한데이터X(request.POST)를 담아서 form을 생성
        # 11. 사용자가 입력한데이터O(request.POST)를 담아서 form을 새성
        form = ArticleForm(request.POST)

        # 7. form을 검증(실패)
        # 12. form을 검증(성공)
        if form.is_valid():
            # 13. form을 저장
            form.save()
            # 14. index페이지로 redirect
            return redirect('articles:index')

    # 1. GET 요청
    else:
        # 2. 비어있는 form을 만들어서
        form = ArticleForm()

    # 3. context dict에 비어있는 form을 담아서
    # 8. context dict에 검증에 실패한 form을 담아서
    context = {
        'form': form,
    }

    # 4. create.html을 랜더링
    # 9. create.html을 랜더링
    return render(request, 'create.html', context)
```
- `templates/base.html` 에 코드 수정하여 버튼 추가
```html
</head>
<body>
    <h1>여기는 base입니다.</h1>
    <a href="{% url 'articles:create' %}">create</a> <!-- 추가 -->
    {% block body %}
    {% endblock %}
</body>
```

### 9. Delete 기능구현
- `articles/templates/index.html` 수정
```html
<h5>{{article.title}}</h5>
        <p>{{article.content}}</p>
        <p>{{article.created_at}}</p>
        <!-- 아래 코드 추가 -->
        {% comment %}
        <a href="{% url 'articles:delete' id=article.id %}">delete</a>
        {% endcomment %}

        <form action="{% url 'articles:delete' id=article.id %}" method="POST">
            {% csrf_token %}
            <input type="submit" value="delete">
        </form>
        <!-- 위까지 추가 -->
        <hr>
    {% endfor %}
```
- `articles/urls.py` path 추가
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    # 추가
    path('<int:id>/delete/', views.delete, name='delete'),
]
```
- `articles/views.py` 함수 추가
```python
def delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()

    return redirect('articles:index')
```

### 10. update 기능구현
- `articles/templates/index.html` 수정
```html
            <input type="submit" value="delete">
        </form>
        <!-- 아래 추가 -->
        <a href="{% url 'articles:update' id=article.id %}">update</a>

        <hr>
    {% endfor %}
```
- `articles/templates`에 `update.html` 파일 만들기
```html
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>
{% endblock %}
```
- `articles/urls.py` path 추가
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:id>/delete/', views.delete, name='delete'),
    # 추가
    path('<int:id>/update/', views.update, name='update'),
]
```
- `articles/views.py` 함수 추가
```python
def update(request, id):
    article = Article.objects.get(id=id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        # article = Article.objects.get(id=id)
        form = ArticleForm(instance=article)

    context = {
        'form': form,
    }

    return render(request, 'update.html', context)
```

### 11. form.html 코드 통합
- `update`
    1. 기존에 정보 보여주기
    2. 수정된 정보 보여주기
- `update`와 `create`를 같은 `.html` 파일로 관리하기
- `articles/templates/create.html` 파일 이름을 `articles/templates/form.html`로 변경 후 코드 수정
```html
{% extends 'base.html' %}

{% block body %}
<!-- <h1>create</h1> 제거 -->

<!-- 아래 코드 추가 -->
{% if request.resolver_match.url_name == 'create' %}
    <h1>create</h1>
{% else %}
    <h1>update</h1>
{% endif %}
<!-- 위 코드까지 -->

<form action="" method="POST">
    {% csrf_token %}
    {{form}}
```
- `articles/templates/update.html` 파일 삭제
- `articles/views.py` 중 `create`함수와 `update`함수 코드 이름 변경
```python
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    # return render(request, 'create.html', context)
    return render(request, 'form.html', context)

...

def update(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        # article = Article.objects.get(id=id)
        form = ArticleForm(instance=article)
        
    context = {
        'form': form,
    }

    # return render(request, 'update.html', context)
    return render(request, 'form.html', context)
```