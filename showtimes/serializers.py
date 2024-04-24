from datetime import datetime, timedelta

from rest_framework import serializers

from showtimes.models import Cinema, Screening

from movielist.models import Movie


#moje
class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cinema
        fields = ['name', 'city', 'movies']


class ScreeningSerializer(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(slug_field='name', queryset=Cinema.objects.all())
    movie = serializers.SlugRelatedField(slug_field='title', queryset=Movie.objects.all())
                                         #filter(date__lte=datetime.now()+timedelta(days=30)))
    class Meta:
        model = Screening
        fields = ['movie', 'cinema', 'date']

#rozwiązanie
# from showtimes.models import Cinema
# from rest_framework import serializers
#
#
# class CinemaSerializer(serializers.ModelSerializer):
#     movies = serializers.HyperlinkedRelatedField(
#         many=True,
#         read_only=True,
#         view_name='movies-detail'
#     )
#     class Meta:
#         model = Cinema
#         fields = ['name', 'city', 'movies']



'''
W pierwszej wersji serializera, która korzysta z HyperlinkedModelSerializer, gdy pole movies zostanie zserializowane, 
będzie zawierało hiperłącza do detali każdego z filmów. To oznacza, że cały obiekt filmu nie zostanie osadzony w 
wynikowych danych, a jedynie hiperłącze do jego szczegółów.
Natomiast w drugiej wersji serializera, gdzie użyto HyperlinkedRelatedField, dane dla pola movies będą zawierać tylko 
hiperłącza do detali filmów, co oznacza, że tylko nazwa filmu nie zostanie osadzona w wynikowych danych.
Decyzja, która wersja jest bardziej odpowiednia, zależy od twoich potrzeb i preferencji. Jeśli chcesz, aby w wynikowych 
danych był dostępny pełny obiekt filmu za pośrednictwem hiperłączy, pierwsza wersja byłaby lepsza. Jeśli wystarczy ci tylko 
hiperłącze do filmu, druga wersja jest wystarczająca.
'''