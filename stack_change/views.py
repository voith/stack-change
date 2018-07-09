from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from stack_change.serializers import UserSerializer


class HomeView(APIView):
    serializer_class = UserSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            user_data = self.serializer_class(user).to_json()
        else:
            user_data = {}
        return Response({'user': user_data}, template_name='index.html')
