from rest_framework import serializers
from decimal import Decimal
from .models import User, Wallet, Operation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']


class OperationSerializer(serializers.ModelSerializer):
    operation_type = serializers.ChoiceField(
        choices=[Operation.OP_DEPOSIT, Operation.OP_WITHDRAW]
    )
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        model = Operation
        fields = ('id', 'wallet', 'operation_type', 'amount', 'created_at')
        read_only_fields = ('id', 'wallet', 'created_at')

    def validate_amount(self, value: Decimal):
        if value <= 0:
            raise serializers.ValidationError('Amount must be positive')
        return value
