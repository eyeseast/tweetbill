from django.core.management.base import NoArgCommand

from congress import load

class Command(NoArgCommand):
    
    def handle_noargs(self, **options):
        "Just load all members"
        load.members()