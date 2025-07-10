import threading
import tkinter as tk
from tkinter import ttk, filedialog, Text, Scrollbar, Button, END
import zipfile
from lxml import etree
import pymupdf as fitz
import re
from collections import Counter

class ComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 File Compare Pro")
        self.root.geometry("1200x700")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="📁 Compare Files", command=self.start_comparison).pack(side=tk.LEFT)

        pane_container = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        pane_container.pack(fill=tk.BOTH, expand=True)

        self.similarity_pane = self._create_text_pane(pane_container, "💚 Similarities", "#f0fff0")
        self.difference_pane = self._create_text_pane(pane_container, "🔍 Differences", "#fff0f0")

    def _create_text_pane(self, parent, title, bg):
        frame = ttk.Frame(parent, width=600)
        header = ttk.Label(frame, text=title, font=('Helvetica', 11, 'bold'), background=bg)
        header.pack(pady=5, fill=tk.X)

        text_widget = Text(frame, wrap=tk.WORD, font=('Consolas', 9), padx=10, pady=10, undo=True, bg=bg)
        scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame.text_widget = text_widget
        parent.add(frame)
        return frame

    def start_comparison(self):
        f1 = filedialog.askopenfilename(title="Select First File")
        if not f1: return
        f2 = filedialog.askopenfilename(title="Select Second File")
        if not f2: return

        self.clear_panes()
        threading.Thread(target=self.self_compare_files, args=(f1, f2), daemon=True).start()

    def self_compare_files(self, f1, f2):
        try:
            self.compare_files(f1, f2)
        except Exception as e:
            self.update_panes(f"⚠️ Comparison Error: {str(e)}", "")

    def clear_panes(self):
        for pane in [self.similarity_pane, self.difference_pane]:
            pane.text_widget.delete(1.0, END)
            pane.text_widget.insert(END, "🔄 Analyzing files...\n")

    def compare_files(self, f1, f2):
        content1 = read_file(f1)
        content2 = read_file(f2)

        words1 = Counter(re.findall(r'\b\w+\b', content1.lower()))
        words2 = Counter(re.findall(r'\b\w+\b', content2.lower()))

        common_words = set(words1.keys()) & set(words2.keys())
        unique_words1 = set(words1.keys()) - set(words2.keys())
        unique_words2 = set(words2.keys()) - set(words1.keys())

        similarities = '\n'.join(f"✔️ {word}" for word in sorted(common_words)) or "⚠️ No significant similarities found"
        differences = '\n'.join(f"❌ {word}" for word in sorted(unique_words1 | unique_words2)) or "✅ No significant differences found"

        total_words = len(words1) + len(words2)
        unique_words_count = len(unique_words1 | unique_words2)
        common_words_count = len(common_words)
        similarity_ratio = (common_words_count / total_words) * 100 if total_words else 0
        dissimilarity_ratio = (unique_words_count / total_words) * 100 if total_words else 0

        header = f"📊 Similarity Ratio: {similarity_ratio:.2f}%\n📊 Dissimilarity Ratio: {dissimilarity_ratio:.2f}%\n\n"
        self.update_panes(similarities, header + differences)

    def update_panes(self, similarities, differences):
        self.similarity_pane.text_widget.delete(1.0, END)
        self.difference_pane.text_widget.delete(1.0, END)
        self.similarity_pane.text_widget.insert(END, similarities)
        self.difference_pane.text_widget.insert(END, differences)


def read_file(file_path):
    try:
        if file_path.endswith('.docx'):
            return extract_text_from_docx(file_path)
        elif file_path.endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='ISO-8859-1', errors='ignore') as f:
                return f.read()
    except Exception as e:
        return f"⚠️ Error reading file: {e}"


def extract_text_from_docx(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            if 'word/document.xml' not in zip_ref.namelist():
                return "⚠️ Invalid DOCX format"
            return extract_text_from_xml(zip_ref.read('word/document.xml'))
    except Exception as e:
        return f"⚠️ DOCX Error: {e}"


def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        return ' '.join(page.get_text("text") for page in doc)
    except Exception as e:
        return f"⚠️ PDF Error: {e}"


def extract_text_from_xml(xml_content):
    try:
        tree = etree.XML(xml_content)
        texts = tree.xpath('//w:t/text()', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        return ' '.join(texts) or "⚠️ Empty document content"
    except Exception as e:
        return f"⚠️ XML Error: {e}"


if __name__ == "__main__":
    root = tk.Tk()
    app = ComparisonApp(root)
    root.mainloop()