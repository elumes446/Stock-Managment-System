from django import forms
from .models import Stock,StockHistory
from .models import Catagory

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['catagory', 'item_name' , 'quantity', 'date']
        
    def clean_catagory(self):
              catagory = self.cleaned_data.get('catagory')
              if not catagory:
                        raise forms.ValidationError("this field is required")
              return catagory 
    def clean_item_name(self):
              item_name = self.cleaned_data.get('item_name')
              if not item_name:
                        raise forms.ValidationError("this field is required")
              return item_name 

class StockSearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required =False)
    class Meta:
        model= Stock 
        fields =['catagory','item_name']



class StockUpdateForm(forms.ModelForm): 
    class Meta:
              model = Stock
              fields= ['catagory', 'item_name', 'quantity']



class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']
        
class ReceiveForm(forms.ModelForm):
    class Meta: 
        model = Stock
        fields = ['receive_quantity']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']


class StockHistorySearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required =False)
    start_date = forms.DateTimeField(required = False)
    end_date = forms.DateTimeField(required = False)
    class Meta: 
        model = StockHistory
        fields = ['catagory', 'item_name','start_date','end_date','export_to_csv']