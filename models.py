from django.db import models

catagory_choice = (
    ('Furniture', 'Furniture'),
    ('IT Equipment', 'IT Equipment'),
    ('Electronic', 'Electronic'),
    ('Phone', 'Phone'),
)

class Catagory(models.Model):
    name=models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name


class Stock(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, blank=True)
    #catagory=models.CharField(max_length=50, blank=True, null=True, choices=catagory_choice)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    time_stamp = models.DateTimeField(auto_now_add= True , auto_now=False, blank=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    #export_to_CSV = models.BooleanField(default=False)

class StockHistory(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE,blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    time_stamp = models.DateTimeField(auto_now_add= False , auto_now=False, null=True)
          
