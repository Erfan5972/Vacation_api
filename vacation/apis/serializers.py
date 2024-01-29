from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .. models import Vacation, VacationResponse
from node.models import NodeConnection


class VacationForVacationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = ('status', )


class VacationResponseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacationResponse
        fields = '__all__'


class VacationResponseCreateSerializer(serializers.ModelSerializer):
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
                    try:
                        node_connection = NodeConnection.objects.filter(to_node=node).first()
                    except NodeConnection.DoesNotExist:
                        raise ValidationError('This node connection does not exist')
                    if node_connection:
                        try:
                            vacation_response = VacationResponse.objects.get(
                                vacation=vacation,
                                status='P',
                                node=node_connection.from_node
                            )
                        except VacationResponse.DoesNotExist:
                            raise ValidationError('The technical manager has not yet confirmed this vacation')

                        if vacation_response:
                            vacation.status = 'F'
                            vacation.save()
                            srz_data = VacationForVacationResponseSerializer(instance=vacation)
                            return srz_data.data
                        else:
                            raise ValidationError('The technical manager has not yet confirmed this vacation')


                else:
                    vacation.status = 'F'
                    vacation.save()
                    srz_data = VacationForVacationResponseSerializer(instance=vacation)
                    return srz_data.data

            raise ValidationError('This vacation has been answered before')
        if status == 'T':
            if vacation.status == 'P':
                if node.is_final == True:
                    try:
                        node_connection = NodeConnection.objects.get(to_node=node)
                    except NodeConnection.DoesNotExist:
                        raise ValidationError('This node connection does not exist')
                    if node_connection:
                        try:
                            vacation_response = VacationResponse.objects.get(
                                vacation=vacation,
                                status='P',
                                node=node_connection.from_node
                            )
                        except VacationResponse.DoesNotExist:
                            raise ValidationError('The technical manager has not yet confirmed this vacation')
                        if vacation_response:
                            vacation.status = 'T'
                            vacation.save()
                            srz_data = VacationForVacationResponseSerializer(instance=vacation)
                            return srz_data.data
                        else:
                            raise ValidationError('The technical manager has not yet confirmed this vacation')

                    else:
                        raise ValidationError('This node connection does not exist')


                else:
                    try:
                        node_connection = NodeConnection.objects.filter(from_node=node).first()
                    except NodeConnection.DoesNotExist:
                        raise ValidationError('This node connection does not exist')

                    if node_connection:
                        vacation_response = VacationResponse.objects.create(
                                vacation=obj.vacation,
                                node=node_connection.to_node,
                                status='P'
                            )

                        data = VacationResponseListSerializer(vacation_response).data
                        return data

                    raise ValidationError('This node connection does not exist')

            raise ValidationError('This vacation has been answered before')


class VacationCreateSerializer(serializers.ModelSerializer):
    vacation_response = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vacation
        fields = ['user',
                  'from_date',
                  'to_date',
                  'description',
                  'vacation_response']

    def get_vacation_response(self, obj):
        vacation_responses = []
        role = obj.user.role
        if role == 'E':
            node_connections = NodeConnection.objects.get(from_node=1)
            vacation_response = VacationResponse(
                        vacation=obj,
                        node=node_connections.to_node,
                        status='P'
                    )
            vacation_response.save()
            vacation_responses.append(vacation_response)

        if role == 'T':
            node_connections = NodeConnection.objects.get(from_node=2)
            vacation_response = VacationResponse(
                        vacation=obj,
                        node=node_connections.to_node,
                        status='P'
                    )
            vacation_response.save()
            vacation_responses.append(vacation_response)

        if role == 'M':
            raise ValidationError('you are manager and you cant create a vacation')
        print(vacation_responses)
        return VacationResponseListSerializer(vacation_responses, many=True).data


class VacationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'


class VacationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = ['from_date',
                  'to_date',
                  'description',
                  'status']
        read_only_fields = ('status', )