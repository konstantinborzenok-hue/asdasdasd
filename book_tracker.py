import tkinter as tk
from tkinter import messagebox
import json
import os

class BookTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Book Tracker")

        self.books = self.load_books()

        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.pages_var = tk.StringVar()
        self.filter_genre_var = tk.StringVar()
        self.filter_pages_var = tk.BooleanVar()

        tk.Label(master, text="Book Title").grid(row=0, column=0)
        tk.Label(master, text="Author").grid(row=1, column=0)
        tk.Label(master, text="Genre").grid(row=2, column=0)
        tk.Label(master, text="Pages").grid(row=3, column=0)

        self.title_entry = tk.Entry(master, textvariable=self.title_var)
        self.author_entry = tk.Entry(master, textvariable=self.author_var)
        self.genre_entry = tk.Entry(master, textvariable=self.genre_var)
        self.pages_entry = tk.Entry(master, textvariable=self.pages_var)
        
        self.title_entry.grid(row=0, column=1)
        self.author_entry.grid(row=1, column=1)
        self.genre_entry.grid(row=2, column=1)
        self.pages_entry.grid(row=3, column=1)

        tk.Button(master, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2)

        tk.Label(master, text="Filter by Genre").grid(row=5, column=0)
        self.filter_genre_entry = tk.Entry(master, textvariable=self.filter_genre_var)
        self.filter_genre_entry.grid(row=5, column=1)

        tk.Checkbutton(master, text="More than 200 pages", variable=self.filter_pages_var).grid(row=6, column=0, columnspan=2)

        tk.Button(master, text="Apply Filter", command=self.apply_filter).grid(row=7, column=0, columnspan=2)

        self.book_list = tk.Listbox(master, width=50, height=10)
        self.book_list.grid(row=8, column=0, columnspan=2)

        self.populate_books()

    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r") as file:
                return json.load(file)
        return []

    def save_books(self):
        with open("books.json", "w") as file:
            json.dump(self.books, file, indent=4)

    def add_book(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        genre = self.genre_var.get().strip()
        pages = self.pages_var.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not pages.isdigit():
            messagebox.showerror("Error", "Pages must be a number")
            return

        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        })
        self.save_books()
        self.populate_books()

    def apply_filter(self):
        filter_genre = self.filter_genre_var.get().strip().lower()
        filter_pages = self.filter_pages_var.get()

        filtered_books = [
            book for book in self.books
            if (filter_genre in book['genre'].lower() or not filter_genre) and
               (book['pages'] > 200 if filter_pages else True)
        ]

        self.book_list.delete(0, tk.END)
        for book in filtered_books:
            self.book_list.insert(tk.END, f"{book['title']} by {book['author']}")

    def populate_books(self):
        self.book_list.delete(0, tk.END)
        for book in self.books:
            self.book_list.insert(tk.END, f"{book['title']} by {book['author']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
