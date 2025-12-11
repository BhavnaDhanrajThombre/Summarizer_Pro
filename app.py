import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import PyPDF2
from PIL import Image, ImageTk, ImageOps
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyttsx3
import threading
import re
from collections import Counter
import math

class SmartSummarizerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Summarizer Pro - Text Extractor & Voice Reader")
        self.root.geometry("1200x800")
        
        # Theme colors
        self.dark_mode = False
        self.colors = {
            'light_bg': '#f0f0f0',
            'light_fg': '#000000',
            'light_btn': '#4CAF50',
            'light_text_bg': '#ffffff',
            'dark_bg': '#2b2b2b',
            'dark_fg': '#ffffff',
            'dark_btn': '#45a049',
            'dark_text_bg': '#1e1e1e'
        }
        
        # Data storage
        self.extracted_text = ""
        self.summary_text = ""
        self.current_image = None
        self.image_label = None
        
        # Voice engine
        self.engine = pyttsx3.init()
        self.voice_speed = 150
        self.voice_volume = 1.0
        
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        self.create_control_panel(main_frame)
        
        # Content area with three columns
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left column - Upload & Image
        self.create_left_panel(content_frame)
        
        # Middle column - Extracted Text
        self.create_middle_panel(content_frame)
        
        # Right column - Summary & Stats
        self.create_right_panel(content_frame)
        
        # Bottom control panel
        self.create_bottom_panel(main_frame)
        
        # Floating help button
        self.create_help_button()
        
    def create_control_panel(self, parent):
        control_frame = tk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title = tk.Label(control_frame, text="📚 Smart Summarizer Pro", 
                        font=("Arial", 18, "bold"))
        title.pack(side=tk.LEFT, padx=10)
        
        # Dark mode toggle
        self.theme_btn = tk.Button(control_frame, text="🌙 Dark Mode", 
                                   command=self.toggle_theme,
                                   font=("Arial", 10), padx=15, pady=5)
        self.theme_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_left_panel(self, parent):
        left_frame = tk.LabelFrame(parent, text="📁 Upload Files", 
                                   font=("Arial", 11, "bold"), padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Upload buttons
        self.pdf_btn = tk.Button(left_frame, text="📄 Upload PDF", 
                                command=self.upload_pdf,
                                font=("Arial", 10), pady=8)
        self.pdf_btn.pack(fill=tk.X, pady=5)
        
        self.img_btn = tk.Button(left_frame, text="🖼️ Upload Image", 
                                command=self.upload_image,
                                font=("Arial", 10), pady=8)
        self.img_btn.pack(fill=tk.X, pady=5)
        
        # Image preview area
        preview_frame = tk.Frame(left_frame, bg='gray', width=300, height=400)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        preview_frame.pack_propagate(False)
        
        self.image_container = tk.Label(preview_frame, text="No Image Loaded", 
                                       bg='gray', fg='white')
        self.image_container.pack(expand=True)
        
        # Image controls
        img_controls = tk.Frame(left_frame)
        img_controls.pack(fill=tk.X)
        
        self.rotate_btn = tk.Button(img_controls, text="↻", 
                                    command=self.rotate_image,
                                    font=("Arial", 10), width=8)
        self.rotate_btn.pack(side=tk.LEFT, padx=2)
        
        self.resize_btn = tk.Button(img_controls, text="⇔", 
                                   command=self.resize_image,
                                   font=("Arial", 10), width=8)
        self.resize_btn.pack(side=tk.LEFT, padx=2)
        
    def create_middle_panel(self, parent):
        middle_frame = tk.LabelFrame(parent, text="📝 Extracted Text", 
                                     font=("Arial", 11, "bold"), padx=10, pady=10)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.extracted_box = scrolledtext.ScrolledText(middle_frame, 
                                                       wrap=tk.WORD,
                                                       font=("Arial", 10),
                                                       height=20)
        self.extracted_box.pack(fill=tk.BOTH, expand=True)
        
    def create_right_panel(self, parent):
        right_frame = tk.LabelFrame(parent, text="✨ Summary & Insights", 
                                    font=("Arial", 11, "bold"), padx=10, pady=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Stats display
        stats_frame = tk.Frame(right_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = tk.Label(stats_frame, 
                                    text="📊 Words: 0 | Summary: 0 | Ratio: 0%",
                                    font=("Arial", 9))
        self.stats_label.pack()
        
        # Summary box
        self.summary_box = scrolledtext.ScrolledText(right_frame, 
                                                     wrap=tk.WORD,
                                                     font=("Arial", 10),
                                                     height=15)
        self.summary_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Summary controls
        summary_controls = tk.Frame(right_frame)
        summary_controls.pack(fill=tk.X)
        
        self.copy_btn = tk.Button(summary_controls, text="📋 Copy", 
                                 command=self.copy_summary,
                                 font=("Arial", 9), width=10)
        self.copy_btn.pack(side=tk.LEFT, padx=2)
        
        self.save_btn = tk.Button(summary_controls, text="💾 Save", 
                                 command=self.save_summary,
                                 font=("Arial", 9), width=10)
        self.save_btn.pack(side=tk.LEFT, padx=2)
        
    def create_bottom_panel(self, parent):
        bottom_frame = tk.Frame(parent)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Main action buttons
        action_frame = tk.Frame(bottom_frame)
        action_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.summarize_btn = tk.Button(action_frame, text="🎯 Generate Summary", 
                                       command=self.generate_summary,
                                       font=("Arial", 11, "bold"), pady=10)
        self.summarize_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.speak_btn = tk.Button(action_frame, text="🔊 Speak Summary", 
                                   command=self.speak_summary,
                                   font=("Arial", 11, "bold"), pady=10)
        self.speak_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.viz_btn = tk.Button(action_frame, text="📊 Visualize", 
                                command=self.show_visualization,
                                font=("Arial", 11, "bold"), pady=10)
        self.viz_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Voice controls
        voice_frame = tk.LabelFrame(bottom_frame, text="🎤 Voice Settings", 
                                   font=("Arial", 9, "bold"), padx=10, pady=5)
        voice_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Speed control
        speed_frame = tk.Frame(voice_frame)
        speed_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(speed_frame, text="Speed:", font=("Arial", 8)).pack()
        self.speed_scale = tk.Scale(speed_frame, from_=50, to=250, 
                                   orient=tk.HORIZONTAL, length=100,
                                   command=self.update_speed)
        self.speed_scale.set(150)
        self.speed_scale.pack()
        
        # Volume control
        volume_frame = tk.Frame(voice_frame)
        volume_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(volume_frame, text="Volume:", font=("Arial", 8)).pack()
        self.volume_scale = tk.Scale(volume_frame, from_=0, to=100, 
                                    orient=tk.HORIZONTAL, length=100,
                                    command=self.update_volume)
        self.volume_scale.set(100)
        self.volume_scale.pack()
        
    def create_help_button(self):
        help_btn = tk.Button(self.root, text="❓", 
                            command=self.show_help,
                            font=("Arial", 12, "bold"),
                            width=3, height=1)
        help_btn.place(relx=0.98, rely=0.02, anchor='ne')
        
    def upload_pdf(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.show_progress("Extracting PDF...")
            threading.Thread(target=self.extract_pdf_text, 
                           args=(file_path,), daemon=True).start()
            
    def extract_pdf_text(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                self.extracted_text = text
                self.root.after(0, self.display_extracted_text)
                self.root.after(0, self.hide_progress)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, self.hide_progress)
            
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.load_image(file_path)
            
    def load_image(self, file_path):
        try:
            self.current_image = Image.open(file_path)
            self.display_image()
            messagebox.showinfo("Success", "Image loaded! Use rotate/resize buttons.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def display_image(self):
        if self.current_image:
            # Resize to fit preview
            img_copy = self.current_image.copy()
            img_copy.thumbnail((280, 380), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img_copy)
            self.image_container.configure(image=photo, text="")
            self.image_container.image = photo
            
    def rotate_image(self):
        if self.current_image:
            self.current_image = self.current_image.rotate(90, expand=True)
            self.display_image()
            
    def resize_image(self):
        if self.current_image:
            width, height = self.current_image.size
            new_size = (int(width * 0.8), int(height * 0.8))
            self.current_image = self.current_image.resize(new_size)
            self.display_image()
            
    def display_extracted_text(self):
        self.extracted_box.delete(1.0, tk.END)
        self.extracted_box.insert(1.0, self.extracted_text)
        self.update_stats()
        
    def generate_summary(self):
        if not self.extracted_text.strip():
            messagebox.showwarning("Warning", "No text to summarize!")
            return
            
        self.show_progress("Generating summary...")
        threading.Thread(target=self.create_summary, daemon=True).start()
        
    def create_summary(self):
        try:
            # Simple extractive summarization
            sentences = re.split(r'[.!?]+', self.extracted_text)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
            
            if not sentences:
                self.root.after(0, lambda: messagebox.showwarning(
                    "Warning", "Not enough content to summarize!"))
                self.root.after(0, self.hide_progress)
                return
            
            # Calculate word frequencies
            words = re.findall(r'\b[a-z]+\b', self.extracted_text.lower())
            stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 
                         'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by'}
            words = [w for w in words if w not in stop_words]
            word_freq = Counter(words)
            
            # Score sentences
            sentence_scores = {}
            for sentence in sentences:
                score = 0
                sentence_words = re.findall(r'\b[a-z]+\b', sentence.lower())
                for word in sentence_words:
                    if word in word_freq:
                        score += word_freq[word]
                if len(sentence_words) > 0:
                    sentence_scores[sentence] = score / len(sentence_words)
            
            # Get top sentences
            num_sentences = max(3, len(sentences) // 5)
            top_sentences = sorted(sentence_scores.items(), 
                                 key=lambda x: x[1], reverse=True)[:num_sentences]
            
            # Order by appearance
            summary_sentences = sorted(top_sentences, 
                                     key=lambda x: sentences.index(x[0]))
            self.summary_text = '. '.join([s[0] for s in summary_sentences]) + '.'
            
            # Get keywords for highlighting
            self.keywords = [word for word, count in word_freq.most_common(10)]
            
            self.root.after(0, self.display_summary)
            self.root.after(0, self.hide_progress)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, self.hide_progress)
            
    def display_summary(self):
        self.summary_box.delete(1.0, tk.END)
        self.summary_box.insert(1.0, self.summary_text)
        
        # Highlight keywords
        self.summary_box.tag_configure("highlight", background="yellow", 
                                      foreground="black")
        
        for keyword in self.keywords[:5]:  # Top 5 keywords
            start_idx = '1.0'
            while True:
                start_idx = self.summary_box.search(keyword, start_idx, 
                                                   stopindex=tk.END, nocase=True)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(keyword)}c"
                self.summary_box.tag_add("highlight", start_idx, end_idx)
                start_idx = end_idx
                
        self.update_stats()
        messagebox.showinfo("Success", "Summary generated with highlighted keywords!")
        
    def update_stats(self):
        orig_words = len(self.extracted_text.split())
        summ_words = len(self.summary_text.split()) if self.summary_text else 0
        ratio = (summ_words / orig_words * 100) if orig_words > 0 else 0
        
        self.stats_label.config(
            text=f"📊 Original: {orig_words} words | Summary: {summ_words} words | Compression: {ratio:.1f}%"
        )
        
    def speak_summary(self):
        if not self.summary_text.strip():
            messagebox.showwarning("Warning", "No summary to speak!")
            return
            
        threading.Thread(target=self.do_speak, daemon=True).start()
        
    def do_speak(self):
        try:
            self.engine.setProperty('rate', self.voice_speed)
            self.engine.setProperty('volume', self.voice_volume)
            self.engine.say(self.summary_text)
            self.engine.runAndWait()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            
    def update_speed(self, val):
        self.voice_speed = int(val)
        
    def update_volume(self, val):
        self.voice_volume = float(val) / 100
        
    def copy_summary(self):
        if self.summary_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.summary_text)
            messagebox.showinfo("Success", "Summary copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No summary to copy!")
            
    def save_summary(self):
        if not self.summary_text:
            messagebox.showwarning("Warning", "No summary to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.summary_text)
                messagebox.showinfo("Success", "Summary saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def show_visualization(self):
        if not self.summary_text:
            messagebox.showwarning("Warning", "Generate a summary first!")
            return
            
        # Get top keywords
        words = re.findall(r'\b[a-z]+\b', self.extracted_text.lower())
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 
                     'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by'}
        words = [w for w in words if w not in stop_words and len(w) > 3]
        word_freq = Counter(words).most_common(8)
        
        if not word_freq:
            messagebox.showinfo("Info", "Not enough keywords to visualize!")
            return
            
        # Create visualization window
        viz_window = tk.Toplevel(self.root)
        viz_window.title("📊 Keyword Frequency Analysis")
        viz_window.geometry("700x500")
        
        fig, ax = plt.subplots(figsize=(8, 5))
        keywords = [item[0] for item in word_freq]
        frequencies = [item[1] for item in word_freq]
        
        bars = ax.bar(keywords, frequencies, color='#4CAF50', alpha=0.8)
        ax.set_xlabel('Keywords', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Top Keywords in Your Document', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
    def apply_theme(self):
        if self.dark_mode:
            bg = self.colors['dark_bg']
            fg = self.colors['dark_fg']
            btn_bg = self.colors['dark_btn']
            text_bg = self.colors['dark_text_bg']
            self.theme_btn.config(text="☀️ Light Mode")
        else:
            bg = self.colors['light_bg']
            fg = self.colors['light_fg']
            btn_bg = self.colors['light_btn']
            text_bg = self.colors['light_text_bg']
            self.theme_btn.config(text="🌙 Dark Mode")
            
        self.root.configure(bg=bg)
        
        # Update all widgets
        for widget in self.root.winfo_children():
            self.update_widget_theme(widget, bg, fg, btn_bg, text_bg)
            
    def update_widget_theme(self, widget, bg, fg, btn_bg, text_bg):
        widget_type = widget.winfo_class()
        
        try:
            if widget_type in ['Frame', 'Labelframe']:
                widget.configure(bg=bg)
                if widget_type == 'Labelframe':
                    widget.configure(fg=fg)
            elif widget_type == 'Label':
                widget.configure(bg=bg, fg=fg)
            elif widget_type == 'Button':
                widget.configure(bg=btn_bg, fg='white', activebackground=btn_bg)
            elif widget_type in ['Text', 'ScrolledText']:
                widget.configure(bg=text_bg, fg=fg, insertbackground=fg)
        except:
            pass
            
        # Recursively update children
        for child in widget.winfo_children():
            self.update_widget_theme(child, bg, fg, btn_bg, text_bg)
            
    def show_progress(self, message):
        # Simple progress indication
        self.root.config(cursor="wait")
        self.root.update()
        
    def hide_progress(self):
        self.root.config(cursor="")
        
    def show_help(self):
        help_text = """
🎯 SMART SUMMARIZER PRO - HELP GUIDE

📁 UPLOADING:
• Click "Upload PDF" to load PDF documents
• Click "Upload Image" to load and preview images
• Extracted text appears in the middle panel

✨ SUMMARIZATION:
• Click "Generate Summary" to create an intelligent summary
• Key terms are automatically highlighted in yellow
• View word counts and compression ratio above summary

🔊 VOICE FEATURES:
• Click "Speak Summary" to hear the summary
• Adjust speed (50-250) and volume (0-100) using sliders
• Voice reads in real-time with your custom settings

📊 VISUALIZATION:
• Click "Visualize" to see top keyword frequencies
• Bar chart shows most important terms

🖼️ IMAGE TOOLS:
• Use ↻ to rotate image 90 degrees
• Use ⇔ to resize image smaller

💾 SAVING & COPYING:
• Click "Copy" to copy summary to clipboard
• Click "Save" to export summary as text file

🌙 THEME:
• Toggle between Light and Dark mode anytime

Enjoy your enhanced study experience! 🚀
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help & Instructions")
        help_window.geometry("600x500")
        
        help_text_widget = scrolledtext.ScrolledText(help_window, 
                                                     wrap=tk.WORD,
                                                     font=("Arial", 10),
                                                     padx=20, pady=20)
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartSummarizerPro(root)
    root.mainloop()