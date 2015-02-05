# -*- coding: utf-8 -*-
import os
import uuid
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

__author__ = 'pobear'


def filepath(instance, filename):
    model = type(instance).__name__.lower()
    f, ext = os.path.splitext(filename)
    return '%s/%s%s' % (model, uuid.uuid4().hex, ext)


class FieldsPlusPreparer(FieldsPreparer):
    def prepare(self, data):
        result = {}

        if not self.fields:
            return data

        for fieldname, lookup in self.fields.items():
            # 允许lookup为FieldsPreparer实例
            if isinstance(lookup, FieldsPlusPreparer):
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
                result[fieldname] = self.lookup_data(lookup, data)

        return result


class DjangoPlusResource(DjangoResource):
    limit_per_page = 20

    def serialize_list(self, data):
        if not hasattr(data, '__iter__'):
            return ''

        limit = int(self.request.GET.get('limit', self.limit_per_page))
        offset = int(self.request.GET.get('offset', 0))
        try:
            count = data.count()
        except (AttributeError, TypeError):
            count = len(data)

        self.request._paginator = {
            'limit': limit,
            'offset': offset,
            'total_count': count,
        }

        data = data[offset:offset + limit]

        return super(DjangoPlusResource, self).serialize_list(data)

    def wrap_list_response(self, data):
        response = super(DjangoPlusResource, self).wrap_list_response(data)
        response.update({
            'meta': self.request._paginator,
        })

        return response