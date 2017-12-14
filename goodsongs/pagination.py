"""Pagination helpers."""

import json

from flask import current_app as app

from flask_mongoengine import BaseQuerySet


def get_pagination_params(request):
    """Return pagination params as keyword arguments on the view.

    Arguments:
        request -- an instance of flask request
    """
    default_per_page = app.config['DEFAULT_PER_PAGE']
    max_per_page = app.config['MAX_PER_PAGE']

    page = request.args.get('page')
    per_page = request.args.get('per_page')

    page = int(page) if page else 1
    per_page = int(per_page) if per_page else default_per_page
    per_page = min(per_page, max_per_page)

    return page, per_page


def paginate(data, page=1, per_page=None):
    """Create a paginated response of the given query set.

    Arguments:
        data -- A flask_mongoengine.BaseQuerySet instance
    """
    assert isinstance(data, BaseQuerySet)

    per_page = app.config['DEFAULT_PER_PAGE'] if not per_page else per_page
    pagination_obj = data.paginate(page=page, per_page=per_page)

    return {
        'data': build_pagination_data(pagination_obj),
        'meta': build_pagination_metadata(pagination_obj),
    }


def build_pagination_data(pagination_obj):
    """Assemble the pagination data."""
    pagination_data = []
    for item in pagination_obj.items:
        pagination_data.append(json.loads(item.to_json()))

    return pagination_data


def build_pagination_metadata(pagination_obj):
    """Assemble the pagination metadata."""
    pagination_metadata = {
        'current_page': pagination_obj.page,
        'total_pages': pagination_obj.pages,
    }
    if pagination_obj.has_prev:
        pagination_metadata['previous_page'] = pagination_obj.prev_num

    if pagination_obj.has_next:
        pagination_metadata['next_page'] = pagination_obj.next_num

    return pagination_metadata
