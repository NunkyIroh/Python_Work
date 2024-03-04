import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk, filedialog
import csv
from datetime import datetime
from tkcalendar import Calendar  # Добавляем виджет календаря

class DateChooser:
    def __init__(self, parent):
        self.parent = parent
        self.date = None

        self.window = tk.Toplevel(parent)
        self.window.title("Выберите дату")

        self.calendar = Calendar(self.window, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(pady=10)

        select_button = tk.Button(self.window, text="Выбрать", command=self.get_date)
        select_button.pack(pady=5)

    def get_date(self):
        self.date = self.calendar.get_date()
        self.window.destroy()

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Заметки")

        self.notes = []

        self.load_notes()

        self.note_listbox = ttk.Treeview(self.root, columns=("Название заметки", "Дата создания", "Время создания", "Содержание"), show="headings")
        self.note_listbox.heading("Название заметки", text="Название заметки")
        self.note_listbox.heading("Дата создания", text="Дата создания")
        self.note_listbox.heading("Время создания", text="Время создания")
        self.note_listbox.heading("Содержание", text="Содержание")
        self.note_listbox.column("Содержание", anchor="center", width=200)  # Установка ширины столбца
        self.note_listbox.pack(pady=10)

        self.refresh_note_list()

        self.create_button = tk.Button(self.root, text="Создать заметку", command=self.create_note)
        self.create_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Редактировать заметку", command=self.edit_note)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Удалить заметку", command=self.delete_note)
        self.delete_button.pack(pady=5)

        self.show_content_button = tk.Button(self.root, text="Показать полное содержание", command=self.show_full_content)
        self.show_content_button.pack(pady=5)

        self.choose_date_button = tk.Button(self.root, text="Выбрать дату", command=self.choose_date)
        self.choose_date_button.pack(pady=5)

        self.show_all_button = tk.Button(self.root, text="Показать все заметки", command=self.show_all_notes)
        self.show_all_button.pack(pady=5)

    def load_notes(self):
        try:
            with open('notes.csv', 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    self.notes.append(row)
        except FileNotFoundError:
            pass

    def save_notes(self):
        with open('notes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            for note in self.notes:
                writer.writerow(note)

    def refresh_note_list(self):
        self.note_listbox.delete(*self.note_listbox.get_children())
        for note in self.notes:
            self.note_listbox.insert("", "end", values=(note[1], note[3], note[4], note[2]))

    def create_note(self):
        title = simpledialog.askstring("Создать заметку", "Введите название заметки:")
        if title is None:
            return  # Если пользователь нажал "Отмена", прерываем создание заметки

        body = simpledialog.askstring("Создать заметку", "Введите содержание заметки:")
        if body is None:
            return  # Если пользователь нажал "Отмена", прерываем создание заметки

        note_id = len(self.notes) + 1
        created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

        new_note = [note_id, title, body, created_at.split()[0], created_at.split()[1]]  # Убираем отметку о выполнении
        self.notes.append(new_note)
        self.save_notes()
        self.refresh_note_list()

    def edit_note(self):
        selected_item = self.note_listbox.selection()
        if selected_item:
            item_values = self.note_listbox.item(selected_item, "values")
            for note in self.notes:
                if note[1] == item_values[0]:
                    new_title = simpledialog.askstring("Редактировать заметку", "Введите новое название заметки:",
                                                      initialvalue=note[1])
                    if new_title is not None:
                        new_body = simpledialog.askstring("Редактировать заметку", "Введите новое содержание заметки:",
                                                          initialvalue=note[2])
                        if new_body is not None:
                            note[1] = new_title
                            note[2] = new_body
                            note[3] = datetime.now().strftime("%d-%m-%Y")
                            note[4] = datetime.now().strftime("%H:%M")
                            self.save_notes()
                            self.refresh_note_list()
        else:
            messagebox.showwarning("Ошибка", "Выберите заметку для редактирования")

    def delete_note(self):
        selected_item = self.note_listbox.selection()
        if selected_item:
            confirmation = messagebox.askyesno("Удалить заметку", "Вы уверены, что хотите удалить заметку?")
            if confirmation:
                item_values = self.note_listbox.item(selected_item, "values")
                for note in self.notes:
                    if note[1] == item_values[0]:
                        self.notes.remove(note)
                        self.save_notes()
                        self.refresh_note_list()
        else:
            messagebox.showwarning("Ошибка", "Выберите заметку для удаления")

    def show_full_content(self):
        selected_item = self.note_listbox.selection()
        if selected_item:
            item = selected_item[0]
            content = self.note_listbox.item(item, "values")[3]
            messagebox.showinfo("Полное содержание", content)
        else:
            messagebox.showwarning("Ошибка", "Выберите заметку для просмотра полного содержания")

    def choose_date(self):
        date_chooser = DateChooser(self.root)
        self.root.wait_window(date_chooser.window)
        selected_date = date_chooser.date
        if selected_date:
            # Преобразуем выбранную дату в объект datetime перед использованием
            selected_datetime = datetime.strptime(selected_date, "%m/%d/%y")
            # Загружаем все записи перед фильтрацией
            self.notes.clear()
            self.load_notes()
            self.filter_notes_by_date(selected_datetime)


    def filter_notes_by_date(self, selected_date):
        formatted_selected_date = selected_date.strftime("%d-%m-%Y")
        filtered_notes = [note for note in self.notes if note[3] == formatted_selected_date]
        self.notes.clear()
        self.notes = filtered_notes
        self.refresh_note_list()

    def show_all_notes(self):
        # Очистка списка всех заметок
        self.notes.clear()
        self.load_notes()
        self.refresh_note_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
