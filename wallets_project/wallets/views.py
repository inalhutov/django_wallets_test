from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Wallet, Operation
from .serializers import UserSerializer, WalletSerializer, OperationSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WalletCreateAPIView(generics.CreateAPIView):
    serializer_class = WalletSerializer

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Создаём кошелёк
        wallet = Wallet.objects.create(user=user, balance=0)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WalletDetailAPIView(APIView):
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, pk=wallet_uuid)
        return Response(WalletSerializer(wallet).data)


class WalletOperationAPIView(APIView):
    def post(self, request, wallet_uuid):
        data = request.data.copy()
        data['wallet'] = wallet_uuid
        serializer = OperationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        op_type = serializer.validated_data['operation_type']
        amount = Decimal(serializer.validated_data['amount'])

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(pk=wallet_uuid)

            if op_type == Operation.OP_DEPOSIT:
                wallet.balance += amount
            elif op_type == Operation.OP_WITHDRAW:
                if wallet.balance < amount:
                    return Response(
                        {'detail': 'Insufficient funds'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                wallet.balance -= amount

            wallet.save(update_fields=['balance'])
            operation = Operation.objects.create(
                wallet=wallet,
                operation_type=op_type,
                amount=amount
            )

        return Response(OperationSerializer(operation).data, status=status.HTTP_201_CREATED)


def index(request):
    return render(request, "index.html")
