import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Создание и работа с главным окном
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7d7", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

####################################################################################### КНОПКИ

        # ДОБАВИТЬ
        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_add = tk.Button(
            toolbar, bg="#d7d7d7", bd=0, image=self.add_img, command=self.open_child
        )
        btn_add.pack(side=tk.LEFT)

        # РЕДАКТИРОВАТЬ
        self.upd_img = tk.PhotoImage(file="./img/update.png")
        btn_upd = tk.Button(
            toolbar, bg="#d7d7d7", bd=0, image=self.upd_img, command=self.open_upd
        )
        btn_upd.pack(side=tk.LEFT)

        # УДАЛИТЬ
        self.del_img = tk.PhotoImage(file="./img/delete.png")
        btn_del = tk.Button(
            toolbar, bg="#d7d7d7", bd=0, image=self.del_img, command=self.delete_records
        )
        btn_del.pack(side=tk.LEFT)

        # ПОИСК
        self.ser_img = tk.PhotoImage(file="./img/search.png")
        btn_ser = tk.Button(
            toolbar, bg="#d7d7d7", bd=0, image=self.ser_img, command=self.open_search
        )
        btn_ser.pack(side=tk.LEFT)
        
        
        # ПОИСК
        self.ref_img = tk.PhotoImage(file="./img/refresh.png")
        btn_ref = tk.Button(
            toolbar, bg="#d7d7d7", bd=0, image=self.ref_img, command=self.view_records
        )
        btn_ref.pack(side=tk.LEFT)

####################################################################################### ТАБЛИЦА 

        # Добавляем таблицы
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "phone", "email"), height=45, show="headings"
        )

        # Добавить параметры колонкам
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="E-mail")

        # Упаковка
        self.tree.pack(side=tk.LEFT)
        
        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

#######################################################################################

    #
    def records(self, name, phone, email):
        self.db.insert_date(name, phone, email)
        self.view_records()

    # просмотр вех данных
    def view_records(self):
        self.db.cur.execute(""" SELECT * FROM Contacts""")

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cur.fetchall()]

    # обновление данных
    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], "#1")
        self.db.cur.execute(
            """UPDATE Contacts SET name=?,  phone=?,  email=? WHERE id=?""",
            (name, phone, email, id),
        )
        self.db.conn.commit()
        self.view_records()

    # удаляет данные
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute(
                """DELETE FROM Contacts WHERE id=?""", (self.tree.set(row, "#1"),)
            )
            self.db.conn.commit()
            self.view_records()

    # поиск данных
    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cur.execute("""SELECT * FROM Contacts WHERE name LIKE ?""", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cur.fetchall()]

####################################################################################### ДОЧЕРНИЕ ОКНА

    # вызывает окно добавления
    def open_child(self):
        Child()

    # вызывает окно редактирования
    def open_upd(self):
        Update()

    # вызывает окно удаления
    def open_search(self):
        Search()


#######################################################################################

# создание окна Добавления
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Создание и работа с дочерним окном
    def init_child(self):
        self.title("Добавить")
        self.geometry("400x200")
        # перехватываем все события происходящие в приложении
        self.grab_set()
        # захватывает фокус
        self.focus_set()

        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text="Телефон")
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text="E-mail")
        label_email.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # Кнопка добавления
        self.btn_add = ttk.Button(self, text="Добавить")
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_phone.get(), self.entry_email.get()
            ),
        )


#######################################################################################

# создание окна Редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title("Редактировать")
        self.btn_add.destroy

        self.btn_upd = ttk.Button(self, text="Редактировать")
        self.btn_upd.bind(
            "<Button-1>",
            lambda event: self.view.update_record(
                self.entry_name.get(), self.entry_phone.get(), self.entry_email.get()
            ),
        )
        self.btn_upd.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_upd.place(x=200, y=170)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], "#1")
        self.db.cur.execute("""SELECT * FROM Contacts WHERE id=?""", (id,))

        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

#######################################################################################

# создание окна Поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Поиск по контактам")
        self.geometry("300x100")
        self.resizable(False, False)
        # перехватываем все события происходящие в приложении
        self.grab_set()
        # захватывает фокус
        self.focus_set()

        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

        # кнопка закрытия
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=170, y=70)

        # кнопка поиска
        self.btn_search = ttk.Button(self, text="Найти")
        self.btn_search.place(x=80, y=70)
        self.btn_search.bind(
            "<Button-1>", lambda event: self.view.search_records(self.entry_name.get())
        )
        self.btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")

#######################################################################################

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("contacts.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            """ CREATE TABLE IF NOT EXISTS Contacts (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                phone TEXT NOT NULL,
                                email TEXT  ) """
        )
        self.conn.commit()

    def insert_date(self, name, phone, email):
        self.cur.execute(
            """ INSERT INTO Contacts (name, phone, email)
                         VALUES (?,?,?)""",
            (name, phone, email),
        )
        self.conn.commit()


####################################################################################### СОЗДАНИЕ ОКНА
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Телефонная книга")
    root.geometry("645x450")
    root.resizable(False, False)
    root.configure(bg="White")
    root.mainloop()
