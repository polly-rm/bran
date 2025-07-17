import os

from datetime import datetime

from django.conf import settings
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html
from weasyprint import HTML

from bran.invoices.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number',
                    'created',
                    'invoice_name',
                    'invoice_address',
                    'pdf_link']
    search_fields = ['invoice_number',
                     'created',
                     'invoice_name',
                     'invoice_address']

    def pdf_link(self, obj):
        if obj.pdf_file:
            filename = os.path.basename(obj.pdf_file.name)
            return format_html('<a href="{}" target="_blank">{}</a>', obj.pdf_file.url, filename)
        return "-"

    pdf_link.short_description = "PDF File"

    def get_changeform_initial_data(self, request):
        data = request.GET.dict()

        # List of datetime fields coming from GET
        datetime_fields = ['time_to_collect', 'time_to_deliver']

        for field in datetime_fields:
            value = data.get(field)
            if value:
                try:
                    # Try parsing format like '2025-07-19 15:18:00'
                    data[field] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    try:
                        # Try parsing with timezone like '2025-07-19 15:18:00+00:00'
                        data[field] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S%z')
                    except ValueError:
                        pass  # If all fails, keep as string (and it will cause a validation error)

        return data

    def save_model(self, request, obj, form, change):
        # Save the invoice to get its ID
        super().save_model(request, obj, form, change)

        # Generate the PDF
        image_path_logo = str(settings.BASE_DIR) + '/assets/img/logo-black.jpg'
        context = {'invoice': obj, 'logo_path': image_path_logo}
        html_string = render_to_string('invoices/invoice_pdf.html', context)

        # Define PDF output path
        output_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'invoice_{obj.invoice_number}.pdf')

        # Generate and save PDF
        HTML(string=html_string).write_pdf(output_path)

        # Save PDF path to model field
        obj.pdf_file = f'invoices/invoice_{obj.invoice_number}.pdf'
        obj.save()
