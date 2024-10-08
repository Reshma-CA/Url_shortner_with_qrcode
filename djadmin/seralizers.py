from rest_framework.serializers import ModelSerializer
from userapp.models import Short_url,People
from rest_framework import serializers
from django.db.models import Sum

class Url_LinkSerializer(ModelSerializer):
    class Meta:
        model = Short_url
        fields = ['id','original_url', 'short_code', 'short_url', 'qr_code_url', 'visit_count', 'created_at']


class User_Serializer(serializers.ModelSerializer):
    visit_count = serializers.IntegerField(read_only=True)  # Custom field to hold total visit count

    class Meta:
        model = People
        fields = ['id', 'username', 'email', 'visit_count','Number_of_shorterned_links']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Calculate total visit count for associated Short_url instances
        representation['visit_count'] = Short_url.objects.filter(user=instance).aggregate(total=Sum('visit_count'))['total'] or 0
        return representation