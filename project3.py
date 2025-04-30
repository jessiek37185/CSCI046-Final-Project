"""
Library Book Management System

Design a system that allows users to check out, return and search for books in library.
The system keeps track of book availability and allow efficient retrieval. 

Data Strucutres Used: Linked List, Hashmap, Queue
"""
# --- Book Class --- 
class Book:
    def __init__(self, isbn, title, author, category):
        # basic book info
        self.isbn = isbn
        self.title = title
        self.author = author
        self.category = category
        self.available = True
        self.reservation_queue = ReservationBST() # Use BST for prio

    # enqueue a user to reserve the book
    def reserve_book(self, user):
        self.reservation_queue.insert(user)
        if user.get_priority_level() == 1:
            print(f"🧑‍🏫 {user.name} has been added to the **front** of the reservation queue because they are a professor.")
        else:
            print(f"{user.name} has been added to the reservation queue.")

    # dequeue the next user waiting for book
    def next_in_queue(self):
        return self.reservation_queue.extract_min()
    
    def show_reservation_queue(self):
        queue = self.reservation_queue.get_queue()
        if not queue:
            print("No one is currently in the reservation queue.")
        else:
            print("📋 Reservation Queue:")
            for i, (name, role) in enumerate(queue, 1):
                print(f"  {i}. {name} ({role})")

# --- Linked List Node for Borrowing History ---
class LinkedListNode:
    def __init__(self, book):
        self.book = book
        self.next = None

# --- Borrowing History (Linked List) ---
class BorrowHistory:
    def __init__(self):
        self.head = None

    # Add a book to the end of user's borrowing history 
    def add_book(self, book):
        new_node = LinkedListNode(book)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # Print the borrowing history
    def print_history(self):
        current = self.head
        if not current:
            print("No borrowing history.")
            return
        idx = 1
        while current:
            print(f"{idx}.{current.book.title} by {current.book.author}")
            current = current.next
            idx += 1

import time
# --- User Class (BST) --- 
class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.borrow_history = BorrowHistory()
        self.timestamp = time.time() #reservation request time

    def get_priority_level(self):
        # lower value = higher prio
        role_prio = {"professor": 1, "graduate": 2, "undergraduate": 3}
        return role_prio.get(self.role, 4) # default prio = 4
    
class BSTNode:
    def __init__(self,key,user):
        self.key = key # (prio_level, timestamp)
        self.user = user
        self.left = None
        self.right = None

class ReservationBST:
    def __init__(self):
        self.root = None
    
    def insert(self, user):
        key = (user.get_priority_level(), user.timestamp)
        self.root = self._insert(self.root, key, user)

    def _insert(self, node, key, user):
        if node is None:
            return BSTNode(key, user)
        if key < node.key:
            node.left = self._insert(node.left, key, user)
        else:
            node.right = self._insert(node.right, key, user)
        return node 

    def extract_min(self):
        if self.root is None:
            return None
        self.root, min_node = self._extract_min(self.root)
        return min_node.user
    
    def _extract_min(self, node):
        if node.left is None:
            return (node.right, node)
        node.left, min_node = self._extract_min(node.left)
        return (node, min_node)

    def is_empty(self):
        return self.root is None
    

    def get_queue(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.user.name, node.user.role))
            self._inorder(node.right, result)

# --- Queue Node Class ---
class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

# --- Queue Class ---
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    # enqueue data at the end
    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    # dequeue data from the front
    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    # check if queue is empty
    def is_empty(self):
        return self.front is None


