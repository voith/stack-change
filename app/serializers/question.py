from django.core.exceptions import ObjectDoesNotExist
from rest_framework_filters import filters, filterset
from rest_framework import serializers

from app.models import (
    Bounty,
    Question,
    StackExchangeSite,
    Tag
)
from stackXchange.utils.date import epoch_to_datetime, add_days_to_today
from stackXchange.utils.serializer import required
from stackXchange.utils.stack_overflow import StackOverflow
from stackXchange.utils.urls import get_site_url, get_url_part


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
            'api_site_parameter': ['exact'],
        }


class QuestionFilter(filterset.FilterSet):
    site = filters.RelatedFilter(SiteFilter, name='site', queryset=StackExchangeSite.objects.all())
    tags = filters.RelatedFilter(TagsFilter, name='tags', queryset=Tag.objects.all())

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


class BountySerializer(serializers.Serializer):
    url = serializers.URLField(validators=[required])
    bounty_amount = serializers.DecimalField(validators=[required], max_digits=20, decimal_places=10)
    time_limit = serializers.IntegerField(validators=[required])
    extra_kwargs = {
        'url': {'write_only': True},
        'bounty_amount': {'write_only': True},
        'amount': {'write_only': True},
    }

    class Meta:
        model = Bounty
        queryset = Bounty.objects.all()
        fields = ('url', 'bounty' 'time_limit')

    def validate_url(self, value):
        try:
            regex = '\/questions\/(\d+)\/*'
            site_url = get_site_url(value)
            site = StackExchangeSite.objects.get(site_url=site_url)
            question_id = get_url_part(value, regex)
            self.context['site'] = site
            self.context['question_id'] = question_id
            self.context['api_site_parameter'] = site.api_site_parameter
        except (IndexError, AttributeError, ObjectDoesNotExist):
            raise serializers.ValidationError(
                'Not a Valid StackExchange Site'
            )
        return value

    def create(self, validated_data):
        question_data = StackOverflow().get_question_details(
            self.context['question_id'],
            self.context['api_site_parameter']
        )
        question_obj = Question(**{
            'bountied_user_id': self.context['request'].user.id,
            'site_question_id':  self.context['question_id'],
            'site_question_url': question_data['link'],
            'site_id': self.context['site'].id,
            'title':  question_data['title'],
            'asked_on': epoch_to_datetime(question_data['creation_date'])
        })
        question_obj.save()
        for tag in question_data['tags']:
            _tag = Tag.objects.get_or_create(name=tag)[0]
            question_obj.tags.add(_tag.id)
        bounty = Bounty(**{
            'question_id': question_obj.id,
            'amount': validated_data['bounty_amount'],
            'expiry_date': add_days_to_today(validated_data['time_limit']),
            'state': 'OPEN',
        })
        bounty.save()
        return bounty

    def to_representation(self, instance):
        return {
            'bounty_amount': instance.amount,
            'tags': map(lambda x: x.name, instance.question.tags.all()),
            'url': instance.question.site_question_url,
            'expiry_date': instance.expiry_date,
            'title': instance.question.title,
            'source': instance.question.site.api_site_parameter,
            'state': instance.state,
        }
