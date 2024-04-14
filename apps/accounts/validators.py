from rest_framework.exceptions import ValidationError

from apps.accounts.choices import State, UserField

class ChoiceFieldsValidator:
    """
    These functions manually validate fields instead of relying on the 
    default `ChoiceField` with the `choices` argument.

    The reason behind this is to address challenges encountered by the 
    frontend dev sending data as required. Because, sometimes we all
    encounter little skill issues & tackling them as a team is part of the fun.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_user_field_choices = set(choice for tuples in UserField.choices for choice in tuples)
        self.valid_state_choices = set(choice for tuples in State.choices for choice in tuples)

    def validate_user_field(self, obj):

        user_field = obj.lower().split(' ')
        user_field = "-".join(user_field)

        if user_field not in self.valid_user_field_choices:
            raise ValidationError(f'"{obj}" is not a valid choice.')

        return user_field
    
    def validate_state(self, obj):
        state = obj.lower().split(' ')
        state = "-".join(state)

        if state not in self.valid_state_choices:
            raise ValidationError(f'"{obj}" is not a valid choice.')

        return state