from django.db import models
from django.contrib.auth import get_user_model


class ECH(models.Model):
  """Order Header file"""
  HORD = models.AutoField(primary_key=True, db_column='HORD',\
                          verbose_name='Order Number')
  HCUST = models.ForeignKey(get_user_model(), to_field='id', db_column='HCUST',\
                            on_delete=models.CASCADE, verbose_name='Customer No', \
                            related_name= 'Cust')
  HSHOP = models.ForeignKey(get_user_model(), to_field='id', db_column='HSHOP', \
                            on_delete=models.CASCADE, verbose_name='Shop No', \
                            related_name= 'Shop')  
  HSNME = models.CharField(max_length= 30, db_column= 'HSNME', verbose_name='Shop Name')
  HEDTE = models.DateField(db_column='HEDTE', verbose_name='Entered Date')
  
  status = (('ONGOING', 'ONGOING'),
            ('CANCELLED', 'CANCELLED'),
            ('COMPLETED', 'COMPLETED'))
  HSTS = models.CharField(max_length= 10, choices= status, db_column='HSTS', \
                          verbose_name='Order Status')

  class Meta:
    verbose_name_plural = 'ECH'

  def __str__(self):
    return str(self.HORD)


class ECL(models.Model):
  """Order Line details file"""
  LORD = models.ForeignKey(ECH, to_field='HORD', db_column= 'LORD', \
                           verbose_name= 'Order Number', on_delete= models.CASCADE)
  LLINE = models.DecimalField(max_digits=3, decimal_places= 0, \
                              db_column='LLINE', verbose_name='Line number')
  LPROD = models.CharField(max_length=200, db_column='LPROD', verbose_name='Item')
  LQORD = models.DecimalField(max_digits=3, decimal_places= 0, \
                              db_column='LQORD', verbose_name= 'Ordered Quantity')
  LPRIC = models.DecimalField(max_digits=6, decimal_places= 2, \
                             db_column= 'LPRIC', verbose_name= 'Price')
  LDISC = models.DecimalField(max_digits=6, decimal_places= 2, \
                              db_column= 'LDISC', verbose_name= 'Discount')
  class Meta:
    verbose_name_plural = 'ECL'

  def __str__(self):
    return str(self.LORD)
  


