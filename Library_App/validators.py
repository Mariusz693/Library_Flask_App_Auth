from datetime import datetime
from wtforms.validators import ValidationError


class EqualDateTo:
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError as exc:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            ) from exc
        if field.data > other.data:
            return

        d = {
            "other_label": hasattr(other, "label")
            and other.label.text
            or self.fieldname,
            "other_name": self.fieldname,
        }
        message = self.message
        if message is None:
            message = field.gettext("Field must be equal to %(other_name)s.")

        raise ValidationError(message % d)


class DateRange:
    """
    Validates that a date is under of today value.

    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(max)s` if desired..

    When supported, sets the `max` attributes on widgets.
    """
    def __init__(self, message=None):
        self.max = datetime.now().date()
        self.message = message
        self.field_flags = {}
        if self.max is not None:
            self.field_flags["max"] = self.max

    def __call__(self, form, field):
        data = field.data
        if data is not None and data <= self.max:
            return

        if self.message is not None:
            message = self.message

        else:
            message = field.gettext("Date must be under %(max)s.")

        raise ValidationError(message % dict(max=self.max))
