# from django.utils.translation import ugettext_lazy as _
#
# from rest_framework import serializers
# from django.contrib.auth import authenticate
#
# from stack_change.exceptions import BadStatusCode
# from stack_change.utils.stack_overflow_aouth import StackOverflowOauth
#
#
# stack_change_auth_obj = StackOverflowOauth()
#
#
# class StackExchangeOauthSerializer(serializers.Serializer):
#     code = serializers.CharField(label=_("Code"))
#
#     def validate(self, attrs):
#         code = attrs.get('code')
#         if not code or not isinstance(code, str):
#             msg = _('code should be an instance of str')
#             raise serializers.ValidationError(msg)
#         try:
#             user_details = stack_change_auth_obj.get_user_from_code(code)
#         except BadStatusCode:
#             msg = _('failed to fetch user from stackexchange')
#             raise serializers.ValidationError(msg, code='authorization')
#         attrs['user_details'] = user_details
#         return attrs
