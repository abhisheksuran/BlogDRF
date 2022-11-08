from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name',  'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):

        if 'password' in validated_data:

            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

    
class TokenAuthSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            msg = _("Can't authenticate with these credentials!!!")
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


