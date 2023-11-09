#!/usr/bin/env python
import os
import tkinter as tk
from tkinter import filedialog
import PyPDF2

class PdfMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("800x600")
        
        self.selected_files = []
        self.output_directory = ""
        
        self.create_gui()

    def create_gui(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        self.status_label = tk.Label(self.frame, text="")
        self.status_label.pack()

        self.label = tk.Label(self.frame, text="Select PDF files to merge:")
        self.label.pack()

        self.file_listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=100)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.frame, text="Add PDFs", command=self.browse_pdf_files)
        self.add_button.pack()

        self.remove_button = tk.Button(self.frame, text="Remove Selected", command=self.remove_selected_file)
        self.remove_button.pack()

        self.up_button = tk.Button(self.frame, text="Move Up", command=self.move_up)
        self.up_button.pack()

        self.down_button = tk.Button(self.frame, text="Move Down", command=self.move_down)
        self.down_button.pack()

        self.output_label = tk.Label(self.frame, text="Enter output filename (without extension):")
        self.output_label.pack()

        self.output_entry = tk.Entry(self.frame)
        self.output_entry.pack()

        self.output_directory_button = tk.Button(self.frame, text="Set Output Directory", command=self.set_output_directory)
        self.output_directory_button.pack()

        self.output_directory_label = tk.Label(self.frame, text="Output directory not set.")
        self.output_directory_label.pack()

        self.merge_button = tk.Button(self.frame, text="Merge PDFs", command=self.merge_selected_pdfs)
        self.merge_button.pack()

    def merge_pdfs(self, pdf_files, output_filename):
        pdf_merge = PyPDF2.PdfMerger()
        for pdf_file in pdf_files:
            with open(pdf_file, 'rb') as file:
                pdf_merge.append(file)

        output_path = os.path.join(self.output_directory, output_filename)
        with open(output_path, 'wb') as output_file:
            pdf_merge.write(output_file)

    def add_to_listbox(self, file_paths):
        for file_path in file_paths:
            self.selected_files.append(file_path)
            self.file_listbox.insert(tk.END, os.path.basename(file_path))

    def browse_pdf_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if file_paths:
            self.add_to_listbox(file_paths)
            self.status_label.config(text="PDFs added to the list.")
        else:
            self.status_label.config(text="No PDF files selected.")

    def remove_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            del self.selected_files[index]
            self.file_listbox.delete(index)
            self.status_label.config(text="File removed from the list.")

    def move_up(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            if index > 0:
                selected_file = self.selected_files.pop(index)
                self.selected_files.insert(index - 1, selected_file)
                self.file_listbox.delete(index)
                self.file_listbox.insert(index - 1, os.path.basename(selected_file))
                self.file_listbox.select_set(index - 1)

    def move_down(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            if index < len(self.selected_files) - 1:
                selected_file = self.selected_files.pop(index)
                self.selected_files.insert(index + 1, selected_file)
                self.file_listbox.delete(index)
                self.file_listbox.insert(index + 1, os.path.basename(selected_file))
                self.file_listbox.select_set(index + 1)

    def set_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            self.output_directory_label.config(text=self.output_directory)
        else:
            self.output_directory_label.config(text="Output directory not set.")

    def merge_selected_pdfs(self):
        if self.selected_files:
            output_filename = self.output_entry.get()
            if not output_filename:
                self.status_label.config(text="Please enter an output filename.")
                return

            output_filename = output_filename.strip() + ".pdf"
            if not self.output_directory:
                self.status_label.config(text="Output directory not set.")
                return

            self.merge_pdfs(self.selected_files, output_filename)
            self.status_label.config(text=f"PDFs merged to {self.output_directory}/{output_filename} successfully!")
        else:
            self.status_label.config(text="No PDF files added to merge.")


def main():
    root = tk.Tk()
    app = PdfMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()