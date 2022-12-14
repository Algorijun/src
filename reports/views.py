from django.shortcuts import render , get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



# Create your views here.


class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'


def csv_upload_view(request):
    return HttpResponse()


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def create_report_view(request):
    # is_ajax() is deprecated ... so change it like that
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Home.js / fomrData 
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        print(request)
        img = get_report_image(image)

        author = Profile.objects.get(user = request.user)


        # That's how we make objects and store it to DB.
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)

        return JsonResponse({'msg': 'send'})
    return JsonResponse({})

def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'

    obj = get_object_or_404(Report, pk=pk)


    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')


    # if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display

    #
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response