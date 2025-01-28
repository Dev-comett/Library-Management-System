from datetime import datetime, timedelta

# Book Class
class Book:
    def __init__(self, title, author, isbn, copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies  # Number of copies available

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - Copies: {self.copies}"


# Member Class
class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []  # Track borrowed books

    def __str__(self):
        return f"Member ID: {self.member_id}, Name: {self.name}"


# Library Class
class Library:
    def __init__(self):
        self.books = {}  # Key: ISBN, Value: Book object
        self.members = {}  # Key: Member ID, Value: Member object
        self.issued_books = {}  # Key: Member ID, Value: List of (Book, due_date)

    # Add a new book
    def add_book(self, book):
        if book.isbn in self.books:
            self.books[book.isbn].copies += book.copies
        else:
            self.books[book.isbn] = book
        print(f"Book '{book.title}' added to the library.")

    # View all books
    def view_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        print("\nBooks in Library:")
        for book in self.books.values():
            print(book)

    # Remove a book
    def remove_book(self, isbn):
        if isbn in self.books:
            del self.books[isbn]
            print(f"Book with ISBN {isbn} removed from the library.")
        else:
            print("Book not found.")

    # Register a member
    def register_member(self, member):
        if member.member_id in self.members:
            print("Member already exists.")
        else:
            self.members[member.member_id] = member
            print(f"Member '{member.name}' registered successfully.")

    # Issue a book
    def issue_book(self, member_id, isbn):
        if member_id not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return
        book = self.books[isbn]
        if book.copies <= 0:
            print("Book is not available.")
            return
        member = self.members[member_id]
        due_date = datetime.now() + timedelta(days=14)  # 2 weeks from now
        book.copies -= 1
        member.borrowed_books.append(book)
        self.issued_books.setdefault(member_id, []).append((book, due_date))
        print(f"Book '{book.title}' issued to member '{member.name}' until {due_date.strftime('%Y-%m-%d')}.")

    # Return a book
    def return_book(self, member_id, isbn):
        if member_id not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return
        member = self.members[member_id]
        book = self.books[isbn]
        if book in member.borrowed_books:
            member.borrowed_books.remove(book)
            book.copies += 1
            self.issued_books[member_id] = [
                (b, due_date) for b, due_date in self.issued_books.get(member_id, []) if b.isbn != isbn
            ]
            print(f"Book '{book.title}' returned by member '{member.name}'.")
        else:
            print(f"Book '{book.title}' was not borrowed by member '{member.name}'.")

    # View issued books
    def view_issued_books(self):
        if not self.issued_books:
            print("No books are currently issued.")
            return
        print("\nIssued Books:")
        for member_id, books in self.issued_books.items():
            member = self.members[member_id]
            print(f"\nMember: {member.name} (ID: {member_id})")
            for book, due_date in books:
                print(f"  - {book.title} (Due: {due_date.strftime('%Y-%m-%d')})")


# Main Program
if __name__ == "__main__":
    library = Library()

    # Adding books
    library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", "12345", 5))
    library.add_book(Book("1984", "George Orwell", "54321", 3))

    # Registering members
    library.register_member(Member("M001", "Alice"))
    library.register_member(Member("M002", "Bob"))

    # Viewing books
    library.view_books()

    # Issuing books
    library.issue_book("M001", "12345")
    library.issue_book("M002", "54321")

    # Viewing issued books
    library.view_issued_books()

    # Returning a book
    library.return_book("M001", "12345")

    # Viewing books after return
    library.view_books()

    # Viewing issued books after return
    library.view_issued_books()
