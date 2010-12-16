from django.core.management.base import NoArgsCommand

from congress import load

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        "Just load all members"
        load.members()