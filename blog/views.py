from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, Category, Comment
from .forms import CommentForm

def homepage(request):
    # Retrieve single hero featured article
    featured_article = Article.objects.filter(status='published', is_featured=True).first()

    # Query latest articles (exclude featured article if present)
    latest_articles_qs = Article.objects.filter(status='published').order_by('-created_at')
    if featured_article:
        latest_articles_qs = latest_articles_qs.exclude(id=featured_article.id)

    # Search filter logic
    query = request.GET.get('q')
    if query:
        latest_articles_qs = Article.objects.filter(status='published').filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'featured_article': featured_article,
        'latest_articles': latest_articles_qs,
        'categories': categories,
        'query': query,
    }
    return render(request, 'blog/index.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    comments = article.comments.filter(active=True)
    categories = Category.objects.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, user=request.user)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            if request.user.is_authenticated:
                new_comment.author = request.user
                new_comment.name = request.user.username
                new_comment.email = request.user.email
            new_comment.save()
            return redirect('article_detail', slug=article.slug)
    else:
        comment_form = CommentForm(user=request.user)

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
    }
    return render(request, 'blog/article_detail.html', context)


def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles_list = Article.objects.filter(category=category, status='published').order_by('-created_at')
    categories = Category.objects.all()

    paginator = Paginator(articles_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'articles': page_obj,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog/category.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article

@login_required
def homepage(request):
    query = request.GET.get('q', '')
    
    # Grab all published articles
    articles_list = Article.objects.filter(status='published').order_by('-created_at')
    
    if query:
        articles_list = articles_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    # Paginate (6 articles per page)
    paginator = Paginator(articles_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Pass BOTH variable names so index.html never comes up empty
    context = {
        'page_obj': page_obj,
        'latest_articles': page_obj,
        'query': query,
    }
    return render(request, 'blog/index.html', context)
    
@login_required
def like_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('article_detail', slug=slug)