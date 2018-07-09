import json

from rest_framework.serializers import ModelSerializer

from app.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'account_id')

    def to_json(self):
        return json.dumps(self.data)
