from .models import Channel, Content
from .serializers import ChannelDetailSerializer, ContentDetailSerializer, \
    ChannelListSerializer, ContentListSerializer
from rest_framework import viewsets


class ChannelsView(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChannelDetailSerializer
        return ChannelListSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return super().get_queryset()
        return Channel.objects.filter(parent_channel__isnull=True).all()


class ContentsView(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContentDetailSerializer
        return ContentListSerializer
