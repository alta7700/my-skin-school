from tickets.forms import TicketForm


class BaseContextMixin:

    title: str = ''
    need_ticket_form = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.need_ticket_form:
            context['ticket_form'] = TicketForm()
        context['title'] = self.get_title()
        context['navbar_history'] = self.get_navbar_history(**kwargs)
        return context

    def get_navbar_history(self, **kwargs) -> dict[str, str]:
        return {}

    def get_title(self) -> str:
        return self.title
