class Book:
    def __init__(self, isbn, title, author, category):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.category = category
        self.available = True
        self.reservation_queue = Queue()

    def reserve_book(self, user):
        self.reservation_queue.enqueue(user)

    def next_in_queue(self):
        return self.reservation_queue.dequeue()


class LinkedListNode:
    def __init__(self, book):
        self.book = book
        self.next = None

class BorrowHistory:
    def __init__(self):
        self.head = None

    def add_book(self, book):
        new_node = LinkedListNode(book)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def print_history(self):
        current = self.head
        while current:
            print(f"- {current.book.title} by {current.book.author}")
            current = current.next


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrow_history = BorrowHistory()


class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def is_empty(self):
        return self.front is None


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

    # Add user to the library system
    def add_user(self, user_id, name):
        if user_id not in self.users:
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
            print("Search Results:")
            for book in results:
                status = "Available" if book.available else "Checked Out"
                print(f"- {book.title} by {book.author} ({status})")
        else:
            print("No books found.")

    # Checkout a book
    def checkout_book(self, isbn, user_id):
        if isbn in self.books and user_id in self.users:
            book = self.books[isbn]
            user = self.users[user_id]

            if book.available:
                book.available = False
                user.borrow_history.add_book(book)
                print(f"{user.name} checked out {book.title}.")
            else:
                print(f"{book.title} is not available. Adding {user.name} to reservation queue.")
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
                    print(f"Book returned. Reserved by {next_user.name}. Auto-checking out to them.")
                    self.checkout_book(isbn, next_user.user_id)
                else:
                    book.available = True
                    print(f"{book.title} is now available.")
            else:
                print("Book is already available.")
        else:
            print("Invalid ISBN.")

    # View user's borrowing history
    def view_user_history(self, user_id):
        if user_id in self.users:
            print(f"Borrowing History for {self.users[user_id].name}:")
            self.users[user_id].borrow_history.print_history()
        else:
            print("User not found.")


# Demo to show functionality
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

    library.view_user_history("U1")
    library.view_user_history("U2")

    # Returning books
    library.return_book("001")  # Alice returns, Bob gets auto-checked out

    # Viewing history
    library.view_user_history("U1")
    library.view_user_history("U2")
