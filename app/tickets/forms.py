from django.forms import ModelForm
from django.forms.utils import ErrorList

from tickets.models import Ticket


class TicketForm(ModelForm):

    class Meta:
        model = Ticket
        fields = ('first_name', 'email', 'phone', 'theme', 'message')

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            instance=None,
            use_required_attribute=None,
            renderer=None,
    ):
        super().__init__(
            data=data,
            files=files,
            auto_id=auto_id,
            prefix=prefix,
            initial=initial,
            error_class=error_class,
            label_suffix=label_suffix,
            empty_permitted=empty_permitted,
            instance=instance,
            use_required_attribute=use_required_attribute,
            renderer=renderer,
        )
        for visible in self.visible_fields():
            attrs = visible.field.widget.attrs
            attrs['class'] = 'footer-input'
            attrs['placeholder'] = visible.field.label
