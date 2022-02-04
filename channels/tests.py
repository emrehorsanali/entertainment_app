from django.test import TestCase
from .models import Channel, Content, Video, Pdf, Text
from io import StringIO
from django.core.management import call_command


class ChannelRatingsTestCase(TestCase):
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "calculate_channel_ratings",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_empty_run(self):
        out = self.call_command('--print')
        self.assertEqual(out, '')

    def test_no_content_run(self):
        channel1 = Channel.objects.create(title='channel1')

        out = self.call_command('--print')
        self.assertEqual(out, 'channel1, None\n')

    def test_single_content_run(self):
        channel1 = Channel.objects.create(title='channel1')
        Video.objects.create(channel=channel1, rating=6.6)

        out = self.call_command('--print')
        self.assertEqual(out, 'channel1, 6.6\n')

    def test_multiple_content_run(self):
        channel1 = Channel.objects.create(title='channel1')
        Video.objects.create(channel=channel1, rating=6.6)
        Pdf.objects.create(channel=channel1, rating=3.3)

        out = self.call_command('--print')
        self.assertEqual(out, 'channel1, 4.95\n')

    def test_single_subchannel_run(self):
        channel1 = Channel.objects.create(title='channel1')
        channel2 = Channel.objects.create(title='channel2', parent_channel=channel1)
        Video.objects.create(channel=channel2, rating=6.6)

        out = self.call_command('--print')
        self.assertEqual(out, 'channel1, 6.6\nchannel2, 6.6\n')

    def test_multiple_subchannel_run(self):
        channel1 = Channel.objects.create(title='channel1')
        channel2 = Channel.objects.create(title='channel2', parent_channel=channel1)
        channel3 = Channel.objects.create(title='channel3', parent_channel=channel1)
        Video.objects.create(channel=channel2, rating=6.6)
        Pdf.objects.create(channel=channel3, rating=3.3)

        out = self.call_command('--print')
        self.assertEqual(out, 'channel2, 6.6\nchannel1, 4.95\nchannel3, 3.3\n')

    def test_multiple_subchannel_no_content_run(self):
        channel1 = Channel.objects.create(title='channel1')
        channel2 = Channel.objects.create(title='channel2', parent_channel=channel1)
        channel3 = Channel.objects.create(title='channel3', parent_channel=channel1)
        Video.objects.create(channel=channel2, rating=6.6)

        out = self.call_command('--print')
        self.assertEqual(out, 'channel1, 6.6\nchannel2, 6.6\nchannel3, None\n')

    def test_multiple_subchannel_multiple_and_no_content_run(self):
        channel1 = Channel.objects.create(title='channel1')
        channel2 = Channel.objects.create(title='channel2', parent_channel=channel1)
        channel3 = Channel.objects.create(title='channel3', parent_channel=channel1)
        channel4 = Channel.objects.create(title='channel4', parent_channel=channel2)
        channel5 = Channel.objects.create(title='channel5', parent_channel=channel2)

        Video.objects.create(channel=channel4, rating=5.5)
        Pdf.objects.create(channel=channel5, rating=2.2)
        Text.objects.create(channel=channel5, rating=1)

        out = self.call_command('--print')
        self.assertEqual(out, 'channel4, 5.5\nchannel1, 3.55\nchannel2, 3.55\nchannel5, 1.6\nchannel3, None\n')
