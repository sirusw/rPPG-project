from django.core.management.base import BaseCommand
from server.management.commands.mqtt_setup import mqtt_client

class Command(BaseCommand):
    help = 'Starts the MQTT client'

    def handle(self, *args, **options):
        print("MQTT client started")