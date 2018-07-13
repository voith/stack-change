from rest_framework_filters import filters, filterset
from rest_framework import serializers

from app.models import (
    Bounty,
    Question,
    StackExchangeSite,
    Tag
)
from stackXchange.utils.serializer import required


class TagsFilter(filterset.FilterSet):
    class Meta:
        model = Tag
        fields = {
            'name': ['exact'],
        }


class SiteFilter(filterset.FilterSet):
    class Meta:
        model = StackExchangeSite
        fields = {
            'name': ['exact'],
        }


class QuestionFilter(filterset.FilterSet):
    site = filters.RelatedFilter(SiteFilter, name='site', queryset=StackExchangeSite.objects.all())
    tag = filters.RelatedFilter(TagsFilter, name='tag', queryset=Tag.objects.all())

    class Meta:
        model = Question
        fields = {
            'id': ['exact']
        }


class BountyFilter(filterset.FilterSet):
    question = filters.RelatedFilter(QuestionFilter, name='question', queryset=Question.objects.all())

    class Meta:
        model = Bounty
        fields = {
            'state': ['exact']
        }


def get_question_details(url):
    pass


class BountySerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[required])
    bounty = serializers.DecimalField(validators=[required], max_digits=20, decimal_places=10)
    time_limit = serializers.IntegerField(validators=[required])

    class Meta:
        model = Bounty
        queryset = Bounty.objects.all()

    def create(self, validated_data):
        pass
