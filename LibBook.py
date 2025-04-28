"""
Library Book Management System

Design a system that allows users to check out, return and search for books in library.
The system should keep track of book availability and allow efficient retrieval. 

Data Strucutres Used: Linked List, Heap/Priority Queue
"""

from collections import deque

# --- Book Class ---
class Book:
    def __init__(self, title, author, isbn, category):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.category = category
        self.is_available = True
        self.reservation_queue = deque() # Queue of users
        
        

# --- Linked List Node for User History ---

# --- User Class ---

# --- Library System Class ---