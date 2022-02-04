from rest_framework import serializers
from .models import Channel, Content, Video, Pdf, Text
from collections import OrderedDict


class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class NonEmptyListModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if not isinstance(result[key], list) or result[key]])


class VideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ['id', 'rating', 'channel']


class PdfDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        exclude = ['id', 'rating', 'channel']


class TextDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ['id', 'rating', 'channel']


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ['id', 'rating', 'channel', 'file']


class PdfListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        exclude = ['id', 'rating', 'channel', 'file']


class TextListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ['id', 'rating', 'channel', 'file']


class ContentListSerializer(NonNullModelSerializer):
    video = VideoListSerializer(read_only=True)
    pdf = PdfListSerializer(read_only=True)
    text = TextListSerializer(read_only=True)

    class Meta:
        model = Content
        exclude = ['channel', ]


class ContentDetailSerializer(NonNullModelSerializer):
    video = VideoDetailSerializer(read_only=True)
    pdf = PdfDetailSerializer(read_only=True)
    text = TextDetailSerializer(read_only=True)

    class Meta:
        model = Content
        fields = '__all__'


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        exclude = ['parent_channel']


class ChannelDetailSerializer(NonEmptyListModelSerializer):
    contents = ContentListSerializer(source='content_set', many=True, read_only=True)
    subchannels = ChannelListSerializer(source='channel_set', many=True, read_only=True)

    class Meta:
        model = Channel
        fields = '__all__'

