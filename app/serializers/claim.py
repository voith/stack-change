from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import serializers

from app.models import Balance, Bounty, UserAssociation
from stackXchange.utils.serializer import required
from stackXchange.utils.stack_overflow import StackOverflow


class ClaimSerilizer(serializers.Serializer):
    bounty_id = serializers.IntegerField(validators=[required])

    def validate_bounty_id(self, value):
        claimed_user = self.context['request'].user
        try:
            bounty = Bounty.objects.get(id=value)
            self.context['bounty'] = bounty
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Failed'
            )
        question = bounty.question
        site = question.site
        answers = StackOverflow().get_question_answers(
            question.site_question_id, site.api_site_parameter
        )
        try:
            # FIXME: THIS SHOULD NOT FAIl
            # fetch this data from SE
            user_profile = UserAssociation.objects.get(account_id=claimed_user.account_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'BUG: userprofile does not exist'
            )
        for answer in answers:
            if answer['owner']['user_type'] != user_profile.site_user_id:
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
        question_user = bounty.question.user
        claimed_user = self.context['request'].user
        question_user_balance = Balance(user_id=question_user.id)
        claimed_user_balance = Balance(user_id=claimed_user.id)
        question_user_balance.amount -= bounty.amount
        claimed_user_balance.amount += bounty.amount
        question_user_balance.save()
        claimed_user_balance.save()
        return question_user


class BountyView(generics.CreateAPIView):

    serializer_class = ClaimSerilizer
    permission_classes = (IsAuthenticated,)
