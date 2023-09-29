from django.shortcuts import render ,redirect
from django.http import HttpResponse
import csv
from .models import Stock
from .models import Catagory
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.
# creating the default page in the web 
def home(request):
    title= "Welcome : this is the home page"
    form = "Welcome : this is the dsdsdhome page"
    context = {
        "title" : title,
        "test" : form,
        
    }
    return redirect('/list_items')
    #return render(request, "home.html",context)
 
def list_items(request):
    header = "List of Itmes"
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "Header": header,
        "queryset": queryset,
        "form": form,
    }
    #---------- code for filter--------------
    if request.method =="POST":
        queryset = Stock.objects.filter(#catagory__icontains=form['catagory'].value(),
                                       item_name__icontains=form['item_name'].value(),
                                       )
        if form['export_to_csv'].value() == True:
                  response = HttpResponse(content_type = 'text/csv')
                  response ['Content-Disposition']='attachement; filename= "List_of_Stock.csv"'
                  writer = csv.writer (response)
                  writer.writerow(['CATAGORY','ITEM NAME', 'QUNATITY IN STORE','STAMP DATE','UPDATED_DATE','VERIFIED_DATE'])
                  instance = queryset
                  for stock in instance:
                            writer.writerow([stock.catagory, stock.item_name, stock.quantity,stock.time_stamp,stock.last_updated,stock.date])
                  return response
        context={
            'form': form,
            'Header': header,
            'queryset':queryset,
        }
    return render(request, "List_items.html",context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,'Added Succsesfully')
        return redirect('add_items')
    context = {
        "form": form,
        "title": "Add Item"
    }
    return render(request, "add_items.html", context)



def update_items(request, pk):
          queryset= Stock.objects.get(id=pk)
          form= StockUpdateForm(instance = queryset)
          
          if request.method == 'POST':
                    form = StockUpdateForm(request.POST,instance=queryset)
                    if form.is_valid():
                              form.save()
                              messages.success(request,'Update Succsesfully')
                              return redirect('/list_items')
          context= {
              'form' : form
          }
          
          return render(request, 'add_items.html', context)

def delete_items (request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method =="POST":
        queryset.delete()
        messages.success(request, 'Deleted Succsesfully')
        return redirect('/list_items')
    return render(request, 'delete_items.html')


def stock_detail(request, pk):
    queryset =  Stock.objects.get(id=pk)
    context = {
        "queryset":queryset,
    }
    return render(request,"stock_detail.html",context)



def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid(): 
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request,"Issued Successfullu"+ str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        
        return redirect('/stock_detail/'+ str(instance.id))
    context = {
        "title": "Issue" + str(queryset.item_name),
        "instance":queryset,
        "form":form,
        'user_name': "Issue By:" + str(request.user)
    }
    return render(request, 'add_items.html',context)
 
        
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request,"Received Successfullu"+ str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        return redirect('/stock_detail/'+ str(instance.id))
    context = {
        "title": "Receive " + str(queryset.item_name),
        "instance":queryset,
        "form":form,
        'user_name': "Received_by:" + str(request.user)
    }
    return render(request, 'add_items.html',context)


def reorder_level (request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance= form.save(commit=False)
        instance.save()
        messages.success(request,"Reorder level for"+str(instance.item_name)+"is Updated to"+str(instance.reorder_level))
        return redirect("/list_items")
    context={
        "instance":queryset,
        "form": form 
    }
    
    return render (request, "add_items.html",context)


def list_history(request):
    header = "History of Items"
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "Header": header,
        "queryset": queryset,
        'form': form,
    }
    if request.method =="POST":
        catagory = form ['catagory'].value()
        queryset = Stock.objects.filter(#catagory__icontains=form['catagory'].value(),
                                       item_name__icontains=form['item_name'].value(),
                                       last_updated__range=[
                                           form['start_date'].value(),
                                           form['end_date'].value()
                                       ]
                                       )
        
        if (catagory != ''):
                  queryset = queryset.filter(catagory_id=catagory)
                  
                  
        if form['export_to_csv'].value() == True:
                response = HttpResponse(content_type = 'text/csv')
                response ['Content-Disposition']='attachement; filename= "List_of_Stock.csv"'
                writer = csv.writer (response)
                writer.writerow(['CATAGORY','ITEM NAME', 'QUNATITY','ISSUE QUANTITY','RECEIVE QUANTITY','RECEIVE BY','ISSUE BY','LAST UPDATED'])
                instance = queryset
                for stock in instance:
                    writer.writerow([stock.catagory, stock.item_name, stock.quantity,stock.issue_quantity,stock.receive_quantity,stock.receive_by,stock.issue_to,stock.last_updated])
                return response
            
        context = {
        'Header' : header,
        'form': form,
        'queryset': queryset,
    }
    return render (request, "list_history.html",context)