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
        self.reservation_queue = Queue()

    # enqueue a user to reserve the book
    def reserve_book(self, user):
        self.reservation_queue.enqueue(user)

    # dequeue the next user waiting for book
    def next_in_queue(self):
        return self.reservation_queue.dequeue()

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


# --- User Class --- 
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrow_history = BorrowHistory()

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
        
    def is_empty(self):
        return self.front is None
        
    # enqueue data at the end
    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
        print(f"📚 Enqueued: {data.name}")
        
    # dequeue data from the front
    def dequeue(self):
        if self.is_empty():
            print("⚠️ Queue is empty. Nothing to dequeue.")
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        print(f"✅ Dequeued: {temp.data.name}")
        return temp.data

    def peek(self):
        if self.is_empty():
            return None
        return self.front.data

    def __len__(self):
        return self.size


# --- Library System ---
class Library:
    def __init__(self):
        self.books = {}  # HashMap: isbn -> Book
        self.users = {}  # HashMap: user_id -> User

    # Add book to the library
    def add_book(self, isbn, title, author, category):
        if isbn not in self.books: #edge case: isbn not found
            self.books[isbn] = Book(isbn, title, author, category)
            print(f"Added book: {title}.")
        else:
            print("Book with this ISBN already exists.")

    # Add a new user to the library system
    def add_user(self, user_id, name):
        if user_id not in self.users: #edge case: user id not found
            self.users[user_id] = User(user_id, name)
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
        else: #edge case: book not found
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


# --- Demo to Show Functionality ---
if __name__ == "__main__":
    library = Library()

    # Adding books
    library.add_book("001", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction")
    library.add_book("002", "1984", "George Orwell", "Dystopian")
    library.add_book("003", "The Art of Computer Programming", "Donald Knuth", "Computer Science")

    # Adding users
    library.add_user("U1", "Alice")
    library.add_user("U2", "Bob")

    # Searching books
    library.search_books("Fiction")

    # Checking out books
    library.checkout_book("001", "U1")  # Alice checks out The Great Gatsby
    library.checkout_book("002", "U1")
    library.checkout_book("003", "U2")
    library.checkout_book("001", "U2")  # Bob tries to checkout same book -> gets added to reservation queue

    # View user borrowing history
    library.view_user_history("U1")
    library.view_user_history("U2")

    # Returning booksr
    library.return_book("001")  # Alice returns, Bob gets auto-checked out

    # Viewing history
    library.view_user_history("U1")
    library.view_user_history("U2")
