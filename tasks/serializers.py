from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'status',
            'due_date', 'created_at', 'updated_at', 'owner'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')


class TaskStatusSerializer(serializers.ModelSerializer):
    """Lightweight serializer for toggling task status only."""
    class Meta:
        model = Task
        fields = ('id', 'status')