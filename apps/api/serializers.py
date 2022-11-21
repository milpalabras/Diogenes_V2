from rest_framework import serializers
from ..accounting_records.models import Records, Category, MethodOfPayment, Account

class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Account
        fields = ('id', 'name', 'account_type', 'amount','created_at', 'updated_at', 'owner')

class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Category
        fields = ('id', 'name', 'category_type', 'parent', 'created_at', 'updated_at', 'owner')

class MethodOfPaymentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = MethodOfPayment
        fields = ('id', 'name','owner')

class RecordsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Records
        fields = ('id', 'record_type', 'amount', 'note', 'payment_date', 
        'category_id', 'account_id','method_of_payment_id', 'owner')