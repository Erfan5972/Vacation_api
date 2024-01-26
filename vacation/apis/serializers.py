from rest_framework import serializers

from .. models import Vacation, VacationResponse
from node.models import NodeConnection


class VacationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacationResponse
        fields = '__all__'


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        exclude = ('status',)


    def create(self, validated_data):
        user = validated_data['user']
        role = user.role
        if role == 'E':
            node_connection = NodeConnection.objects.filter(from_node=1)
            VacationResponse.objects.create(vacation=validated_data['id'],
                                            node=node_connection['to_node'],
                                            status='P')