# --- Library System ---
class Library:
    def __init__(self):
        self.books = {}  # HashMap: isbn -> Book
        self.users = {}  # HashMap: user_id -> User

    # Add book to the library
    def add_book(self, isbn, title, author, category):
        if isbn not in self.books:
            self.books[isbn] = Book(isbn, title, author, category)
            print(f"Added book: {title}.")
        else:
            print("Book with this ISBN already exists.")

    # Add a new user to the library system
    def add_user(self, user_id, name, role):
        if user_id not in self.users:
            self.users[user_id] = User(user_id, name, role)
            print(f"User {name} added.")
        else:
            print("User already exists.")

    # Search book by title, author, ISBN, or category
    def search_books(self, keyword):
        results = []
        for book in self.books.values():
            if (keyword.lower() in book.title.lower() or
                keyword.lower() in book.author.lower() or
                keyword.lower() in book.category.lower() or
                keyword.lower() == book.isbn.lower()):
                results.append(book)

        if results:
            print("\n" + "="*50)
            print(f" Search Results for '{keyword}' ".center(50, "-"))
            print("="*50)
            for book in results:
                status = "Available" if book.available else "Checked Out"
                print(f"- {book.title} by {book.author} ({status})")
        else:
            print("No books found.")

    # Checkout a book
    def checkout_book(self, isbn, user_id, is_auto=False):
        if isbn in self.books and user_id in self.users:
            book = self.books[isbn]
            user = self.users[user_id]

            if book.available:
                book.available = False
                user.borrow_history.add_book(book)
                
                print(f"\n✅ Successfully checked out:")
                print(f"     - User: {self.users[user_id].name}")
                print(f"     - Title: {book.title}")
                print(f"     - Author: {book.author}")
                print(f"     - Category: {book.category}")
            else:
                if not is_auto: 
                    print(f"\n❗ {book.title} is currently checked out. {user.name} has been added to the reservation queue. \n")
                book.reserve_book(user)
        else:
            print("Invalid ISBN or User ID.")

    # Return a book
    def return_book(self, isbn):
        if isbn in self.books:
            book = self.books[isbn]
            if not book.available:
                next_user = book.next_in_queue()
                if next_user:
                    # before autho-checking out, mark book as available
                    book.available = True

                    print("\n" + "="*50)
                    print(f"                   System Message")
                    print("="*50)
                    print(f"✅ {book.title} returned. Reserved by {next_user.name}. \n   Auto-checking out to them. \n")
                    self.checkout_book(isbn, next_user.user_id, is_auto=True)
                else:
                    book.available = True
                    print("\n" + "="*50)
                    print(f"                System Message")
                    print("="*50)
                    print(f"✅ {book.title} is now available.\n")
            else:
                print("Book is already available.")
        else:
            print("Invalid ISBN.")

    # View user's borrowing history
    def view_user_history(self, user_id):
        if user_id in self.users:
            print ("\n" + "="*50)
            print(f"Borrowing History for {self.users[user_id].name} ".center(50, "-"))
            print("="*50)
            self.users[user_id].borrow_history.print_history()
            print("\n")
        else:
            print("User not found.")

    def show_reservation_line(self, isbn):
        if isbn in self.books:
            print(f"\n🔎 Reservation queue for '{self.books[isbn].title}':")
            self.books[isbn].show_reservation_queue()
        else:
            print("❌ Book not found.")

# --- Demo to Show Functionality ---
if __name__ == "__main__":
    library = Library()

    # Adding books
    library.add_book("001", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction")
    library.add_book("002", "1984", "George Orwell", "Dystopian")
    library.add_book("003", "The Art of Computer Programming", "Donald Knuth", "Computer Science")

    # Adding users
    library.add_user("U1", "Alice", "undergraduate")
    library.add_user("U2", "Bob", "professor")
    library.add_user("U3", "Charlie", "graduate")

    # Searching books
    library.search_books("Fiction")

    # Checking out books
    library.checkout_book("001", "U1")  # undergrad Alice checks out The Great Gatsby
    library.checkout_book("002", "U1")
    library.checkout_book("001", "U3")  # graduate Charlie tries to checks out The Great Gatsby -> ets added to reservation queue
    library.checkout_book("003", "U2")
    library.checkout_book("001", "U2")  # prof Bob tries to checkout same book -> gets added to reservation queue with higher priority

    # Viewing Queue Line
    library.show_reservation_line("001")
    
    # View user borrowing history
    library.view_user_history("U1")
    library.view_user_history("U2")
    library.view_user_history("U3")

    # Returning books
    library.return_book("001")  # Alice returns, prof Bob gets auto-checked out

    # Viewing history
    library.view_user_history("U1")
    library.view_user_history("U2")
    library.view_user_history("U3")

    