import csv
from django.views.generic import View
from django.http import HttpResponse


class ModelCSVExportView(View):
    """
    Export data in csv file
    """
    def __init__(self, serializer_class, model_class, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = serializer_class
        self.model_class = model_class

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        """
        Create csv file.

        Returns:
            return response with csv file.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="messages.csv"'

        serializer = self.get_serializer(
            self.model_class.objects.all(),
            many=True
        )
        header = self.serializer_class.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response
