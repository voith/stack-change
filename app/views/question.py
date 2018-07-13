from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics

from app.models import Bounty
from app.serializers.question import BountyFilter, BountySerializer


class BountyView(generics.ListCreateAPIView):
    queryset = Bounty.objects.filter(state='OPEN')
    serializer_class = BountySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = BountyFilter
