# Flashcard Creator

This tool allows you to create, save, search, and edit flashcards. The tool is developed using PyQt5 and provides a user interface for easy interaction.

## Features

- Input questions and answers for flashcards
- Save flashcards to a JSON file
- Check for duplicates to avoid creating duplicate flashcards
- Load existing flashcards for editing
- Search for flashcards based on keywords in the questions
- Change the font size for the user interface
- Change the background color of the main window

## Instructions

1. Enter a question in the "Question" text field.
2. Enter the corresponding answer in the "Answer" text field.
3. Click the "Save" button to save the flashcard. It checks for existing duplicates.
4. To edit an existing flashcard, click the "Select Flashcard" button and choose the desired flashcard from the dropdown menu. Then click "Load Flashcard" to load the question and answer into the respective text fields.
5. To search for flashcards, enter a search term in the "Search" text field and click the "Search" button. It will display all flashcards whose question contains the search term.
6. Click the "Change Font Size" button to adjust the font size of the user interface. Enter the desired font size in the displayed dialog.
7. Click the "Change Background Color" button to change the background color of the main window. Select a color from the color selection dialog.

Please note that the flashcards are saved in a JSON file named "flashcards.json". Make sure this file is present in the same directory as the tool.

## Requirements

- Python 3.x
- PyQt5

## Execution

Run the following command to start the tool:

```shell
python FlashcardCreator.py

or

python3 FlashcardCreator.py
```shell



### Author: 

Satisfraction

### License: 

MIT
