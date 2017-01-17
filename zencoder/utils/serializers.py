

class PlaceholderFieldsMixin(object):
    """Allow placeholder fields to be set by SerializerCls.Meta.placeholder_fields

    assignment should adhere to the following pattern e.g.,
    class Meta:
        placeholder_fields = {
            field_name: placeholder_value
        }
    """

    def to_representation(self, obj):
        data = super(PlaceholderFieldsMixin, self).to_representation(obj)
        # Check for conflicts & prioritize pre-existing values to placeholders.
        meta = getattr(self, "Meta", None)
        placeholder_fields = getattr(meta, "placeholder_fields", {})
        for key, value in placeholder_fields.items():
            if key not in data:
                data[key] = value
        return data
