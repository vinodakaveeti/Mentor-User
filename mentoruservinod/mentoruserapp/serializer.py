from rest_framework import serializers
from .models import CustomUser, Conversation


class ConversationSerializer(serializers.ModelSerializer):
    document = serializers.FileField()
    # Used to filter the user sender in the new mail page
    current_email = ''

    def __init__(self, *args, **kwargs):
        if 'email' in kwargs:
            ConversationSerializer.current_email = kwargs.pop('email')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Conversation
        fields = ('sender', 'receipient', 'conversation', 'document')
        extra_kwargs = {'document': {'required': True}, }

    def get_fields(self, *args, **kwargs):
        fields = super(ConversationSerializer, self).get_fields(*args, **kwargs)
        fields['sender'].queryset = CustomUser.objects.filter(email=ConversationSerializer.current_email)
        fields['receipient'].queryset = CustomUser.objects.filter(is_mentor=True)
        return fields


class MentorReplySerializer(serializers.ModelSerializer):
    query = serializers.ReadOnlyField(source='conversation')
    reply = serializers.CharField()
    sender_email = serializers.ReadOnlyField(source='get_sender_email')

    class Meta:
        model = Conversation
        fields = ('sender_email', 'query', 'reply')
