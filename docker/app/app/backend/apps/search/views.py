"""
    search.views
    ============

    Here we choose a function based views for the simplicity / efficiency
"""
import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import utils

logger = logging.getLogger('project_logger')


@api_view(['GET'])
def autosuggest_view(request):
    """ Autocompletes query using Redis. """
    q = request.GET.get('q', "")
    logger.debug("autosuggest_view, query: %s" % q)
    return Response(utils.autocomplete_suggestion(q, 10))


@api_view(['GET'])
def search_view(request):
    """ Searchs Redis based on query. """
    q = request.GET.get('q', "")
    logger.debug("search_view, query: %s" % q)
    return Response(utils.search_redis(q, 25))
