from django.http import HttpResponse

from tickets.forms import TicketForm


def add_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200, content='OK')
    return HttpResponse(status=400, content='Bad request')
