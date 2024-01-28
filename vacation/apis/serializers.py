from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .. models import Vacation, VacationResponse
from node.models import NodeConnection


class VacationForVacationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = ('status', )


class VacationResponseForVacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacationResponse
        fields = '__all__'


class VacationResponseSerializer(serializers.ModelSerializer):
    validate_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VacationResponse
        fields = ['vacation',
                  'node',
                  'status',
                  'validate_status',
                  ]

    def get_validate_status(self, obj):
        status = obj.status
        vacation = obj.vacation
        node = obj.node
        if status == 'F':
            if vacation.status == 'P':
                if node.is_final == True:
                    node_connection = NodeConnection.objects.filter(to_node=node).first()
                    log = VacationResponse.objects.filter(vacation=vacation,
                                                          status='P',
                                                          node=node_connection.from_node)
                    if log.exists():
                        vacation.status = 'F'
                        vacation.save()
                        srz_data = VacationForVacationResponseSerializer(instance=vacation)
                        return srz_data.data
                    raise ValidationError('The technical manager has not yet confirmed this vacation')
                else:
                    vacation.status = 'F'
                    vacation.save()
                    srz_data = VacationForVacationResponseSerializer(instance=vacation)
                    return srz_data.data
            raise ValidationError('this vacation has been answered before')
        if status == 'T':
            if vacation.status == 'P':
                if node.is_final == True:
                    node_connection = NodeConnection.objects.filter(to_node=node).first()
                    log = VacationResponse.objects.filter(vacation=vacation,
                                                          status='P',
                                                          node=node_connection.from_node)
                    if log.exists():
                        vacation.status = 'T'
                        vacation.save()
                        srz_data = VacationForVacationResponseSerializer(instance=vacation)
                        return srz_data.data
                    return None
                else:
                    node_connection = NodeConnection.objects.get(from_node=node)
                    vacation_response = VacationResponse.objects.create(vacation=obj.vacation,
                                                                        node=node_connection.to_node,
                                                                        status='P'
                                                                        )
                    data = VacationResponseForVacationSerializer(vacation_response).data
                    return data
            raise ValidationError('this vacation has been answered before')


class VacationSerializer(serializers.ModelSerializer):
    vacation_response = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vacation
        fields = ['id',
                  'user',
                  'from_date',
                  'to_date',
                  'description',
                  'created_at',
                  'updated_at',
                  'status',
                  'vacation_response']
        read_only_fields = ['status']


    def get_vacation_response(self, obj):
        vacation_responses = []
        role = obj.user.role

        if role == 'E':
            node_connections = NodeConnection.objects.filter(from_node=1).first()
            vacation_response = VacationResponse(
                    vacation=obj,
                    node=node_connections.to_node,
                    status='P'
                )
            vacation_response.save()
            vacation_responses.append(vacation_response)

        if role == 'T':
            node_connections = NodeConnection.objects.filter(from_node=2).first()
            vacation_response = VacationResponse(
                    vacation=obj,
                    node=node_connections.to_node,
                    status='P'
                )
            vacation_response.save()
            vacation_responses.append(vacation_response)

        if role == 'M':
            raise ValidationError('you are manager and you cant create a vacation')

        return VacationResponseForVacationSerializer(vacation_responses, many=True).data