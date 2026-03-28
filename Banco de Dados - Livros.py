import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Nome do arquivo de banco de dados
DB_FILE = 'books.json'

# Funções de persistência JSON
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

# Funções do programa
def add_book():
    author = entry_author.get()
    title = entry_title.get()
    year = entry_year.get()

    if author and title and year:
        books = load_data()
        # NoSQL: Adicionamos o dicionário sem um ID incremental fixo
        new_book = {
            "author": author,
            "title": title,
            "year": year
        }
        books.append(new_book)
        save_data(books)
        
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        clear_entries()
        display_books()
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def display_books(filter_data=None):
    for row in tree.get_children():
        tree.delete(row)
    
    books = filter_data if filter_data is not None else load_data()
    
    for book in books:
        # Exibe apenas Autor, Título e Ano
        tree.insert('', 'end', values=(book['author'], book['title'], book['year']))

def delete_book():
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item[0])['values']
        books = load_data()
        
        # Filtra a lista removendo o livro que coincide com os valores selecionados
        # (Em NoSQL sem ID, usamos a combinação dos campos como critério)
        updated_books = [b for b in books if not (b['author'] == item_values[0] and 
                                                  b['title'] == item_values[1] and 
                                                  str(b['year']) == str(item_values[2]))]
        
        save_data(updated_books)
        display_books()
        clear_entries()
        messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Selecione um livro para excluir.")

def edit_book():
    selected_item = tree.selection()
    if selected_item:
        old_values = tree.item(selected_item[0])['values']
        new_author = entry_author.get()
        new_title = entry_title.get()
        new_year = entry_year.get()

        if new_author and new_title and new_year:
            books = load_data()
            for b in books:
                if (b['author'] == old_values[0] and 
                    b['title'] == old_values[1] and 
                    str(b['year']) == str(old_values[2])):
                    
                    b['author'] = new_author
                    b['title'] = new_title
                    b['year'] = new_year
                    break
            
            save_data(books)
            display_books()
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
    else:
        messagebox.showwarning("Atenção", "Selecione um livro para editar.")

def search_books():
    search_term = search_entry.get().lower()
    books = load_data()
    
    filtered = [b for b in books if 
                search_term in b['author'].lower() or 
                search_term in b['title'].lower() or 
                search_term in str(b['year'])]
    
    display_books(filtered)

def clear_entries():
    entry_author.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_year.delete(0, tk.END)

def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item[0])['values']
        clear_entries()
        entry_author.insert(tk.END, item[0])
        entry_title.insert(tk.END, item[1])
        entry_year.insert(tk.END, item[2])

# Interface gráfica (Tkinter)
root = tk.Tk()
root.title("Cadastro de Livros")
root.geometry("800x650")
root.config(bg="#f9f9f9")

label_title = tk.Label(root, text="Cadastro de Livros (JSON)", font=("Arial", 24, "bold"), fg="#3f51b5", bg="#f9f9f9")
label_title.pack(pady=10)

frame_form = tk.Frame(root, bg="#fff", padx=20, pady=20, relief=tk.GROOVE, borderwidth=2)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nome do Autor:", font=("Arial", 14), bg="#fff").grid(row=0, column=0, sticky="w")
entry_author = tk.Entry(frame_form, font=("Arial", 14), width=30)
entry_author.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Título do Livro:", font=("Arial", 14), bg="#fff").grid(row=1, column=0, sticky="w")
entry_title = tk.Entry(frame_form, font=("Arial", 14), width=30)
entry_title.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Ano de Publicação:", font=("Arial", 14), bg="#fff").grid(row=2, column=0, sticky="w")
entry_year = tk.Entry(frame_form, font=("Arial", 14), width=10)
entry_year.grid(row=2, column=1, padx=10, pady=5)

btn_add = tk.Button(frame_form, text="Cadastrar Livro", font=("Arial", 14), bg="#3f51b5", fg="white", command=add_book)
btn_add.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

btn_edit = tk.Button(frame_form, text="Editar Livro", font=("Arial", 14), bg="#ff9800", fg="white", command=edit_book)
btn_edit.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

btn_delete = tk.Button(frame_form, text="Excluir Livro", font=("Arial", 14), bg="#f44336", fg="white", command=delete_book)
btn_delete.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

tk.Label(root, text="Buscar:", font=("Arial", 14), bg="#f9f9f9").pack(pady=5)
search_entry = tk.Entry(root, font=("Arial", 14), width=40)
search_entry.pack(pady=5)

btn_search = tk.Button(root, text="Buscar", font=("Arial", 14), bg="#3f51b5", fg="white", command=search_books)
btn_search.pack(pady=5)

# Tabela sem o campo ID
tree = ttk.Treeview(root, columns=("Autor", "Título", "Ano"), show="headings", height=10)
tree.heading("Autor", text="Autor")
tree.heading("Título", text="Título")
tree.heading("Ano", text="Ano")
tree.column("Autor", width=250)
tree.column("Título", width=300)
tree.column("Ano", width=100)
tree.pack(pady=10)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Inicialização
display_books()
root.mainloop()
