import tkinter as tk
from tkinter import messagebox
import json
import os


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'is_borrowed': self.is_borrowed
        }

    @staticmethod
    def from_dict(data):
        book = Book(data['title'], data['author'], data['isbn'])
        book.is_borrowed = data['is_borrowed']
        return book


class User:
    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = password
        self.role = role


class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        if os.path.exists("library_data.json"):
            self.load_data()

    def load_data(self):
        with open("library_data.json", "r") as file:
            data = json.load(file)
            for book_data in data['books']:
                book = Book.from_dict(book_data)
                self.books.append(book)
            for username, user_data in data['users'].items():
                user = User(username, user_data['password'], user_data['role'])
                self.users[username] = user

    def save_data(self):
        data = {
            'books': [book.to_dict() for book in self.books],
            'users': {username: {'password': user.password, 'role': user.role} for username, user in self.users.items()}
        }
        with open("library_data.json", "w") as file:
            json.dump(data, file)

    def register_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = User(username, password)
        self.save_data()
        return True

    def login_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    def add_book(self, book):
        self.books.append(book)
        self.save_data()

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_borrowed:
                book.is_borrowed = True
                self.save_data()
                return True
        return False

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and book.is_borrowed:
                book.is_borrowed = False
                self.save_data()
                return True
        return False

    def search_books(self, query):
        results = [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]
        return results


class LibraryApp:
    def __init__(self):
        self.library = Library()
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("Library Management System")
        
        # Create frames for different sections
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.user_frame = tk.Frame(self.root)
        
        # Create login frame components
        tk.Label(self.login_frame, text="Username").grid(row=0)
        tk.Label(self.login_frame, text="Password").grid(row=1)
        
        self.username_login_entry = tk.Entry(self.login_frame)
        self.password_login_entry = tk.Entry(self.login_frame, show="*")
        
        self.username_login_entry.grid(row=0, column=1)
        self.password_login_entry.grid(row=1, column=1)
        
        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, columnspan=2)
        
        tk.Button(self.login_frame, text="Register", command=self.show_register_frame).grid(row=3, columnspan=2)

        
         # Create register frame components
        tk.Label(self.register_frame, text="Username").grid(row=0)
        tk.Label(self.register_frame, text="Password").grid(row=1)

        self.username_register_entry = tk.Entry(self.register_frame)
        self.password_register_entry = tk.Entry(self.register_frame, show="*")

        self.username_register_entry.grid(row=0, column=1)
        self.password_register_entry.grid(row=1, column=1)

        tk.Button(self.register_frame, text="Register", command=self.register).grid(row=2, columnspan=2)

        tk.Button(self.register_frame, text="Back to Login", command=self.show_login_frame).grid(row=3,columnspan=2)

         
         # Create user frame components
        tk.Button(self.user_frame,text="Add Book", command=self.add_book).grid(row=0,columnspan=2)
        tk.Button(self.user_frame,text="View Books", command=self.view_books).grid(row=1,columnspan=2)
        tk.Button(self.user_frame,text="Search Books", command=self.search_books).grid(row=2,columnspan=2)

         # Pack frames into the main window
        for frame in (self.login_frame,self.register_frame,self.user_frame):
             frame.grid(row=0,column=0)

         # Show login frame initially
        self.show_login_frame()

     # Show login frame method
    def show_login_frame(self):
       # Hide all frames and show login frame only
       for frame in (self.register_frame,self.user_frame):
           frame.grid_remove()
       self.login_frame.grid()

   # Show register frame method
    def show_register_frame(self):
       # Hide all frames and show register frame only
       for frame in (self.login_frame,self.user_frame):
           frame.grid_remove()
       self.register_frame.grid()

   # Login method 
    def login(self):
       username = self.username_login_entry.get()
       password = self.password_login_entry.get()
       user = self.library.login_user(username,password)

       if user:
           messagebox.showinfo("Login","Login successful!")
           # Hide login frame and show user frame 
           for frame in (self.login_frame,self.register_frame):
               frame.grid_remove()
           self.user_frame.grid()
       else:
           messagebox.showerror("Login","Invalid credentials!")

   # Register method 
    def register(self):
       username = self.username_register_entry.get()
       password = self.password_register_entry.get()

       if not username or not password:
           messagebox.showerror("Registration","Please fill all fields!")
           return

       if not library.register_user(username,password):
           messagebox.showerror("Registration","Username already exists!")
       else:
           messagebox.showinfo("Registration","Registration successful!")
           # Show login frame after registration 
           self.show_login_frame()

   # Add Book method 
    def add_book(self):
       title = input("Enter Book Title: ")
       author = input("Enter Author Name: ")
       isbn = input("Enter ISBN Number: ")

       new_book = Book(title, author,isbn)
       library.add_book(new_book)

   # View Books method 
    def view_books(self):
       books_list = "\n".join([f"{book.title} by {book.author} (ISBN: {book.isbn})" for book in library.books])
       
       if not books_list:
           books_list ="No books available."
       
       messagebox.showinfo("Books Available",books_list)

   # Search Books method 
    def search_books(self):
       query = input("Enter search query (title/author): ")
       results = library.search_books(query)

       if results:
           result_list="\n".join([f"{book.title} by {book.author} (ISBN: {book.isbn})" for book in results])
           messagebox.showinfo("Search Results",result_list)
       else:
           messagebox.showinfo("Search Results","No books found.")

if __name__ == "__main__":
   app = LibraryApp()
   app.root.mainloop()


# install package through terminal before running code.

# 1. pip install json
# 2. pip install os
# 3. pip install tkinter
# 4. pip install messagebox
