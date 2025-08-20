"""
WebSocket consumers for real-time dashboard updates
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join dashboard group
        self.room_group_name = "dashboard"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Send welcome message
        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "Connected to CS Student Hub Dashboard!",
                }
            )
        )

    async def disconnect(self, close_code):
        # Leave dashboard group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle messages from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Echo message back (for testing)
        await self.send(
            text_data=json.dumps({"type": "echo", "message": f"Echo: {message}"})
        )

    # Receive message from room group
    async def dashboard_update(self, event):
        message = event["message"]
        update_type = event["update_type"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": update_type, "message": message}))
