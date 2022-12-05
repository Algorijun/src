from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
from .utils import get_customer_from_id, get_sales_from_id, get_chart
from reports.forms import ReportForm



# Create your views here.
def home_view(request):

    # function view.
    # fuuntion view vs class view ?
    # function view is more readalbe for me?

    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    search_form = SalesSearchForm(request.POST or None) # if or None doesn't exist, It says annoying texts ""
    report_form = ReportForm()
    chart = None
    no_data = None
    #hello = 'hello world from the view'
    
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            position_data = []
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_sales_from_id)
            # strftime (??)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({
                            'customer_id' : 'customer',
                            'salesman_id' : 'salesman',
                            'id' : 'sales_id',
            }
            , axis=1 , inplace=True)
            # What if 
            #sales_df['sales_id'] = sales_df['id']

            
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id' : pos.id,
                        'product' : pos.product.name,
                        'quantity' : pos.quantity,
                        'price' : pos.price,
                        'sales_id' : pos.get_sales_id(),

                    }
                    position_data.append(obj)

            positions_df = pd.DataFrame(position_data)    
            merged_df = pd.merge(sales_df,positions_df, on = 'sales_id')
            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

#            chart = get_chart(chart_type, df, labels=df['transaction_id'].values)
            chart = get_chart(chart_type, sales_df, results_by)

            #print("This is how  chart looks like")
            #print(chart) 
            # We see bunch of random looks like chars.... 
            # 

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()            

            
            
            print(sales_df)
            print(position_data)
        else:
            no_data = "No data available at this range!"

        #qs = Sale.objects.filter(created__date = date_from)
        #obj = Sale.objects.get(id=1)
        

    context = {
        'search_form'  : search_form,
        'report_form'  : report_form,
        'sales_df' : sales_df,
        'positions_df' : positions_df,
        'merged_df' : merged_df,
        'df' : df,
        'chart' : chart,
        'no_data' : no_data
    }
                                            # dictionary key should match with... the element in html
    return render(request, 'sales/home.html', context) # template name and dictionary

# inherit from ListView of django
class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'  
    #context_object_name = 'qs' # we are going to use 'qs' as object_list in the html file.
 

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'  