import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('books.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS books
                  (id INTEGER PRIMARY KEY, author TEXT, title TEXT, year INTEGER)''')
conn.commit()

# Funções do programa
def add_book():
    author = entry_author.get()
    title = entry_title.get()
    year = entry_year.get()

    if author and title and year:
        cursor.execute('INSERT INTO books (author, title, year) VALUES (?, ?, ?)', (author, title, int(year)))
        conn.commit()
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        entry_author.delete(0, tk.END)
        entry_title.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        load_books()
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def load_books():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM books')
    for book in cursor.fetchall():
        tree.insert('', 'end', values=(book[0], book[1], book[2], book[3]))

def delete_book():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item[0])['values'][0]
        cursor.execute('DELETE FROM books WHERE id = ?', (item_id,))
        conn.commit()
        load_books()
        messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Selecione um livro para excluir.")

def edit_book():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item[0])['values'][0]
        new_author = entry_author.get()
        new_title = entry_title.get()
        new_year = entry_year.get()

        if new_author and new_title and new_year:
            cursor.execute('''UPDATE books SET author = ?, title = ?, year = ? WHERE id = ?''',
                           (new_author, new_title, int(new_year), item_id))
            conn.commit()
            load_books()
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
    else:
        messagebox.showwarning("Atenção", "Selecione um livro para editar.")

def search_books():
    search_term = search_entry.get()
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM books WHERE author LIKE ? OR title LIKE ? OR year LIKE ?", 
                   (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    for book in cursor.fetchall():
        tree.insert('', 'end', values=(book[0], book[1], book[2], book[3]))

# Preenche os campos de entrada com os dados da linha selecionada
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item[0])['values']
        entry_author.delete(0, tk.END)
        entry_author.insert(tk.END, item[1])
        entry_title.delete(0, tk.END)
        entry_title.insert(tk.END, item[2])
        entry_year.delete(0, tk.END)
        entry_year.insert(tk.END, item[3])

# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Livros")
root.geometry("800x600")
root.config(bg="#f9f9f9")

# Título do app
label_title = tk.Label(root, text="Cadastro de Livros", font=("Arial", 24, "bold"), fg="#3f51b5", bg="#f9f9f9")
label_title.pack(pady=10)

# Frame de formulário
frame_form = tk.Frame(root, bg="#fff", padx=20, pady=20, relief=tk.GROOVE, borderwidth=2)
frame_form.pack(pady=10)

# Labels e campos de entrada
tk.Label(frame_form, text="Nome do Autor:", font=("Arial", 14), bg="#fff").grid(row=0, column=0, sticky="w")
entry_author = tk.Entry(frame_form, font=("Arial", 14), width=30)
entry_author.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Título do Livro:", font=("Arial", 14), bg="#fff").grid(row=1, column=0, sticky="w")
entry_title = tk.Entry(frame_form, font=("Arial", 14), width=30)
entry_title.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Ano de Publicação:", font=("Arial", 14), bg="#fff").grid(row=2, column=0, sticky="w")
entry_year = tk.Entry(frame_form, font=("Arial", 14), width=10)
entry_year.grid(row=2, column=1, padx=10, pady=5)

# Botões de ações
btn_add = tk.Button(frame_form, text="Cadastrar Livro", font=("Arial", 14), bg="#3f51b5", fg="white", command=add_book)
btn_add.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

btn_edit = tk.Button(frame_form, text="Editar Livro", font=("Arial", 14), bg="#ff9800", fg="white", command=edit_book)
btn_edit.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

btn_delete = tk.Button(frame_form, text="Excluir Livro", font=("Arial", 14), bg="#f44336", fg="white", command=delete_book)
btn_delete.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

# Barra de busca
tk.Label(root, text="Buscar:", font=("Arial", 14), bg="#f9f9f9").pack(pady=5)
search_entry = tk.Entry(root, font=("Arial", 14), width=40)
search_entry.pack(pady=5)

# Adicionar botão de busca
btn_search = tk.Button(root, text="Buscar", font=("Arial", 14), bg="#3f51b5", fg="white", command=search_books)
btn_search.pack(pady=5)

# Tabela de livros
tree = ttk.Treeview(root, columns=("ID", "Autor", "Título", "Ano"), show="headings", height=10)
tree.heading("ID", text="ID")
tree.heading("Autor", text="Autor")
tree.heading("Título", text="Título")
tree.heading("Ano", text="Ano")
tree.column("ID", width=50)
tree.column("Autor", width=150)
tree.column("Título", width=200)
tree.column("Ano", width=100)
tree.pack(pady=10)

# Evento de clique na tabela
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Carregar dados na tabela
load_books()

# Configuração final e loop da interface
root.mainloop()

# Fechar a conexão com o banco ao sair
conn.close()
