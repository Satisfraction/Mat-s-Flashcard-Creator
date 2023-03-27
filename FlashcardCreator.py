import tkinter as tk
import json
from tkinter import messagebox, simpledialog
from tkinter import colorchooser



def check_duplicate(question, answer, file_path):
    try:
        with open(file_path, 'r') as f:
            data = [json.loads(line) for line in f]
    except FileNotFoundError:
        return False

    for card in data:
        if card["question"] == question and card["answer"] == answer:
            return True

    return False


class FlashcardCreator:
    def __init__(self, master):
        self.master = master
        master.geometry("400x800")
        master.title("Mat´s Lernkarten ersteller")
        master.config(bg="#F3EFEF")

        # Schriftgröße
        self.font_size = 12

        # Hintergrundfarbe
        self.bg_color = "#F3EFEF"

        # Label und Textfeld für Frage
        self.label_question = tk.Label(
            master, text="Frage:", font=("Verdana", self.font_size), bg=self.bg_color)
        self.label_question.pack(pady=10)
        self.entry_question = tk.Entry(
            master, width=40, font=("Verdana", self.font_size), bg="#E1DADA", fg="#3D3D3D")
        self.entry_question.pack(pady=5)

        # Label und Textfeld für Antwort
        self.label_answer = tk.Label(
            master, text="Antwort:", font=("Verdana", self.font_size), bg=self.bg_color)
        self.label_answer.pack(pady=10)
        self.entry_answer = tk.Entry(master, width=40, font=(
            "Verdana", self.font_size), bg="#E1DADA", fg="#3D3D3D")
        self.entry_answer.pack(pady=5)

        # Label und Textfeld für Suche
        self.label_search = tk.Label(master, text="Suche:", font=("Verdana", self.font_size), bg=self.bg_color)
        self.label_search.pack(pady=10)
        self.entry_search = tk.Entry(master, width=40, font=("Verdana", self.font_size), bg="#E1DADA", fg="#3D3D3D")
        self.entry_search.pack(pady=5)

        # Button zum Speichern der Lernkarte
        self.button_save = tk.Button(
            master, text="Speichern", command=self.save_flashcard, font=("Verdana", self.font_size), bg="#FFCD5C", fg="#3D3D3D")
        self.button_save.pack(pady=20)

        # Button zum Auswählen einer Lernkarte zum Bearbeiten hinzufügen
        self.button_select = tk.Button(
            master, text="Lernkarte auswählen", command=self.select_flashcard, font=("Verdana", self.font_size), bg="#FFCD5C", fg="#3D3D3D")
        self.button_select.pack(pady=10)

        # Button für die Suche
        self.button_search = tk.Button(master, text="Suchen", command=self.search_flashcards, font=("Verdana", self.font_size), bg="#FFCD5C", fg="#3D3D3D")
        self.button_search.pack(pady=10)

        # Button zum Ändern der Schriftgröße
        self.button_font_size = tk.Button(master, text="Schriftgröße ändern", command=self.change_font_size, font=("Verdana", self.font_size), bg="#FFCD5C", fg="#3D3D3D")
        self.button_font_size.pack(pady=10)
        
        # Button zum Ändern der Hintergrundfarbe
        self.button_bg_color = tk.Button(master, text="Hintergrundfarbe ändern", command=self.change_bg_color, font=("Verdana", self.font_size), bg="#FFCD5C", fg="#3D3D3D")
        self.button_bg_color.pack(pady=10)

    def select_flashcard(self):
        # Neue Toplevel erzeugen, um eine Lernkarte auszuwählen
        self.top_level = tk.Toplevel(self.master)
        self.top_level.geometry("400x400")
        self.top_level.title("Lernkarte auswählen")
        self.top_level.config(bg="#F3EFEF")

        # Liste der Lernkarten laden
        try:
            with open("flashcards.json", "r") as f:
                data = [json.loads(line) for line in f]
        except FileNotFoundError:
            data = []

        # Dropdown-Menü mit den vorhandenen Lernkarten erstellen
        self.selected_flashcard = tk.StringVar(self.top_level)
        self.selected_flashcard.set(data[0]["question"] if data else "")
        self.dropdown_flashcards = tk.OptionMenu(
            self.top_level, self.selected_flashcard, *[card["question"] for card in data])
        self.dropdown_flashcards.pack(pady=10)

        # Button zum Laden der ausgewählten Lernkarte hinzufügen
        self.button_load = tk.Button(
            self.top_level, text="Lernkarte laden", command=self.load_flashcard, font=("Verdana", 12), bg="#FFCD5C", fg="#3D3D3D")
        self.button_load.pack(pady=10)
    
    def search_flashcards(self):
        search_term = self.entry_search.get()
        try:
            with open("flashcards.json", "r") as f:
                data = [json.loads(line) for line in f]
        except FileNotFoundError:
            data = []
        matching_flashcards = [card for card in data if search_term in card["question"]]

        if matching_flashcards:
            # Neue Toplevel erzeugen, um die übereinstimmenden Lernkarten anzuzeigen
            self.top_level = tk.Toplevel(self.master)
            self.top_level.geometry("400x400")
            self.top_level.title("Suchergebnisse")
            self.top_level.config(bg="#F3EFEF")

            # Dropdown-Menü mit den übereinstimmenden Lernkarten erstellen
            self.selected_flashcard = tk.StringVar(self.top_level)
            self.selected_flashcard.set(matching_flashcards[0]["question"])
            self.dropdown_flashcards = tk.OptionMenu(
                self.top_level, self.selected_flashcard, *[card["question"] for card in matching_flashcards])
            self.dropdown_flashcards.pack(pady=10)

            # Button zum Laden der ausgewählten Lernkarte hinzufügen
            self.button_load = tk.Button(
                self.top_level, text="Lernkarte laden", command=self.load_flashcard, font=("Verdana", 12), bg="#FFCD5C", fg="#3D3D3D")
            self.button_load.pack(pady=10)
        else:
            messagebox.showwarning(
                "Keine Treffer", "Es wurden keine übereinstimmenden Lernkarten gefunden.")
        
    def load_flashcard(self):
        # Ausgewählte Lernkarte aus den Daten laden
        with open("flashcards.json", "r") as f:
            data = [json.loads(line) for line in f]
        selected_question = self.selected_flashcard.get()
        selected_flashcard = next(
            (card for card in data if card["question"] == selected_question), None)

        if selected_flashcard:
            # Textfelder mit der ausgewählten Lernkarte füllen
            self.entry_question.delete(0, tk.END)
            self.entry_question.insert(0, selected_flashcard["question"])
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.insert(0, selected_flashcard["answer"])
            # Toplevel-Fenster schließen
            self.top_level.destroy()
        else:
            messagebox.showwarning(
                "Fehler", "Die ausgewählte Lernkarte konnte nicht geladen werden.")
    
    def save_flashcard(self):
        # Lernkarten als Python-Datenstruktur speichern
        flashcard = {
            "question": self.entry_question.get(),
            "answer": self.entry_answer.get()
        }

        # Überprüfen, ob die Lernkarte bereits vorhanden ist
        if check_duplicate(flashcard["question"], flashcard["answer"], "flashcards.json"):
            messagebox.showwarning(
                "Duplikat", "Diese Lernkarte existiert bereits.")
            return

        with open("flashcards.json", "a") as f:
            json.dump(flashcard, f)
            f.write("\n")

        # Textfelder leeren
        self.entry_question.delete(0, tk.END)
        self.entry_answer.delete(0, tk.END)

        # Nachricht anzeigen, dass die Lernkarte gespeichert wurde
        messagebox.showinfo(
            "Erfolg", "Die Lernkarte wurde erfolgreich gespeichert!")
        
    def change_font_size(self):
        # Neue Toplevel erzeugen, um nach neuer Schriftgröße zu fragen
        new_size = tk.simpledialog.askinteger(
            "Font Size", "Enter the new font size:"
        )
        
        # Wenn gültige Eingabe einer Schriftgröße erfolgt ist, ändere die Schriftgröße für alle Widgets
        if new_size is not None:
            self.font_size = new_size
            self.label_question.config(font=("Verdana", self.font_size))
            self.entry_question.config(font=("Verdana", self.font_size))
            self.label_answer.config(font=("Verdana", self.font_size))
            self.entry_answer.config(font=("Verdana", self.font_size))
            self.label_search.config(font=("Verdana", self.font_size))
            self.entry_search.config(font=("Verdana", self.font_size))
            self.button_save.config(font=("Verdana", self.font_size))
            self.button_select.config(font=("Verdana", self.font_size))
            self.button_search.config(font=("Verdana", self.font_size))
            self.button_font_size.config(font=("Verdana", self.font_size))

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.master.config(bg=color)


root = tk.Tk()
app = FlashcardCreator(root)
root.mainloop()
