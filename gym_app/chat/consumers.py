import json, requests
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.mail import send_mail
from .models import ChatMessage, ChatGroup
from better_profanity import profanity

profanity.load_censor_words()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"🔌 Conectando al grupo: {self.scope['url_route']['kwargs'].get('group_name')}")
        self.user = self.scope["user"]
        self.group_name = self.scope['url_route']['kwargs'].get('group_name')
        self.room_group_name = f"chat_{self.group_name}"

        if self.user.is_authenticated:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user_message = data['message']
            flagged = profanity.contains_profanity(user_message)
            clean_message = profanity.censor(user_message) if flagged else user_message

            # Verificar que el grupo existe
            try:
                group = ChatGroup.objects.get(name=self.group_name)
            except ChatGroup.DoesNotExist:
                await self.send(text_data=json.dumps({'message': '⚠️ Grupo no encontrado.'}))
                return

            # Guardar el mensaje del usuario
            ChatMessage.objects.create(
                user=self.user,
                group=group,
                role='user',
                message=clean_message,
                flagged=flagged
            )

            # Notificación por correo si hay palabras clave
            if "lesión" in user_message.lower() or "urgente" in user_message.lower():
                send_mail(
                    subject="🚨 Pregunta importante en el chat",
                    message=f"{self.user.username} preguntó: {user_message}",
                    from_email="noreply@gymchat.com",
                    recipient_list=["coach@gym.com"]
                )

            # Enviar mensaje al grupo
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': f"{self.user.username}: {clean_message}"
            })

            # Si el grupo es 'IA', generar respuesta automática
            if self.group_name.lower() == "ia":
                prompt = f"Eres un experto en entrenamiento y nutrición. Responde profesionalmente: {clean_message}"
                headers = {"Authorization": "Bearer TU_TOKEN_HUGGINGFACE"}
                payload = {"inputs": prompt}
                response = requests.post(
                    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                    headers=headers,
                    json=payload
                )
                ai_text = response.json().get('generated_text', 'Lo siento, no entendí eso.') if response.status_code == 200 else "⚠️ Error con la IA"

                # Guardar respuesta de la IA
                ChatMessage.objects.create(
                    user=self.user,
                    group=group,
                    role='ai',
                    message=ai_text
                )

                # Enviar respuesta al cliente
                await self.send(text_data=json.dumps({'message': f"IA: {ai_text}"}))

        except Exception as e:
            await self.send(text_data=json.dumps({'message': f'⚠️ Error interno: {str(e)}'}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))
