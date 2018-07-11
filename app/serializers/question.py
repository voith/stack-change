from rest_framework_filters import filters, filterset
from rest_framework import serializers

from app.models import (
    Bounty,
    Question,
    StackExchangeSite,
    Tag
)


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


class BountySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bounty
        queryset = Bounty.objects.all()
