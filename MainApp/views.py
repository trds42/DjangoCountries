from django.shortcuts import render
from django.core.paginator import Paginator
import MainApp.country_by_languages
import string

countries = MainApp.country_by_languages.get_countries()


def home(request):
    return render(request, "index.html")


def country_page(request, country_name):
    for country in countries:
        if country["country"] == country_name:
            context = {
                "country": country
            }
    return render(request, "country_page.html", context)


def countries_list(request, letter='', language=''):
    alphabet = list(string.ascii_uppercase)

    if letter != '':
        countries_to_show = []
        text = f" на букву {letter}"
        for country in countries:
            if country["country"][0] == letter:
                countries_to_show.append(country)

    elif language != '':
        countries_to_show = []
        text = f", где говорят на языке {language}"
        for country in countries:
            for country_lang in country["languages"]:
                if country_lang == language:
                    countries_to_show.append(country)

    else:
        countries_to_show = countries
        text = ''

    paginator = Paginator(countries_to_show, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "alphabet": alphabet,
        "text": text
    }
    return render(request, "countries_list.html", context)


def languages_list(request):
    languages_to_show = []
    for country in countries:
        for country_lang in country["languages"]:
            languages_to_show.append(country_lang)

    languages_to_show = set(languages_to_show)
    languages_to_show = sorted(languages_to_show)

    context = {
        "languages": languages_to_show
    }
    return render(request, "languages_list.html", context)