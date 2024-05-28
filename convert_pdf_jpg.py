import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import fitz  # PyMuPDF
import os

def convert_pdf_to_jpg(input_file, output_folder):
    try:
        # Verifica se o diretório de saída é gravável
        if not os.access(output_folder, os.W_OK):
            raise PermissionError(f"Sem permissão para gravar na pasta: {output_folder}")

        pdf_document = fitz.open(input_file)
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            output_file = os.path.join(output_folder, f"page_{page_number + 1}.jpg")
            pix.save(output_file)
        messagebox.showinfo("Conversão Concluída 🎉", f"PDF convertido para JPG e salvo em {output_folder}")
    except Exception as e:
        messagebox.showerror("Erro ❌", f"Ocorreu um erro durante a conversão: {str(e)}")

def convert_jpg_to_pdf(input_files, output_file):
    try:
        # Verifica se o diretório de saída é gravável
        output_dir = os.path.dirname(output_file)
        if not os.access(output_dir, os.W_OK):
            raise PermissionError(f"Sem permissão para gravar na pasta: {output_dir}")

        images = [Image.open(img) for img in input_files]
        images[0].save(output_file, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
        messagebox.showinfo("Conversão Concluída 🎉", f"JPGs convertidos para PDF e salvo como {output_file}")
    except Exception as e:
        messagebox.showerror("Erro ❌", f"Ocorreu um erro durante a conversão: {str(e)}")

def select_input_pdf():
    input_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if input_file:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, input_file)

def select_output_folder():
    output_folder = filedialog.askdirectory()
    if output_folder:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, output_folder)

def select_input_jpg():
    input_files = filedialog.askopenfilenames(filetypes=[("JPEG files", "*.jpg")])
    if input_files:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, ", ".join(input_files))

def select_output_pdf():
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_file:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, output_file)

def start_conversion():
    input_file = entry_input.get()
    output_file = entry_output.get()
    if conversion_type.get() == 1:  # PDF to JPG
        if input_file and output_file:
            convert_pdf_to_jpg(input_file, output_file)
    elif conversion_type.get() == 2:  # JPG to PDF
        if input_file and output_file:
            input_files = input_file.split(", ")
            convert_jpg_to_pdf(input_files, output_file)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Conversor PDF <-> JPG 🎨")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

conversion_type = tk.IntVar()

radio_pdf_to_jpg = tk.Radiobutton(frame, text="Converter PDF para JPG", variable=conversion_type, value=1, font=("Helvetica", 12))
radio_pdf_to_jpg.grid(row=0, column=0, columnspan=3, pady=5)

radio_jpg_to_pdf = tk.Radiobutton(frame, text="Converter JPG para PDF", variable=conversion_type, value=2, font=("Helvetica", 12))
radio_jpg_to_pdf.grid(row=1, column=0, columnspan=3, pady=5)

label_input = tk.Label(frame, text="Arquivo de Entrada:", font=("Helvetica", 12), fg="blue")
label_input.grid(row=2, column=0, pady=5)

entry_input = tk.Entry(frame, width=40, font=("Helvetica", 12))
entry_input.grid(row=2, column=1, pady=5)

button_input_pdf = tk.Button(frame, text="Selecionar PDF...", command=select_input_pdf, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
button_input_pdf.grid(row=2, column=2, pady=5)

button_input_jpg = tk.Button(frame, text="Selecionar JPGs...", command=select_input_jpg, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
button_input_jpg.grid(row=2, column=3, pady=5)

label_output = tk.Label(frame, text="Pasta de Saída / Arquivo de Saída:", font=("Helvetica", 12), fg="blue")
label_output.grid(row=3, column=0, pady=5)

entry_output = tk.Entry(frame, width=40, font=("Helvetica", 12))
entry_output.grid(row=3, column=1, pady=5)

button_output_folder = tk.Button(frame, text="Selecionar Pasta...", command=select_output_folder, bg="lightgreen", fg="black", font=("Helvetica", 12, "bold"))
button_output_folder.grid(row=3, column=2, pady=5)

button_output_pdf = tk.Button(frame, text="Salvar como PDF...", command=select_output_pdf, bg="lightgreen", fg="black", font=("Helvetica", 12, "bold"))
button_output_pdf.grid(row=3, column=3, pady=5)

button_convert = tk.Button(root, text="Converter 🎶", command=start_conversion, bg="orange", fg="black", font=("Helvetica", 12, "bold"))
button_convert.pack(pady=10)

root.mainloop()
