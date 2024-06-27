from django.urls import path
from .views import news_list, news_detail, homePageView, ContactPageView, Custom_404,HomePageView, \
    LocalNewsView, ForiegnNewsView, TechnologyNewsView, SportNewsView


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news', news_list, name="all_news_list"),
    path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign/', ForiegnNewsView.as_view(), name='foreign_news_page'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    # path('', HomePageView, name='about_page'),
    path('', Custom_404, name='404page'),
]

