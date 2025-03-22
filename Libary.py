import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import datetime

# File to store books data
BOOKS_FILE = "books.csv"

# File to store transaction data
TRANSACTIONS_FILE = "transactions.csv"

# Initialize books data
def initialize_books():
    if not os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Book ID", "Title", "Author", "Available"])
            writer.writerow(["1", "Python Programming", "John Doe", "Yes"])
            writer.writerow(["2", "Data Science Basics", "Jane Smith", "Yes"])

# Initialize transactions file
def initialize_transactions():
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Transaction ID", "Book ID", "User", "Action", "Timestamp"])

initialize_books()
initialize_transactions()

class LibrarySystem:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Library Login")
        self.create_login_window()
        self.login_window.mainloop()

    def create_login_window(self):
        tk.Label(self.login_window, text="Library Management System", font=("Arial", 16)).pack(pady=20)
        
        frame = tk.Frame(self.login_window)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(self.login_window, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "admin123":
            self.login_window.destroy()
            self.admin_home()
        elif username == "user" and password == "user123":
            self.login_window.destroy()
            self.user_home()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def admin_home(self):
        self.admin_window = tk.Tk()
        self.admin_window.title("Admin Dashboard")
        
        tk.Label(self.admin_window, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)
        
        buttons = [
            ("Add Book", self.add_book),
            ("Delete Book", self.delete_book),
            ("Update Book", self.update_book),
            ("Check Availability", self.check_availability),
            ("Logout", lambda: self.logout(self.admin_window))
        ]
        
        for text, command in buttons:
            tk.Button(self.admin_window, text=text, width=20, command=command).pack(pady=5)

    def user_home(self):
        self.user_window = tk.Tk()
        self.user_window.title("User Dashboard")
        
        tk.Label(self.user_window, text="User Dashboard", font=("Arial", 16)).pack(pady=20)
        
        buttons = [
            ("Issue Book", self.issue_book),
            ("Return Book", self.return_book),
            ("Check Availability", self.check_availability),
            ("Logout", lambda: self.logout(self.user_window))
        ]
        
        for text, command in buttons:
            tk.Button(self.user_window, text=text, width=20, command=command).pack(pady=5)
    
    def logout(self, window):
        window.destroy()
        self.__init__()

    def add_book(self):
        add_window = tk.Toplevel(self.admin_window)
        add_window.title("Add New Book")
        
        fields = ["Book ID:", "Title:", "Author:"]
        entries = []
        
        for i, field in enumerate(fields):
            tk.Label(add_window, text=field).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)
        
        def save_book():
            data = [entry.get() for entry in entries]
            if all(data):
                with open(BOOKS_FILE, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([*data, "Yes"])
                messagebox.showinfo("Success", "Book added successfully!")
                add_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")
        
        tk.Button(add_window, text="Save", command=save_book).grid(row=len(fields), columnspan=2, pady=10)

    def delete_book(self):
        del_window = tk.Toplevel(self.admin_window)
        del_window.title("Delete Book")
        
        tk.Label(del_window, text="Enter Book ID to delete:").pack(pady=10)
        book_id_entry = tk.Entry(del_window)
        book_id_entry.pack(pady=5)
        
        def confirm_delete():
            book_id = book_id_entry.get()
            books = []
            deleted = False
            
            with open(BOOKS_FILE, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] != book_id:
                        books.append(row)
                    else:
                        deleted = True
            
            if deleted:
                with open(BOOKS_FILE, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(books)
                messagebox.showinfo("Success", "Book deleted successfully!")
                del_window.destroy()
            else:
                messagebox.showerror("Error", "Book ID not found")
        
        tk.Button(del_window, text="Delete", command=confirm_delete).pack(pady=10)

    def update_book(self):
        update_window = tk.Toplevel(self.admin_window)
        update_window.title("Update Book Details")
        
        tk.Label(update_window, text="Book ID:").pack(pady=5)
        book_id_entry = tk.Entry(update_window)
        book_id_entry.pack(pady=5)
        
        def fetch_book():
            book_id = book_id_entry.get()
            with open(BOOKS_FILE, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == book_id:
                        self.show_update_fields(update_window, row)
                        return
                messagebox.showerror("Error", "Book not found")
        
        tk.Button(update_window, text="Fetch Book", command=fetch_book).pack(pady=10)

    def show_update_fields(self, window, book_data):
        fields = ["Title:", "Author:", "Availability (Yes/No):"]
        entries = []
        
        for i, field in enumerate(fields):
            tk.Label(window, text=field).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(window)
            entry.insert(0, book_data[i+1] if i < 2 else book_data[3])
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)
        
        def save_changes():
            new_data = [entry.get() for entry in entries]
            books = []
            updated = False
            
            with open(BOOKS_FILE, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == book_data[0]:
                        row[1:4] = new_data
                        updated = True
                    books.append(row)
            
            if updated:
                with open(BOOKS_FILE, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(books)
                messagebox.showinfo("Success", "Book updated successfully!")
                window.destroy()
            else:
                messagebox.showerror("Error", "Update failed")
        
        tk.Button(window, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def issue_book(self):
        issue_window = tk.Toplevel(self.user_window)
        issue_window.title("Issue Book")
        
        tk.Label(issue_window, text="Enter Book ID:").pack(pady=10)
        book_id_entry = tk.Entry(issue_window)
        book_id_entry.pack(pady=5)
        
        def process_issue():
            book_id = book_id_entry.get()
            books = []
            issued = False
            
            with open(BOOKS_FILE, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == book_id:
                        if row[3] == "Yes":
                            row[3] = "No"
                            issued = True
                            # Record the transaction
                            self.record_transaction(book_id, "user", "issue")
                        else:
                            messagebox.showerror("Error", "Book not available")
                    books.append(row)
            
            if issued:
                with open(BOOKS_FILE, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(books)
                messagebox.showinfo("Success", "Book issued successfully!")
                issue_window.destroy()
            else:
                messagebox.showerror("Error", "Book issue failed")
        
        tk.Button(issue_window, text="Issue", command=process_issue).pack(pady=10)

    def return_book(self):
        return_window = tk.Toplevel(self.user_window)
        return_window.title("Return Book")
        
        tk.Label(return_window, text="Enter Book ID:").pack(pady=10)
        book_id_entry = tk.Entry(return_window)
        book_id_entry.pack(pady=5)
        
        def process_return():
            book_id = book_id_entry.get()
            books = []
            returned = False
            
            with open(BOOKS_FILE, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == book_id:
                        if row[3] == "No":
                            row[3] = "Yes"
                            returned = True
                            # Record the transaction
                            self.record_transaction(book_id, "user", "return")
                        else:
                            messagebox.showerror("Error", "Book was not issued")
                    books.append(row)
            
            if returned:
                with open(BOOKS_FILE, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(books)
                messagebox.showinfo("Success", "Book returned successfully!")
                return_window.destroy()
            else:
                messagebox.showerror("Error", "Book return failed")
        
        tk.Button(return_window, text="Return", command=process_return).pack(pady=10)

    def check_availability(self):
        avail_window = tk.Toplevel()
        avail_window.title("Book Availability")
        
        tree = ttk.Treeview(avail_window, columns=("ID", "Title", "Author", "Status"), show="headings")
        tree.heading("ID", text="Book ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Status", text="Availability")
        
        with open(BOOKS_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                tree.insert("", "end", values=row)
        
        tree.pack(padx=10, pady=10)
        tk.Button(avail_window, text="Close", command=avail_window.destroy).pack(pady=10)

    def record_transaction(self, book_id, user, action):
        transaction_id = self.get_next_transaction_id()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(TRANSACTIONS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([transaction_id, book_id, user, action, timestamp])

    def get_next_transaction_id(self):
        try:
            with open(TRANSACTIONS_FILE, 'r') as file:
                reader = csv.reader(file)
                transactions = list(reader)
                if len(transactions) > 1:  # Skip header
                    last_id = int(transactions[-1][0])
                    return last_id + 1
                else:
                    return 1
        except FileNotFoundError:
            return 1

if __name__ == "__main__":
    LibrarySystem()
