from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import serializers

from app.models import Balance, Bounty, UserAssociation
from stackXchange.utils.serializer import required
from stackXchange.utils.stack_overflow import StackOverflow


class ClaimSerializer(serializers.Serializer):
    bounty_id = serializers.IntegerField(validators=[required])

    def validate_bounty_id(self, value):
        claimed_user = self.context['request'].user
        try:
            bounty = Bounty.objects.get(id=value)
            self.context['bounty'] = bounty
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'no bounty found'
            )
        if bounty.state != 'OPEN':
            raise serializers.ValidationError(
                'bounty not open'
            )
        question = bounty.question
        site = question.site
        answers = StackOverflow().get_question_answers(
            question.site_question_id, site.api_site_parameter
        )
        user_profile = UserAssociation.objects.filter(user_id=claimed_user.id)
        siter_user_ids = list(map(lambda x: x.site_user_id, user_profile))
        for answer in answers:
            if answer['owner']['user_type'] in siter_user_ids:
                continue
            if answer['is_accepted'] is not True:
                raise serializers.ValidationError(
                    'Answer provided not accepted'
                )
            else:
                return value
        else:
            raise serializers.ValidationError(
                'did not find any answer accepted by user'
            )

    def to_representation(self, instance):
        return {
            'status': 'OK'
        }

    def create(self, validated_data):
        bounty = self.context['bounty']
        question_user = bounty.question.bountied_user
        claimed_user = self.context['request'].user
        question_user_balance = Balance.objects.get_or_create(user_id=question_user.id)[0]
        claimed_user_balance = Balance.objects.get_or_create(user_id=claimed_user.id)[0]
        question_user_balance.amount -= bounty.amount
        claimed_user_balance.amount += bounty.amount
        question_user_balance.save()
        claimed_user_balance.save()
        bounty.state = 'COMPLETED'
        bounty.save()
        return question_user


class ClaimView(generics.CreateAPIView):

    serializer_class = ClaimSerializer
    permission_classes = (IsAuthenticated,)
