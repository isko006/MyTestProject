from rest_framework import serializers
from main.models import *

from rest_framework.exceptions import ValidationError


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id rate text'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    filtered = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id name duration date age_restriction genres reviews filtered rating'.split()

    def get_filtered(self, movie):
        reviews = Review.objects.filter(movie=movie).exclude(text__contains='ниггер')
        return ReviewSerializer(reviews, many=True).data


class MovieCreateValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)
    duration = serializers.IntegerField()
    date = serializers.DateField()
    age_restriction = serializers.CharField(min_length=2, max_length=3)
    genres = serializers.ListField(child=serializers.IntegerField(), required=True)


    def validate_name(self, name):
        movies = Movie.objects.filter(name=name)
        if movies.count() > 0:
            raise ValidationError("Такой фильм уже существует!!!")
        return name

    def validate_age_restriction(self, age):
        if age[-1] != '+':
            raise ValidationError('Последний символ должен быть +')
        try:
            int(age[:-1])
        except:
            raise ValidationError('До + должно быть число')








