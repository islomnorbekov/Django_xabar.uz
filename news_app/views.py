from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView,DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from hitcount.utils import get_hitcount_model

from .models import Category, News
from .forms import ContactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser
from hitcount.views import HitCountDetailView, HitCountMixin


def news_list(request):
    # news_list = News.published.filter(status=News.Status.Published) :bu ikkinchi usul pastdagi 1chi usul
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


class PostCountHitDetailView(HitCountDetailView):
    model = News        # your model goes here
    count_hit = True    # set to True if you want it to try and count the hit

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context ={}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits +1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    news_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data= request.POST)
        if comment_form.is_valid():
            #yangi comment obejctni yaratamiz lekin malumot bazasiga saqlamaymiz
            news_comment = comment_form.save(commit=False)
            #izoh egasini sorov yuborayotgan userga bogladik
            news_comment.news = news
            news_comment.user = request.user
            #malumotlar bazasiga saqlaymiz
            news_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        'comments': comments,
        'news_comment': news_comment,
        'comment_form': comment_form,
        'comment_count':comment_count
    }
    return render(request, 'news/news_detail.html', context)

@login_required
def homePageView(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:5]
    local_one = News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:1]
    local_news = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[:5]

    context = {
        'news_list': news_list,
        'categories': categories,
        "local_news": local_news,
        "local_one": local_one
    }
    return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[:5]
        context['xorij_xabarlar'] = News.published.all().filter(category__name="Xorij").order_by('-publish_time')[:5]
        context['sport_xabarlar'] = News.published.all().filter(category__name="Sport").order_by('-publish_time')[:5]
        context['texnologiya_xabarlar'] = News.published.all().filter(category__name="Texnologiya").order_by('-publish_time')[:5]
        return context

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, requst, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form

        }
        return render(requst, 'news/contact.html', context)

    def post(self, requst, *args, **kwargs):
        form = ContactForm(requst.POST)
        if requst.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('<h2> Biz bilan boglaningiz uchun rahmat</h2>')
        context = {
            'form': form
        }

        return render(requst, 'news/contact.html', context)


def Custom_404(request, exception):
    return render(request, 'news/404.html', status=404)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news


class ForiegnNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news



class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'


    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )














