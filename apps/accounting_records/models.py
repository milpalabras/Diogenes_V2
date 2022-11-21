from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import date
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Account (models.Model):
    '''Account model for save the accounts of the user'''
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)    
    class AccountType (models.TextChoices):
        GENERAL = 'GRAL', _('General')
        EFECTIVO ='EFEC', _('Efectivo')
        BANCARIA = 'BANC', _('Cuenta Bancaria')
        CREDITO = 'CRED', _('Tarjeta de Credito')
        AHORRO = 'AHOR', _('Cuenta de ahorros')
        EXTRA = 'EXTR', _('Extra')
        SEGURO = 'SEGU', _('Seguro')
        INVERSION = 'INVE', _('Inversión')
        PRESTAMO = 'PRES', _('Prestamo')
        HIPOTECA = 'HIPO', _('Hipoteca')
    account_type = models.CharField(max_length=4, choices=AccountType.choices, default=AccountType.GENERAL)
    amount= models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Cuentas"
        verbose_name="Cuenta"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category (MPTTModel):
    '''Category model for save the categories of the expense and income'''
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    parent = TreeForeignKey ('self', on_delete=models.CASCADE, related_name='children', 
        null=True, blank=True, related_query_name='subcategoria')
    class CategoryType (models.TextChoices):
        FIJO ='F', _('Gasto Fijo(Obligatorio)')
        NECESIDAD = 'N', _('Gasto Necesario(Sobrevivencia)')
        PRESCINDIBLE = 'P',_('Gasto Prescindible(Lujo)')
        INGRESO = 'I',_('Ingreso de dinero')
        PADRE = 'C',_('Categoria Padre (admin)')    
    category_type = models.CharField(max_length=1, choices=CategoryType.choices, default=CategoryType.FIJO)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class MPTTMeta:
        order_insertion_by=['name']

    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name = "Categoria"
        ordering = ['name']

    def __str__(self):
        return self.name


class MethodOfPayment (models.Model):
    '''Method of payment model for save the methods of payment of the user'''
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural="Forma de pagos"
        verbose_name="Forma de pago"        

    def __str__(self):
        return self.name


class Records(models.Model):
    '''Records model for save the records of income and expense by user'''
    owner = models.ForeignKey(User,related_name='records', on_delete=models.CASCADE)
    class RecordType (models.TextChoices):
        GASTO = 'GAST', _('Gasto')
        INGRESO ='INGR', _('Ingreso')
        TRANSFERENCIA = 'TRAN', _('Transferencia')
    record_type = models.CharField(max_length=4, choices=RecordType.choices, default=RecordType.GASTO)
    amount = models.DecimalField(max_digits=15,  decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    note = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField(default=date.today)
    category_id = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    account_id = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
    method_of_payment_id = models.ForeignKey('MethodOfPayment', on_delete=models.CASCADE, null=True, blank=True)    
    voucher = models.FileField(upload_to='vouchers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Registros"
        verbose_name = "Registro"
        ordering = ['payment_date']

    def save(self, *args, **kwargs):
        account= Account.objects.get(id=self.account_id.id)        
        if self.record_type == 'GAST':
            account.amount -= self.amount
        elif self.record_type == 'INGR':
            account.amount += self.amount
        account.save()
        super(Records, self).save(*args, **kwargs)
    
    #make delete method to update the account amount
    def delete(self, *args, **kwargs):
        account= Account.objects.get(id=self.account_id.id)        
        if self.record_type == 'GAST':
            account.amount += self.amount
        elif self.record_type == 'INGR':
            account.amount -= self.amount
        account.save()
        super(Records, self).delete(*args, **kwargs)
    
    #make update method to update the account amount
    def update(self, *args, **kwargs):
        account= Account.objects.get(id=self.account_id.id)
        old_amount = Records.objects.get(id=self.id).amount

        if self.record_type == 'GAST':
            if old_amount > self.amount:
                account.amount += old_amount - self.amount
            elif old_amount < self.amount:
                account.amount -= self.amount - old_amount
        elif self.record_type == 'INGR':
            if old_amount > self.amount:
                account.amount -= old_amount - self.amount
            elif old_amount < self.amount:
                account.amount += self.amount - old_amount
        account.save()
        super(Records, self).update(*args, **kwargs)
            
    def __str__(self):
        return self.get_record_type_display() + " - " + str(self.amount) + " - " + str(self.payment_date)
    
    @property
    def get_comprobante(self):
        return self.voucher.url