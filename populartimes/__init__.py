#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .crawler import run
from .crawler import get_populartimes
from .crawler import get_populartimes_from_search as internal_get_populartimes_from_search
from .crawler import get_data_from_search as internal_get_data_from_search
from .crawler import get_popularity_for_day

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

"""

ENTRY POINT

"""


def get(api_key, types, p1, p2, n_threads=20, radius=180, all_places=False):
    """
    :param api_key: str; api key from google places web service
    :param types: [str]; placetypes
    :param p1: (float, float); lat/lng of a delimiting point
    :param p2: (float, float); lat/lng of a delimiting point
    :param n_threads: int; number of threads to use
    :param radius: int; meters;
    :param all_places: bool; include/exclude places without populartimes
    :return: see readme
    """
    params = {
        "API_key": api_key,
        "radius": radius,
        "type": types,
        "n_threads": n_threads,
        "all_places": all_places,
        "bounds": {
            "lower": {
                "lat": min(p1[0], p2[0]),
                "lng": min(p1[1], p2[1])
            },
            "upper": {
                "lat": max(p1[0], p2[0]),
                "lng": max(p1[1], p2[1])
            }
        }
    }

    return run(params)


def get_id(api_key, place_id):
    """
    retrieves the current popularity for a given place
    :param api_key:
    :param place_id:
    :return: see readme
    """
    return get_populartimes(api_key, place_id)

def get_populartimes_from_search(place_identifier, proxy_host=False):
    """
    retrieves popular times based on place identifier
    :param place_identifier:
    :return: see readme
    """
    rating, rating_n, popularity, current_popularity, time_spent = internal_get_populartimes_from_search(place_identifier, proxy_host)

    to_return = {}
    to_return['rating'] = rating
    to_return['rating_n'] = rating_n
    to_return['current_popularity'] = current_popularity
    to_return['time_spend'] = time_spent

    if popularity is not None:
        popularity, wait_times = get_popularity_for_day(popularity)

        to_return['popularity'] = popularity
        to_return['wait_times'] = wait_times

    return to_return

def get_data_from_search(place_identifier, proxy_host=False):
    """
    retrieves popular times based on place identifier
    :param place_identifier:
    :return: see readme
    """
    to_return = internal_get_data_from_search(place_identifier, proxy_host)

    if to_return['popular_times'] is not None:
        popularity, wait_times = get_popularity_for_day(to_return['popular_times'])

        to_return['popularity'] = popularity
        to_return['wait_times'] = wait_times
        to_return.pop('popular_times', None)

    return to_return
