import tkinter as tk
from tkinter import messagebox
import json
import os

# Configurações globais
DB_FILE = 'books.json'
ITEMS_PER_PAGE = 20  
CARD_MIN_WIDTH = 250 
current_page = 0

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")

# --- Funções de Lógica ---

def add_book():
    author = entry_author.get()
    title = entry_title.get()
    year = entry_year.get()

    if author and title and year:
        books = load_data()
        books.append({"author": author, "title": title, "year": year})
        save_data(books)
        messagebox.showinfo("Sucesso", "Livro cadastrado!")
        clear_entries()
        render_page()
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def delete_book(book_to_delete):
    if messagebox.askyesno("Confirmar", f"Deseja excluir '{book_to_delete['title']}'?"):
        books = load_data()
        updated_books = [b for b in books if not (b['author'] == book_to_delete['author'] and 
                                                  b['title'] == book_to_delete['title'] and 
                                                  str(b['year']) == str(book_to_delete['year']))]
        save_data(updated_books)
        render_page()

def edit_book_setup(book):
    entry_author.delete(0, tk.END)
    entry_author.insert(0, book['author'])
    entry_title.delete(0, tk.END)
    entry_title.insert(0, book['title'])
    entry_year.delete(0, tk.END)
    entry_year.insert(0, book['year'])
    
    books = load_data()
    updated_books = [b for b in books if not (b['author'] == book['author'] and 
                                              b['title'] == book['title'] and 
                                              str(b['year']) == str(book['year']))]
    save_data(updated_books)

# --- Funções de Interface ---

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)
    render_page()

def render_page():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    books = load_data()
    total_books = len(books) # Conta o total de itens no JSON
    
    start = current_page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_items = books[start:end]

    canvas_width = canvas.winfo_width()
    num_cols = max(1, canvas_width // CARD_MIN_WIDTH)
    if num_cols > 5: num_cols = 5 

    for i in range(num_cols):
        scrollable_frame.grid_columnconfigure(i, weight=1)

    for i, book in enumerate(page_items):
        row = i // num_cols
        col = i % num_cols
        create_card(book, row, col)

    # Atualiza os textos de paginação e total
    total_pages = (total_books - 1) // ITEMS_PER_PAGE + 1 if total_books else 1
    label_page.config(text=f"Página {current_page + 1} de {total_pages}")
    label_total.config(text=f"Total de Livros: {total_books}")

def create_card(book, row, col):
    card = tk.Frame(scrollable_frame, bg="white", highlightbackground="#e0e0e0", 
                    highlightthickness=1, bd=0, padx=10, pady=10, height=180)
    card.grid(row=row, column=col, padx=5, pady=10, sticky="ew")
    card.grid_propagate(False)

    tk.Label(card, text=book['title'], font=("Arial", 11, "bold"), bg="white", fg="#333", wraplength=220, justify="left").pack(anchor="w")
    tk.Label(card, text=f"Autor: {book['author']}", font=("Arial", 9), bg="white", fg="#666", wraplength=220, justify="left").pack(anchor="w")
    tk.Label(card, text=f"Ano: {book['year']}", font=("Arial", 8), bg="white", fg="#07008c").pack(anchor="w")

    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack(side="bottom", anchor="e")

    tk.Button(btn_frame, text="Editar", bg="#ff9800", fg="white", relief="flat", font=("Arial", 8),
              command=lambda b=book: edit_book_setup(b)).pack(side="left", padx=2)
    
    tk.Button(btn_frame, text="Excluir", bg="#f44336", fg="white", relief="flat", font=("Arial", 8),
              command=lambda b=book: delete_book(b)).pack(side="left")

def next_page():
    global current_page
    books = load_data()
    if (current_page + 1) * ITEMS_PER_PAGE < len(books):
        current_page += 1
        render_page()

def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        render_page()

def clear_entries():
    entry_author.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_year.delete(0, tk.END)

# --- Layout Principal ---

root = tk.Tk()
root.title("Livraria Digital")
root.geometry("1500x750")
root.config(bg="#f4f7f6")

header = tk.Frame(root, bg="#3f51b5", pady=15)
header.pack(fill="x")
tk.Label(header, text="Novo Livro", font=("Arial", 18, "bold"), fg="white", bg="#3f51b5").pack()

form = tk.Frame(root, bg="#f4f7f6", pady=15)
form.pack()

tk.Label(form, text="Autor:", bg="#f4f7f6").grid(row=0, column=0, sticky="w")
entry_author = tk.Entry(form, width=35)
entry_author.grid(row=0, column=1, pady=2, padx=10)

tk.Label(form, text="Título:", bg="#f4f7f6").grid(row=1, column=0, sticky="w")
entry_title = tk.Entry(form, width=35)
entry_title.grid(row=1, column=1, pady=2, padx=10)

tk.Label(form, text="Ano:", bg="#f4f7f6").grid(row=2, column=0, sticky="w")
entry_year = tk.Entry(form, width=35)
entry_year.grid(row=2, column=1, pady=2, padx=10)

tk.Button(form, text="Salvar Livro", bg="#4caf50", fg="white", font=("Arial", 10, "bold"),
          width=15, command=add_book).grid(row=3, column=0, columnspan=2, pady=10)

container = tk.Frame(root, bg="#f4f7f6")
container.pack(fill="both", expand=True, padx=(10, 0))

canvas = tk.Canvas(container, bg="#f4f7f6", highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f4f7f6")

canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", on_canvas_configure)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Rodapé com Paginação e Total ---
footer = tk.Frame(root, bg="#f4f7f6", pady=10)
footer.pack(fill="x")

# Label de Total (Fica centralizada acima da navegação)
label_total = tk.Label(footer, text="Total de Livros: 0", bg="#f4f7f6", font=("Arial", 12, "bold"), fg="#008E1F")
label_total.pack()

nav_frame = tk.Frame(footer, bg="#f4f7f6")
nav_frame.pack(fill="x", pady=5)

tk.Button(nav_frame, text="◀ Anterior", bg="#520078", fg="#ffffff", font=("Arial", 12, "bold"), command=prev_page, width=12).pack(side="left", padx=50)
label_page = tk.Label(nav_frame, text="Página 1", bg="#f6f4f7", font=("Arial", 12, "bold"))
label_page.pack(side="left", expand=True)
tk.Button(nav_frame, text="Próxima ▶",  bg="#520078", fg="#ffffff", font=("Arial", 12, "bold"), command=next_page, width=12).pack(side="right", padx=50)

render_page()
root.mainloop()
