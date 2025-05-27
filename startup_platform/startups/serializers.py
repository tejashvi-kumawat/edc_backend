from rest_framework import serializers
from .models import Startup
from accounts.serializers import UserSerializer

class StartupSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    is_approved = serializers.ReadOnlyField()

    class Meta:
        model = Startup
        fields = [
            'id', 'name', 'description', 'industry', 'stage', 'location',
            'website', 'email', 'phone', 'logo', 'status', 'created_by',
            'approved_by', 'created_at', 'updated_at', 'approved_at', 'is_approved'
        ]
        read_only_fields = ('id', 'status', 'created_at', 'updated_at', 'approved_at', 'approved_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class StartupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = [
            'name', 'description', 'industry', 'stage', 'location',
            'website', 'email', 'phone', 'logo'
        ]

class StartupApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = ['status']

    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("Status must be 'approved' or 'rejected'")
        return value