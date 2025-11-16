from rest_framework import serializers
from .models import *


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'



class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['id', 'part_no', 'quantity', 'purchase_price', 'total_price']



class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)

    class Meta:
        model = Purchase
        fields = [
            'id',
            'invoice_no',
            'purchase_date',
            'exporter_name',
            'company_name',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)

        for item in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item)

        return purchase

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        
        # Update main purchase fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Track existing items
        existing_item_ids = [item.id for item in instance.items.all()]
        new_item_ids = []

        # Update or create items
        for item in items_data:
            item_id = item.get('id', None)

            # Existing -> update
            if item_id and item_id in existing_item_ids:
                purchase_item = PurchaseItem.objects.get(id=item_id, purchase=instance)
                for attr, value in item.items():
                    setattr(purchase_item, attr, value)
                purchase_item.save()
                new_item_ids.append(item_id)
            
            # New -> create
            else:
                new_item = PurchaseItem.objects.create(purchase=instance, **item)
                new_item_ids.append(new_item.id)

        # Delete removed items
        for old_item in instance.items.all():
            if old_item.id not in new_item_ids:
                old_item.delete()

        return instance




class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'



class IncomeSrializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'



class CombinedPurchaseSerializer(serializers.Serializer):
    date = serializers.DateField()
    invoice_no = serializers.CharField()
    part_no = serializers.CharField()
    product_name = serializers.CharField()
    supplier_or_exporter = serializers.CharField()
    quantity = serializers.IntegerField()
    purchase_amount = serializers.DecimalField(max_digits=12, decimal_places=2)