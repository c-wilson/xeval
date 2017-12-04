"""
Storage module

This module encapsulates a (very) basic database implementation, with the idea that the interface can be
reused with a more robust and efficient transactional DB.

The main class here is SimpleStore, which serves as a database interface.
"""

from . import exceptions
import numpy as np
from typing import List

FEATURES = ('reach', 'clarity')  # "features" that the database needs to know about.


class SimpleStore:
    """
    This is the database interface. The underlying data structure is a Python dictionary, and so it is
    optimized (O(1)) to look up by only one attribute: "reputee". Other search/filter functions can be added
    at great performance penalty (O(n), where n is number of transactions); this should be migrated to SQL
    if that functionality is desired.
    """

    def __init__(self):
        self._data_by_reputee = {}

    def get_reputee(self, reputee_name: str):
        """
        Returns reputee model for a given name
        :return: ReputeeModel
        """

        try:
            reputee = self._data_by_reputee[reputee_name]
        except KeyError:
            raise exceptions.ReputeeNotFoundError()
        return reputee

    def add_transaction(self, data):
        """
        Add transaction to re

        Automatically adds reputee's if they are not already in the table.

        :param data:
        :return:
        """
        reputee_name = data['reputee']
        if reputee_name not in self._data_by_reputee.keys():
            reputee = ReputeeModel(reputee_name)
            self._data_by_reputee[reputee_name] = reputee
        else:
            reputee = self._data_by_reputee[reputee_name]  # type: ReputeeModel
        reputee.add_data(data)

    def get_rep_values(self, reputee_name: str, feature_name: str):
        """

        :param reputee_name:
        :param feature_name:
        :return:
        """

        reputee = self.get_reputee(reputee_name)  # type: ReputeeModel
        entries = reputee.entries[feature_name]  # type: List[EntryModel]
        values = np.zeros(len(entries))
        for i, e in enumerate(entries):
            values[i] = e.repute_value
        return values


class ReputeeModel:
    """
    Container for reputee information.

    Reputation information is stored in a python Dict which holds lists of entries by

    """
    def __init__(self, name):
        self.name = name
        self.entries = {}  # entries are kept separate by feature.
        self._rids = {}  # storage for unique txn identifier; uses hashing so it's a bit faster:
        for featurename in FEATURES:
            self.entries[featurename] = []
            self._rids[featurename] = set()
        # self.reputation = {} # "cached" reputation calculated
        # state of reputation attribute-set True when txn added and reputation not updated
        # self.stale = True

    def add_data(self, data: dict):
        """
        Adds an transaction entry to the model after checking for RID duplication.

        I'm assuming that the behavior we'd want here is to only add_data txns to the database if the rid does
        not already exist for the database. NOTE this is not verbose - duplicate RIDs will just not be added
        with no user feedback, although this can be changed.

        :param data:
        :return:
        """

        feature = data['repute']['feature']
        rid = data['repute']['rid']
        if rid not in self._rids[feature]:
            self._rids[feature].add(rid)
            entry = EntryModel(data)
            self.entries[feature].append(entry)
        else:
            raise exceptions.RidDuplicateError

    def filter_entries(self, feature_name):
        """

        :param feature_name:
        :return:
        """



class EntryModel:
    def __init__(self, data):
        self.reputer = data['reputer']
        self.reputee = data['reputee']
        self.repute_rid = data['repute']['rid']
        self.repute_feature = data['repute']['feature']
        self.repute_value =  float(data['repute']['value'])
