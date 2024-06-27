from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import Category, News
from .forms import ContactForm


def news_list(request):
    # news_list = News.published.filter(status=News.Status.Published) :bu ikkinchi usul pastdagi 1chi usul
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news
    }
    return render(request, 'news/news_detail.html', context)


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








