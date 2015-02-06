# -*- coding: utf-8 -*-
try:
    from django.db.models import QuerySet, FieldDoesNotExist
    from django.db.models.fields.related import RelatedField
except ImportError:
    QuerySet = None
    FieldDoesNotExist = None


class Preparer(object):
    """
    A plain preparation object which just passes through data.

    It also is relevant as the protocol subclasses should implement to work with
    Restless.
    """
    def __init__(self):
        super(Preparer, self).__init__()

    def prepare(self, data):
        """
        Handles actually transforming the data.

        By default, this does nothing & simply returns the data passed to it.
        """
        return data


class FieldsPreparer(Preparer):
    """
    A more complex preparation object, this will return a given set of fields.

    This takes a ``fields`` parameter, which should be a dictionary of
    keys (fieldnames to expose to the user) & values (a dotted lookup path to
    the desired attribute/key on the object).

    Example::

        preparer = FieldsPreparer(fields={
            # ``user`` is the key the client will see.
            # ``author.pk`` is the dotted path lookup ``FieldsPreparer``
            # will traverse on the data to return a value.
            'user': 'author.pk',
        })

    """
    def __init__(self, fields):
        super(FieldsPreparer, self).__init__()
        self.fields = fields

    def prepare(self, data):
        """
        Handles transforming the provided data into the fielded data that should
        be exposed to the end user.

        Uses the ``lookup_data`` method to traverse dotted paths.

        Returns a dictionary of data as the response.
        """
        result = {}

        if not self.fields:
            return data

        for fieldname, lookup in self.fields.items():
            # 允许lookup为FieldsPreparer实例
            if isinstance(lookup, FieldsPreparer):
                preparer = lookup

                sub_data = None
                if hasattr(data, fieldname):
                    sub_data = getattr(data, fieldname)

                if sub_data is not None:
                    # 特殊处理数组
                    if hasattr(sub_data, '__iter__'):
                        sub_result = []
                        for sd in sub_data:
                            sub_result.append(preparer.prepare(sd))
                    else:
                        sub_result = preparer.prepare(sub_data)

                    result[fieldname] = sub_result
            else:
                if lookup.endswith('?'):
                    lookup = lookup[:-1]
                    try:
                        result[fieldname] = self.lookup_data(lookup, data)
                    except AttributeError:
                        pass
                else:
                    result[fieldname] = self.lookup_data(lookup, data)

        return result

    def optimize_django_query(self, data):
        if not QuerySet:
            return data

        if isinstance(data, QuerySet):
            only_fields = []
            for fieldname, lookup in self.fields.items():
                if isinstance(lookup, FieldsPreparer):
                    pass
                else:
                    model = data.model
                    keys = []
                    for key in lookup.split('.'):
                        try:
                            field = model._meta.get_field_by_name(key)[0]
                            keys.append(key)
                            if isinstance(field, RelatedField):
                                pass

                        except FieldDoesNotExist:
                            pass

        return data

    def lookup_data(self, lookup, data):
        """
        Given a lookup string, attempts to descend through nested data looking for
        the value.

        Can work with either dictionary-alikes or objects (or any combination of
        those).

        Lookups should be a string. If it is a dotted path, it will be split on
        ``.`` & it will traverse through to find the final value. If not, it will
        simply attempt to find either a key or attribute of that name & return it.

        Example::

            >>> data = {
            ...     'type': 'message',
            ...     'greeting': {
            ...         'en': 'hello',
            ...         'fr': 'bonjour',
            ...         'es': 'hola',
            ...     },
            ...     'person': Person(
            ...         name='daniel'
            ...     )
            ... }
            >>> lookup_data('type', data)
            'message'
            >>> lookup_data('greeting.en', data)
            'hello'
            >>> lookup_data('person.name', data)
            'daniel'

        """
        value = data
        parts = lookup.split('.')

        if not parts or not parts[0]:
            return value

        part = parts[0]
        remaining_lookup = '.'.join(parts[1:])

        if hasattr(data, 'keys') and hasattr(data, '__getitem__'):
            # Dictionary enough for us.
            value = data[part]
        elif data is not None:
            # Assume it's an object.
            value = getattr(data, part)

        # 支持方法或者函数的值的获取
        if hasattr(value, '__call__'):
            value = value()

        if not remaining_lookup:
            return value

        # There's more to lookup, so dive in recursively.
        return self.lookup_data(remaining_lookup, value)