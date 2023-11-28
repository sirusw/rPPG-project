from django.http import JsonResponse
from server.management.commands.mqtt_setup import mqtt_client  # import the global MQTT client
import logging
def send_mqtt_cmd(request):
    if request.method == 'POST':
        raw_json = request.body.decode('utf-8')  # Decode the byte string
        
        mqtt_client.client.publish("/config/rx", raw_json)

        if mqtt_client is None:
            return JsonResponse({'error': 'MQTT client is not running'}, status=500)

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)