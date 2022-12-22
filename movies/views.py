from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear:
    """ Жанри та роки виходу фільмів """

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").distinct()


class MoviesView(GenreYear, ListView):
    """ Список фільмів """
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # template_name = "movies/movie_list.html"


class MovieDetailView(GenreYear, DetailView):
    """ Повний опис фільму """
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """ Вивід інформації про актора """
    model = Actor
    template_name = 'movies/actor.html'
    # Поле по якому ми шукаємо акторів
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """ Фільтр фільмів """
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset



class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)