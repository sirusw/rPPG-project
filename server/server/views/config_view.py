from django.http import JsonResponse
from server.management.commands.mqtt_setup import mqtt_client  # import the global MQTT client
import json

def send_mqtt_cmd(request):
    if request.method == 'POST':
        raw_json = request.body.decode('utf-8')  # Decode the byte string
        
        mqtt_client.client.publish("/config/rx", raw_json)

        if mqtt_client is None:
            return JsonResponse({'error': 'MQTT client is not running'}, status=500)

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)

# def sync_param(request):
#     if request.method == 'POST':
#         json_data = request.body.decode('utf-8')  # Decode the byte string
#         data = json.loads(json_data)
#         received_data = None

#         if data.get('param') == 'sync' and data.get('value') == 0:
#             def on_message(client, userdata, msg):
#                 nonlocal received_data
#                 print(msg.payload.decode())
#                 received_data = json.loads(msg.payload.decode())

#             mqtt_client.client.subscribe("/config/tx") 
#             mqtt_client.client.publish("/config/rx", json_data)
        
#         return JsonResponse(received_data, status=200)
#     else:
#         return JsonResponse({'error': 'Invalid HTTP method'}, status=400)

import time

def sync_param(request):
    if request.method == 'POST':
        mqtt_client.client.publish("/config/rx", "{\"param\":\"sync\",\"value\":0}")
        for _ in range(10):  # Adjust the range as needed
            if mqtt_client.received_param:
                return JsonResponse(mqtt_client.received_param, status=200)
            time.sleep(1)

        # If no data has been received after waiting, return an error
        return JsonResponse({'error': 'No data received from /config/tx'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)
        