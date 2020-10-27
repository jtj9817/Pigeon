from rest_framework import serializers
from pigeon_messaging.models import Message


class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=512, required=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        # Prevent Sender and Receiver fields from being editable once a Message object has been created
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('sender').read_only = True
            self.fields.get('receiver').read_only = True
