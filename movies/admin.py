from django.contrib import admin
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Категорії """
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """ Відгуки на сторінці фільму """
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """ Фільми """
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("category__name", "title")
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    # fields = (("actors", "directors", "genres"), )
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """ Відгуки """
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """ Жанри """
    list_display = ("name", "url")

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """ Актори та режисери """
    list_display = ("name", "age")

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Рейтинг """
    list_display = ("star", "ip")

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """ Кадри з фільму """
    list_display = ("title", "movie")

admin.site.register(RatingStar)

