'''Eqivalent to views'''

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class AudioConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'test_audio_group'
        async_to_sync(self.channel_layer.group_add)(
           self.group_name,
           self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'type':'connected'}))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']
        print(message)
        
        # self.send(text_data=json.dumps({'message':'Reply'}))
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'audio_messages',
                'data': message
            }
        )
    
    def audio_messages(self, event):
        print(event, type(event))
        data = event['data']
        # print(data)
        # print("data: ",json.loads(data))
        try:
            self.send(text_data=json.dumps({
                'type':'audio_data',
                'data': json.loads(data)
            }))
        except:
            self.send(text_data=data)

    def disconnect(self, *args, **kwargs):
        print('Disconnected')

# helper func
def parse_query(query_string):
    if '&' in query_string:
        query_string = query_string.split('&')
        print(query_string)
    else:
        key, value = query_string.split('=')
        query_dict = {key: value}
        print(query_dict)

class TempConsumer(WebsocketConsumer):
    def connect(self):
        # print('self.scope: ', self.scope)
        query_string = self.scope['query_string'].decode('utf-8')
        print("query_string: ", query_string)
        parse_query(query_string)
        
        self.group_name = 'test_audio_group2'
        async_to_sync(self.channel_layer.group_add)(
           self.group_name,
           self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'type':'connected'}))
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']
        
        # self.send(text_data=json.dumps({'message':'Reply'}))
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'messages',
                'data': message
            }
        )
    
    def messages(self, event):
        print(event, type(event))
        data = event['data']
        # print(data)
        # print("data: ",json.loads(data))
        try:
            self.send(text_data=json.dumps({
                # 'type':'chat',
                'data': json.loads(data)
            }))
        except:
            self.send(text_data=data)
    
    def disconnect(self, *args, **kwargs):
        print('Disconnected')