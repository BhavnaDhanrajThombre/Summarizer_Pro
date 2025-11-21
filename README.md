# Smart Summarizer Pro

Smart Summarizer Pro is a desktop application built with Tkinter that allows users to extract text from PDFs, load images for preview/editing, generate extractive summaries, visualize keyword frequencies, and listen to summaries through text-to-speech.
It is designed to make studying, reviewing documents, and analyzing content faster and more intuitive.

## Features

PDF Text Extraction
Extractive Summarization with keyword highlighting
Image Preview + Rotate + Resize
Keyword Frequency Visualization
Text-to-Speech with adjustable speed & volume
Light/Dark Mode
Copy & Save Summary

## Installation

1. Clone the repository
   
git clone <https://github.com/BhavnaDhanrajThombre/Summarizer_Pro.git>
cd SummarizerPro

2. Install dependencies
   
Ensure you have Python 3.8+ installed.

pip install PyPDF2 pillow matplotlib pyttsx3

How to Run
python app.py

## Dependencies
Library	Purpose
Tkinter	GUI framework
PyPDF2	PDF text extraction
Pillow (PIL)	Image handling & preview
matplotlib	Visualization
pyttsx3	Offline text-to-speech
collections.Counter	Keyword frequency processing
