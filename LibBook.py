"""
Library Book Management System

Design a system that allows users to check out, return and search for books in library.
The system should keep track of book availability and allow efficient retrieval. 

Data Strucutres Used: Linked List, Heap/Priority Queue
"""

import heapq

# --- Book Class ---
class Book:
    def __init__(self, title, author, dewey_decimal):
        self.title = title
        self.author = author
        self.dewey_decimal = dewey_decimal
        self.is_available = True
        self.reservation_queue = [] # prio queue of (prio, username)

    def reserve_book(self, username, prioprity=0):
        heapq.heappush(self.reservation_queue, (priority, username))

    def next_reservation(self):
        if self.reservation_queue:
            return heapq.heappop(self.rservation_queue)
        return None

# --- Linked List Node for User History ---

# --- User Class ---

# --- Library System Class ---