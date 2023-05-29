import json
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QColorDialog


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


class FlashcardCreator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mat's Lernkarten ersteller")
        self.setGeometry(100, 100, 400, 800)
        self.setStyleSheet("background-color: #F3EFEF;")

        # Schriftgröße
        self.font_size = 12

        # Hintergrundfarbe
        self.bg_color = "#F3EFEF"

        # Label und Textfeld für Frage
        self.label_question = QtWidgets.QLabel("Frage:", self)
        self.label_question.setFont(QtGui.QFont("Verdana", self.font_size))
        self.label_question.move(20, 10)

        self.entry_question = QtWidgets.QLineEdit(self)
        self.entry_question.setFont(QtGui.QFont("Verdana", self.font_size))
        self.entry_question.setGeometry(20, 40, 360, 30)
        self.entry_question.setStyleSheet("background-color: #E1DADA; color: #3D3D3D;")

        # Label und Textfeld für Antwort
        self.label_answer = QtWidgets.QLabel("Antwort:", self)
        self.label_answer.setFont(QtGui.QFont("Verdana", self.font_size))
        self.label_answer.move(20, 90)

        self.entry_answer = QtWidgets.QLineEdit(self)
        self.entry_answer.setFont(QtGui.QFont("Verdana", self.font_size))
        self.entry_answer.setGeometry(20, 120, 360, 30)
        self.entry_answer.setStyleSheet("background-color: #E1DADA; color: #3D3D3D;")

        # Label und Textfeld für Suche
        self.label_search = QtWidgets.QLabel("Suche:", self)
        self.label_search.setFont(QtGui.QFont("Verdana", self.font_size))
        self.label_search.move(20, 170)

        self.entry_search = QtWidgets.QLineEdit(self)
        self.entry_search.setFont(QtGui.QFont("Verdana", self.font_size))
        self.entry_search.setGeometry(20, 200, 360, 30)
        self.entry_search.setStyleSheet("background-color: #E1DADA; color: #3D3D3D;")

        # Button zum Speichern der Lernkarte
        self.button_save = QtWidgets.QPushButton("Speichern", self)
        self.button_save.setFont(QtGui.QFont("Verdana", self.font_size))
        self.button_save.setGeometry(20, 250, 360, 30)
        self.button_save.setStyleSheet("background-color: #FFCD5C; color: #3D3D3D;")
        self.button_save.clicked.connect(self.save_flashcard)

        # Button zum Auswählen einer Lernkarte zum Bearbeiten hinzufügen
        self.button_select = QtWidgets.QPushButton("Lernkarte auswählen", self)
        self.button_select.setFont(QtGui.QFont("Verdana", self.font_size))
        self.button_select.setGeometry(20, 300, 360, 30)
        self.button_select.setStyleSheet("background-color: #FFCD5C; color: #3D3D3D;")
        self.button_select.clicked.connect(self.select_flashcard)

        # Button für die Suche
        self.button_search = QtWidgets.QPushButton("Suchen", self)
        self.button_search.setFont(QtGui.QFont("Verdana", self.font_size))
        self.button_search.setGeometry(20, 350, 360, 30)
        self.button_search.setStyleSheet("background-color: #FFCD5C; color: #3D3D3D;")
        self.button_search.clicked.connect(self.search_flashcards)

        # Button zum Ändern der Schriftgröße
        self.button_font_size = QtWidgets.QPushButton("Schriftgröße ändern", self)
        self.button_font_size.setFont(QtGui.QFont("Verdana", self.font_size))
        self.button_font_size.setGeometry(20, 400, 360, 30)
        self.button_font_size.setStyleSheet("background-color: #FFCD5C; color: #3D3D3D;")
        self.button_font_size.clicked.connect(self.change_font_size)

        # Button zum Ändern der Hintergrundfarbe
        self.button_bg_color = QtWidgets.QPushButton("Hintergrundfarbe ändern", self)
        self.button_bg_color.setFont(QtGui.QFont("Verdana", self.font_size))
        self.button_bg_color.setGeometry(20, 450, 360, 30)
        self.button_bg_color.setStyleSheet("background-color: #FFCD5C; color: #3D3D3D;")
        self.button_bg_color.clicked.connect(self.change_bg_color)

    def select_flashcard(self):
        # Neue Dialog erstellen, um eine Lernkarte auszuwählen
        self.top_level = QtWidgets.QDialog()
        self.top_level.setWindowTitle("Lernkarte auswählen")
        self.top_level.setGeometry(200, 200, 400, 400)
        self.top_level.setStyleSheet("background-color: #F3EFEF;")

        # Liste der Lernkarten laden
        try:
            with open("flashcards.json", "r") as f:
                data = [json.loads(line) for line in f]
        except FileNotFoundError:
            data = []

        # Dropdown-Menü mit den vorhandenen Lernkarten erstellen
        self.selected_flashcard = QtWidgets.QComboBox(self.top_level)
        self.selected_flashcard.setGeometry(20, 20, 360, 30)
        self.selected_flashcard.setStyleSheet("background-color: #E1DADA; color: #3D3D3D;")
        self.selected_flashcard.addItems([card["question"] for card in data])

        # Button zum Laden der ausgewählten Lernkarte hinzufügen
        self.button_load = QtWidgets.QPushButton("Lernkarte laden", self.top_level)
        self.button_load.setFont(QtGui.QFont("Verdana", 12))
        self.button_load.setGeometry(20, 70, 360, 30)
        self.button_load.setStyleSheet("background-color: #FFCD5C; color: #3D3D3D;")
        self.button_load.clicked.connect(self.load_flashcard)

        self.top_level.exec_()

    def search_flashcards(self):
        search_term = self.entry_search.text()
        try:
            with open("flashcards.json", "r") as f:
                data = [json.loads(line) for line in f]
        except FileNotFoundError:
            data = []
        matching_flashcards = [card for card in data if search_term in card["question"]]

        if matching_flashcards:
            # Neue Dialog erstellen, um die übereinstimmenden Lernkarten anzuzeigen
            self.top_level = QtWidgets.QDialog()
            self.top_level.setWindowTitle("Suchergebnisse")
            self.top_level.setGeometry(200, 200, 400, 400)
            self.top_level.setStyleSheet("background-color: #F3EFEF;")

            # Dropdown-Menü mit den übereinstimmenden Lernkarten erstellen
            self.selected_flashcard = QtWidgets.QComboBox(self.top_level)
            self.selected_flashcard.setGeometry(20, 20, 360, 30)
            self.selected_flashcard.setStyleSheet("background-color: #E1DADA; color: #3D3D3D;")
            self.selected_flashcard.addItems([card["question"] for card in matching_flashcards])

            # Button zum Laden der ausgewählten Lernkarte hinzufügen
            self.button_load = QtWidgets.QPushButton("Lernkarte laden", self.top_level)
            self.button_load.setFont(QtGui.QFont("Verdana", 12))
            self.button_load.setGeometry(20, 70, 360, 30)
            self.button_load.setStyleSheet("background-color: #FFCD5C; color: #3D3D3D;")
            self.button_load.clicked.connect(self.load_flashcard)

            self.top_level.exec_()
        else:
            QtWidgets.QMessageBox.warning(
                self, "Keine Treffer", "Es wurden keine übereinstimmenden Lernkarten gefunden.")

    def load_flashcard(self):
        # Ausgewählte Lernkarte aus den Daten laden
        with open("flashcards.json", "r") as f:
            data = [json.loads(line) for line in f]
        selected_question = self.selected_flashcard.currentText()
        selected_flashcard = next(
            (card for card in data if card["question"] == selected_question), None)

        if selected_flashcard:
            # Textfelder mit der ausgewählten Lernkarte füllen
            self.entry_question.setText(selected_flashcard["question"])
            self.entry_answer.setText(selected_flashcard["answer"])
            # Dialog schließen
            self.top_level.close()
        else:
            QtWidgets.QMessageBox.warning(
                self, "Fehler", "Die ausgewählte Lernkarte konnte nicht geladen werden.")

    def save_flashcard(self):
        # Lernkarten als Python-Datenstruktur speichern
        flashcard = {
            "question": self.entry_question.text(),
            "answer": self.entry_answer.text()
        }

        # Überprüfen, ob die Lernkarte bereits vorhanden ist
        if check_duplicate(flashcard["question"], flashcard["answer"], "flashcards.json"):
            QtWidgets.QMessageBox.warning(
                self, "Duplikat", "Diese Lernkarte existiert bereits.")
            return

        with open("flashcards.json", "a") as f:
            json.dump(flashcard, f)
            f.write("\n")

        # Textfelder leeren
        self.entry_question.clear()
        self.entry_answer.clear()

        # Nachricht anzeigen, dass die Lernkarte gespeichert wurde
        QtWidgets.QMessageBox.information(
            self, "Erfolg", "Die Lernkarte wurde erfolgreich gespeichert!")

    def change_font_size(self):
        # Neue Dialog erstellen, um nach neuer Schriftgröße zu fragen
        new_size, ok = QtWidgets.QInputDialog.getInt(
            self, "Font Size", "Enter the new font size:")
        
        # Wenn gültige Eingabe einer Schriftgröße erfolgt ist, ändere die Schriftgröße für alle Widgets
        if ok:
            self.font_size = new_size
            self.label_question.setFont(QtGui.QFont("Verdana", self.font_size))
            self.entry_question.setFont(QtGui.QFont("Verdana", self.font_size))
            self.label_answer.setFont(QtGui.QFont("Verdana", self.font_size))
            self.entry_answer.setFont(QtGui.QFont("Verdana", self.font_size))
            self.label_search.setFont(QtGui.QFont("Verdana", self.font_size))
            self.entry_search.setFont(QtGui.QFont("Verdana", self.font_size))
            self.button_save.setFont(QtGui.QFont("Verdana", self.font_size))
            self.button_select.setFont(QtGui.QFont("Verdana", self.font_size))
            self.button_search.setFont(QtGui.QFont("Verdana", self.font_size))
            self.button_font_size.setFont(QtGui.QFont("Verdana", self.font_size))
            self.button_bg_color.setFont(QtGui.QFont("Verdana", self.font_size))
    
    def change_bg_color(self):
        # Dialog zur Farbauswahl öffnen
        color = QtWidgets.QColorDialog.getColor()

        # Wenn eine Farbe ausgewählt wurde, ändere die Hintergrundfarbe des Hauptfensters
        if color.isValid():
            self.bg_color = color.name()
            self.setStyleSheet(f"background-color: {self.bg_color};")
            

app = QtWidgets.QApplication([])
window = FlashcardCreator()
window.show()
app.exec_()
