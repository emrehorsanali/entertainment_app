from django.core.management.base import BaseCommand
from channels.models import Channel


class Command(BaseCommand):
    help = 'Calculate and write channel ratings to a csv file'

    def add_arguments(self, parser):
        parser.add_argument(
            "--print",
            action="store_true",
            default=False,
            help="Print output instead of writing to a file",
        )

    def handle(self, *args, **options):
        print_flag = options['print']
        channels = list(Channel.objects.all())
        for channel in channels:
            channel.calculate_rating()
        channels.sort(key=lambda x: x.rating or -1, reverse=True)

        if not print_flag:
            file = open('channel_ratings.csv', 'w')

        for channel in channels:
            out_str = channel.title + ', ' + str(channel.rating)
            if print_flag:
                self.stdout.write(out_str)
            else:
                file.write(out_str + '\n')

        if not print_flag:
            file.close()
