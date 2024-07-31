from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)




# new/ > 빈 종이를 보여주는 기능
# create/ > 사용자가 입력한 데이터를 저장

# GET create/ > 빈 종이를 보여주는 기능
# POST create/ > 사용자가 입력한 데이터를 저장
def create(request):
    # - GET: form을 만들어서 html 문서를 사용자에게 리턴 -> 1~4번
    # - POST invalid data(데이터 검증에 실패한 경우) -> 5~9번
    # - POST valid data(데이터 검증에 성공한 경우) -> 10~14번


    # 5. POST 요청(데이터가 잘 못 들어온 경우)
    # 10. POST 요청(데이터가 잘 들어온 경우)
    if request.method == 'POST':
        # 6. 사용자가 입력한 데이터X(request.POST)를 담아서 form을 생성
        # 11. 사용자가 입력한 데이터O(request.POST)를 담아서 form을 생성
        form = ArticleForm(request.POST)

        # 7. form을 검증(실패)
        # 12. form을 검증(성공)
        if form.is_valid(): # 검증과정.
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
    return render(request, 'form.html', context)


def delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()

    return redirect('articles:index')


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
    return render(request, 'form.html', context)
    # context랑 return 을 else문 밖으로 안빼면 get 요청으로 들어오면 에러남.