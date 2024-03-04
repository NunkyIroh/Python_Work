import csv
from datetime import datetime

class DateChooser:
    def choose_date(self):
        selected_date = input("Выберите дату (в формате ДД-ММ-ГГГГ): ")
        try:
            selected_datetime = datetime.strptime(selected_date, "%d-%m-%Y")
            return selected_datetime
        except ValueError:
            print("Ошибка: Некорректный формат даты.")
            return None

class NoteApp:
    def __init__(self):
        self.notes = []
        self.load_notes()

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

    def create_note(self):
        title = input("Введите название заметки: ")
        body = input("Введите содержание заметки: ")
        created_at = datetime.now().strftime("%d-%m-%Y %H:%M")
        new_id = self.get_unique_id()
        new_note = [str(new_id), title, body, created_at.split()[0], created_at.split()[1]]
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно создана.")

    def get_unique_id(self):
        existing_ids = {int(note[0]) for note in self.notes}
        new_id = 1
        while new_id in existing_ids:
            new_id += 1
        return new_id

    def edit_note(self):
        note_id = int(input("Введите ID заметки, которую хотите отредактировать: "))
        found = False
        for note in self.notes:
            if int(note[0]) == note_id:
                new_title = input("Введите новое название заметки: ")
                new_body = input("Введите новое содержание заметки: ")
                note[1] = new_title
                note[2] = new_body
                note[3] = datetime.now().strftime("%d-%m-%Y")
                note[4] = datetime.now().strftime("%H:%M")
                self.save_notes()
                found = True
                print("Заметка успешно отредактирована.")
                break
        if not found:
            print("Заметка с указанным ID не найдена.")

    def delete_note(self):
        note_id = int(input("Введите ID заметки, которую хотите удалить: "))
        found = False
        for note in self.notes:
            if int(note[0]) == note_id:
                confirmation = input("Вы уверены, что хотите удалить заметку? (y/n): ")
                if confirmation.lower() == 'y':
                    self.notes.remove(note)
                    self.save_notes()
                    found = True
                    print("Заметка успешно удалена.")
                else:
                    print("Удаление отменено.")
                break
        if not found:
            print("Заметка с указанным ID не найдена.")
            
    def show_full_content(self):
        note_id = input("Введите ID заметки, полное содержание которой хотите просмотреть: ")
        found = False
        for note in self.notes:
            if note[0] == note_id:
                print("Полное содержание заметки:")
                print(f"Название: {note[1]}")
                print(f"Содержание: {note[2]}")
                print(f"Дата создания: {note[3]}")
                print(f"Время создания: {note[4]}")
                found = True
                break
        if not found:
            print("Заметка с указанным ID не найдена.")

    def choose_date(self):
        date_chooser = DateChooser()
        selected_date = date_chooser.choose_date()
        if selected_date:
            self.filter_notes_by_date(selected_date)

    def filter_notes_by_date(self, selected_date):
        formatted_selected_date = selected_date.strftime("%d-%m-%Y")
        filtered_notes = [note for note in self.notes if note[3] == formatted_selected_date]
        print("Заметки на выбранную дату:")
        for note in filtered_notes:
            print(note)

    def show_all_notes(self):
        print("Все заметки:")
        for note in self.notes:
            print(note)

def main():
    app = NoteApp()
    while True:
        print("\n1. Создать заметку")
        print("2. Редактировать заметку")
        print("3. Удалить заметку")
        print("4. Показать полное содержание заметки")
        print("5. Выбрать дату")
        print("6. Показать все заметки")
        print("7. Выйти")
        choice = input("Выберите действие: ")
        if choice == '1':
            app.create_note()
        elif choice == '2':
            app.edit_note()
        elif choice == '3':
            app.delete_note()
        elif choice == '4':
            app.show_full_content()
        elif choice == '5':
            app.choose_date()
        elif choice == '6':
            app.show_all_notes()
        elif choice == '7':
            print("До свидания!")
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите существующее действие.")

if __name__ == "__main__":
    main()
