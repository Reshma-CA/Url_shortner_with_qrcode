from rest_framework.serializers import ModelSerializer
from userapp.models import Short_url


# class LinkSerializer(ModelSerializer):
#     class Meta:
#         model = MyLink
#         fields = '__all__'
#         read_only_fields = ['hash']

class LinkSerializer(ModelSerializer):
    class Meta:
        model = Short_url
        fields = ['id','original_url', 'short_code', 'short_url', 'qr_code_url', 'visit_count', 'created_at']
       