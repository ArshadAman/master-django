import time
import csv
from django.http import StreamingHttpResponse

def csv_generator():
    """A generator function that yeilds CSV rows."""
    # Yeild the header row first
    yield ['Row Number', 'Timestamp']

    # Yield 10 data rows, simulating a slow process
    for i in range(1, 11):
        yield [i, f"{time.time():.4f}"]
        print(f"Generated row{i}")
        time.sleep(1) #simulate a delay, like a slow database query

class Echo:
    """An object that implements just the write method of the file like interface used to stream scv data directly to the respons"""

    def write(self, value):
        """Write the value by returning it."""
        return value

def stream_csv_view(request):
    """A view that streams a large csv file"""
    rows = csv_generator()
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    # The response is streaminghttpresponse with a generator

    response = StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type = "text/csv"
    )

    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response