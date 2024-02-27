from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from dotenv import load_dotenv
from deepgram import Deepgram
from typing import Dict
from googletrans import Translator
from django.core.cache import cache
import os

from_lang = 'en'

# For home page
class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    # Get drop box values
    async def receive_json(self, content, **kwargs):
        from_lang = content['dropdown1'] 
        dest_lang = content['dropdown2']
        print(from_lang)
        session_key = self.scope["session"].session_key
        cache.set(f"{session_key}_from_lang", from_lang, timeout=3600)
        cache.set(f"{session_key}_dest_lang", dest_lang, timeout=3600)

load_dotenv()

translator = Translator()

class TranscriptConsumer(AsyncWebsocketConsumer):
   dg_client = Deepgram('261c65fb2d1608d4f9adbdc10d53f867e1d66957')

   async def get_transcript(self, data: Dict) -> None:
        if 'channel' in data:
            transcript = data['channel']['alternatives'][0]['transcript']
            if transcript:
                print(transcript)
                #translate before sending to js
                session_key = self.scope["session"].session_key
                from_lang = cache.get(f"{session_key}_from_lang", "auto")
                dest_lang = cache.get(f"{session_key}_dest_lang", "en")
                transcript = translator.translate(transcript, src="auto", dest=dest_lang).text
                await self.send(transcript)


   async def connect_to_deepgram(self):
       try:
            # set language and other perams
            session_key = self.scope["session"].session_key
            from_lang = cache.get(f"{session_key}_from_lang", "en")
            self.socket = await self.dg_client.transcription.live({'model': "nova-2", 'punctuate': True, 'language': from_lang, 'interim_results': False})
            self.socket.registerHandler(self.socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
            self.socket.registerHandler(self.socket.event.TRANSCRIPT_RECEIVED, self.get_transcript)

       except Exception as e:
           raise Exception(f'Could not open socket: {e}')

   async def connect(self):
       await self.connect_to_deepgram()
       await self.accept()
          

   async def disconnect(self, close_code):
       await self.channel_layer.group_discard(
           self.room_group_name,
           self.channel_name
       )

   async def receive(self, bytes_data):
       self.socket.send(bytes_data)
