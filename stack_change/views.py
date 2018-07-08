# from rest_framework import parsers, renderers
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from stack_change.serializers import StackExchangeOauthSerializer
#
#
# class RegisterStackExchangeUser(APIView):
#     throttle_classes = ()
#     permission_classes = ()
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
#     renderer_classes = (renderers.JSONRenderer,)
#     serializer_class = StackExchangeOauthSerializer
#
#     def get(self, request):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user_details = serializer.validated_data['user_details']
#         return Response({'status': 'OK'})
#
#
# login = RegisterStackExchangeUser.as_view()
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def gh_login(request):
    """Attempt to redirect the user to Github for authentication."""
    return redirect('social:begin', backend='stackoverflow')
