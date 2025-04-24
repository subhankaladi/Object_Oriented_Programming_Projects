import json
import os
from abc import ABC, abstractmethod
import uuid

# Abstraction: Defining an abstract base class for storage operations
class LibraryStorage(ABC):
    """Abstract base class demonstrating abstraction"""
    # Abstraction: Abstract methods that must be implemented by subclasses
    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def save(self, data):
        pass

# Inheritance: FileStorage inherits from LibraryStorage
class FileStorage(LibraryStorage):
    """Concrete class for file storage implementing abstraction and encapsulation"""
    def __init__(self, filename='library.txt'):
        # Encapsulation: Using protected attribute to hide implementation details
        self._filename = filename
    
    # Abstraction: Implementing abstract method from parent class
    def load(self):
        if os.path.exists(self._filename):
            with open(self._filename, 'r') as file:
                return json.load(file)
        return []
    
    # Abstraction: Implementing abstract method from parent class
    def save(self, data):
        with open(self._filename, 'w') as file:
            json.dump(data, file)

# Encapsulation: Book class encapsulates book-related data and behavior
class Book:
    """Base class for books demonstrating encapsulation"""
    def __init__(self, title, author, year, genre, read=False):
        # Encapsulation: Using protected attributes to hide internal state
        self._id = str(uuid.uuid4())
        self._title = title
        self._author = author
        self._year = year
        self._genre = genre
        self._read = read
    
    # Encapsulation: Using property decorators for controlled access to attributes
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def read(self):
        return self._read
    
    # Encapsulation: Controlled modification of read status
    @read.setter
    def read(self, value):
        self._read = value
    
    # Polymorphism: This method can be overridden in subclasses
    def get_details(self):
        """Method to get book details"""
        status = "Read" if self._read else "Unread"
        return f"{self._title} by {self._author} ({self._year}) - {self._genre} - {status}"

# Inheritance: SpecialBook inherits from Book
# Polymorphism: Overrides get_details method
class SpecialBook(Book):
    """Derived class demonstrating inheritance and polymorphism"""
    def __init__(self, title, author, year, genre, read=False, special_note=""):
        # Inheritance: Calling parent class constructor
        super().__init__(title, author, year, genre, read)
        # Encapsulation: Protected attribute for special note
        self._special_note = special_note
    
    # Polymorphism: Overriding parent class method to provide different behavior
    def get_details(self):
        base_details = super().get_details()
        return f"{base_details} [Special Note: {self._special_note}]"

# Encapsulation: LibraryManager encapsulates all library operations
class LibraryManager:
    """Main class managing the library operations"""
    def __init__(self, storage: LibraryStorage):
        # Encapsulation: Using composition to hide storage implementation
        self._storage = storage
        # Encapsulation: Private books list
        self._books = self._load_books()
    
    # Encapsulation: Private method for loading books
    def _load_books(self):
        """Private method demonstrating encapsulation"""
        raw_data = self._storage.load()
        books = []
        for book_data in raw_data:
            if 'special_note' in book_data:
                # Polymorphism: Creating different book types based on data
                book = SpecialBook(
                    book_data['title'],
                    book_data['author'],
                    book_data['year'],
                    book_data['genre'],
                    book_data['read'],
                    book_data['special_note']
                )
            else:
                book = Book(
                    book_data['title'],
                    book_data['author'],
                    book_data['year'],
                    book_data['genre'],
                    book_data['read']
                )
            books.append(book)
        return books
    
    # Encapsulation: Private method for saving books
    def _save_books(self):
        """Private method demonstrating encapsulation"""
        books_data = []
        for book in self._books:
            book_data = {
                'title': book.title,
                'author': book.author,
                'year': book._year,
                'genre': book._genre,
                'read': book.read
            }
            # Polymorphism: Handling different book types
            if isinstance(book, SpecialBook):
                book_data['special_note'] = book._special_note
            books_data.append(book_data)
        self._storage.save(books_data)
    
    def add_book(self, is_special=False):
        """Method to add new books"""
        title = input("Enter book title: ")
        author = input("Enter author: ")
        year = input("Enter publication year: ")
        genre = input("Enter genre: ")
        read = input("Have you read this book? (yes/no): ").lower() == 'yes'
        
        # Polymorphism: Creating different book types based on parameter
        if is_special:
            special_note = input("Enter special note: ")
            book = SpecialBook(title, author, year, genre, read, special_note)
        else:
            book = Book(title, author, year, genre, read)
        
        self._books.append(book)
        self._save_books()
        print(f'Book "{title}" added successfully!')
    
    def remove_book(self):
        """Method to remove books"""
        title = input("Enter the title of the book to remove: ")
        initial_length = len(self._books)
        self._books = [book for book in self._books if book.title.lower() != title.lower()]
        if len(self._books) < initial_length:
            self._save_books()
            print(f'Book "{title}" removed successfully!')
        else:
            print(f'Book "{title}" not found.')
    
    def search_books(self):
        """Method to search books"""
        search_by = input("Search by title or author: ").lower()
        if search_by not in ['title', 'author']:
            print("Invalid search criteria.")
            return
        
        search_term = input(f"Enter the {search_by}: ").lower()
        results = [book for book in self._books if search_term in getattr(book, search_by).lower()]
        
        if results:
            # Polymorphism: Calling get_details which could be from Book or SpecialBook
            for book in results:
                print(book.get_details())
        else:
            print("No matching books found.")
    
    def display_all_books(self):
        """Method to display all books"""
        if self._books:
            # Polymorphism: Calling get_details which could be from different book types
            for book in self._books:
                print(book.get_details())
        else:
            print("No books in the library.")
    
    def display_statistics(self):
        """Method to display library statistics"""
        total_books = len(self._books)
        read_books = len([book for book in self._books if book.read])
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        print(f"Total Books: {total_books}")
        print(f"Percentage Read: {percentage_read:.2f}%")

def main():
    # Abstraction: Using FileStorage through abstract interface
    storage = FileStorage()
    # Encapsulation: LibraryManager hides implementation details
    library = LibraryManager(storage)
    
    while True:
        print("\nMenu:")
        print("1. Add Regular Book")
        print("2. Add Special Book")
        print("3. Remove Book")
        print("4. Search Book")
        print("5. Display All Books")
        print("6. Display Statistics")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            library.add_book(is_special=False)
        elif choice == '2':
            library.add_book(is_special=True)
        elif choice == '3':
            library.remove_book()
        elif choice == '4':
            library.search_books()
        elif choice == '5':
            library.display_all_books()
        elif choice == '6':
            library.display_statistics()
        elif choice == '7':
            print("Exiting the Library Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()