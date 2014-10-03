from django.utils.translation import ugettext as _
from django.http import HttpResponse

import csv

CSV_FILE = 'exported_data.csv'


def export_csv_action(view, queryset):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(CSV_FILE)

    writer = csv.writer(response)

    for item in queryset:
        row = []
        for var in vars(item):
            row.append(item.__getattribute__(var))
        writer.writerow(row)

    return response

export_csv_action.short_description = _('export items to CSV')
