import uuid
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


class User(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal('0.00')
    )

    def __str__(self):
        return f'{self.user.name} — {self.balance}'


class Operation(models.Model):
    OP_DEPOSIT = 'DEPOSIT'
    OP_WITHDRAW = 'WITHDRAW'
    OPERATION_CHOICES = (
        (OP_DEPOSIT, 'Deposit'),
        (OP_WITHDRAW, 'Withdraw'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='operations')
    operation_type = models.CharField(max_length=8, choices=OPERATION_CHOICES)
    amount = models.DecimalField(max_digits=18, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
