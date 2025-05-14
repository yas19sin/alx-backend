#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Return a dictionary with key-value pairs for deletion-resilient
        hypermedia pagination.

        Args:
            index (int, optional): The current start index. Defaults to None,
                                   which will be treated as 0.
            page_size (int, optional): The current page size. Defaults to 10.

        Returns:
            Dict: A dictionary with pagination information.
        """
        indexed_dataset = self.indexed_dataset()
        # If index is None, set it to 0
        if index is None:
            index = 0
        # Verify that index is in a valid range
        assert isinstance(index, int) and 0 <= index < len(indexed_dataset)
        # Initialize variables
        data = []
        next_index = index
        count = 0
        # Get data for the current page
        while count < page_size and next_index < len(indexed_dataset):
            if next_index in indexed_dataset:
                data.append(indexed_dataset[next_index])
                count += 1
            next_index += 1
        # Return dictionary with the required key-value pairs
        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': data
        }
