from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        if not isinstance(participants, list):
            participants = [participants]

        participants.append(request.user.id)
        users = list(User.objects.filter(id__in=participants))

        if len(users) < 2:
            return Response(
                {"error": "Thread must have at least two users"}, status=400
            )
        if len(users) > 2:
            return Response(
                {"error": "A thread can't have more than 2 participants."}, status=400
            )

        existing_threads = (
            Thread.objects.filter(participants__in=users)
            .annotate(num_participants=Count("participants"))
            .filter(num_participants=len(users))
            .distinct()
        )

        if existing_threads.exists():
            return Response(ThreadSerializer(existing_threads.first()).data)

        thread = Thread.objects.create()
        thread.participants.set(users)
        return Response(ThreadSerializer(thread).data, status=201)

    def destroy(self, request, *args, **kwargs):
        thread = self.get_object()
        if request.user not in thread.participants.all():
            return Response({"error": "Not allowed"}, status=403)

        thread.delete()
        return Response({"message": "Thread deleted"}, status=204)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        thread_id = self.request.data.get("thread_id")
        messages = Message.objects.filter(thread__id=thread_id)

        messages.filter(is_read=False).exclude(sender=self.request.user).update(
            is_read=True
        )

        return messages

    def create(self, request, *args, **kwargs):
        thread_id = request.data.get("thread")
        text = request.data.get("text")

        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return Response({"error": "Thread not found"}, status=404)

        message = Message.objects.create(thread=thread, sender=request.user, text=text)
        return Response(MessageSerializer(message).data, status=201)
