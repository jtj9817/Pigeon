from rest_framework import serializers
from pigeon_posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    body = serializers.CharField(max_length=512, required=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'date_published', 'date_updated']

    def __init__(self, *args, **kwargs):
        # Prevent Author field from being changed once Post has been created
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('author').read_only = True
