import csv
from io import StringIO
from rest_framework.renderers import BaseRenderer

class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, accepted_media_type=None, renderer_context = None):
        """Renders queryset data into a CSV string."""
        if not data:
            return ""
        
        # Use a StringIO buffer to build the csv in memory
        string_buffer = StringIO()
        writer = csv.writer(string_buffer)

        # Assuming data is a list of dictionaries
        headers = data[0].keys()
        writer.writerow(headers)
        for item in data:
            writer.writerow(item.values())
        
        return string_buffer.getvalue()
