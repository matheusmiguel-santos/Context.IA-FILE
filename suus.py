import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import webbrowser

def detect_framework(directory):
    if os.path.isfile(os.path.join(directory, 'node_modules', 'react-scripts', 'bin', 'react-scripts.js')):
        return 'react'
    elif os.path.isfile(os.path.join(directory, 'node_modules', 'vue', 'dist', 'vue.runtime.common.prod.js')):
        return 'vue'
    elif os.path.isfile(os.path.join(directory, 'node_modules', '@angular', 'core', 'bundles', 'core.umd.js')):
        return 'angular'
    else:
        return 'unknown'

def is_essential_dir(path, framework):
    if framework in ['react', 'nextjs']:
        return path.endswith(('src', 'public')) or 'src' in path or 'public' in path
    elif framework == 'vue':
        return path.endswith(('src', 'public', 'components')) or 'src' in path or 'public' in path or 'components' in path
    elif framework == 'angular':
        return path.endswith(('src', 'app')) or 'src' in path or 'app' in path
    elif framework == 'laravel':
        return path.endswith(('app', 'resources')) or 'app' in path or 'resources' in path
    elif framework == 'nodejs':
        return path.endswith(('bin', 'lib', 'public', 'routes', 'views')) or 'bin' in path or 'lib' in path or 'public' in path or 'routes' in path or 'views' in path
    else:
        return False

def is_text_file(filename):
    return filename.endswith(('.html', '.js', '.css', '.json', '.txt', '.md'))

def map_dir(directory, framework, prefix=''):
    dir_map = ''
    if prefix:
        dir_map += prefix[:-1] + '+--' + os.path.basename(directory) + '\n'
    else:
        dir_map += os.path.basename(directory) + '\n'
    prefix += '|  '

    for item in sorted(os.listdir(directory)):
        path = os.path.join(directory, item)
        if os.path.isfile(path) and is_essential_dir(path, framework):
            dir_map += prefix + '+--' + item + '\n'
        elif os.path.isdir(path) and is_essential_dir(path, framework):
            dir_map += map_dir(path, framework, prefix)

    return dir_map

def write_files(directory, framework, output_file):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if is_essential_dir(os.path.join(root, file), framework) and is_text_file(file):
                file_count += 1
                output_file.write('--FILENAME: ' + file + '\n')
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    output_file.write(f.read() + '\n\n')
    return f"Total de arquivos processados: {file_count}"

def main():
    directory = directory_entry.get()

    if not os.path.exists(directory):
        result_label['text'] = f"Erro: o diretório {directory} não existe."
        return

    framework = detect_framework(directory)
    output_filename = os.path.basename(directory) + '.' + file_type.get()
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(map_dir(directory, framework))
        result_label['text'] = write_files(directory, framework, output_file)
    
    result_label['text'] += f"\nArquivo {output_filename} gerado com sucesso!"
    open_file_button['state'] = 'normal'
    open_dir_button['state'] = 'normal'

def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

def open_file():
    webbrowser.open(os.path.join(os.getcwd(), os.path.basename(directory_entry.get()) + '.' + file_type.get()))

def open_directory():
    webbrowser.open(os.getcwd())

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = int(screen_width * 0.35)
window_height = int(screen_height * 0.35)
window.geometry(f"{window_width}x{window_height}")

frame = tk.Frame(window)
frame.place(relwidth=1, relheight=1)
frame.config(bg='light gray')

logo = Image.open("img/logo.png")
logo.thumbnail((200, 200))
logo = ImageTk.PhotoImage(logo)

logo_label = tk.Label(frame, image=logo, bg='light gray')
logo_label.place(relx=0.5, rely=0.1, anchor='n')

prompt_label = tk.Label(frame, text="Por favor, forneça o diretório do projeto:", bg='light gray')
prompt_label.place(relx=0.5, rely=0.3, anchor='n')

dir_frame = tk.Frame(frame, bg='light gray')
dir_frame.place(relx=0.5, rely=0.4, anchor='n')

directory_entry = tk.Entry(dir_frame)
directory_entry.pack(side='left', fill='x', expand=True)

browse_img = Image.open("img/search.png")
browse_img.thumbnail((30, 30))
browse_img = ImageTk.PhotoImage(browse_img)

browse_button = tk.Button(dir_frame, image=browse_img, command=browse_directory)
browse_button.pack(side='left', padx=5)

file_type = tk.StringVar()
file_type.set('txt')

doc_img = Image.open("img/docx.png")
doc_img.thumbnail((45, 45))
doc_img = ImageTk.PhotoImage(doc_img)

pdf_img = Image.open("img/pdf.png")
pdf_img.thumbnail((45, 45))
pdf_img = ImageTk.PhotoImage(pdf_img)

txt_img = Image.open("img/txt.png")
txt_img.thumbnail((45, 45))
txt_img = ImageTk.PhotoImage(txt_img)

doc_button = tk.Radiobutton(frame, image=doc_img, variable=file_type, value='docx', bg='light gray')
doc_button.place(relx=0.4, rely=0.55, anchor='n')

pdf_button = tk.Radiobutton(frame, image=pdf_img, variable=file_type, value='pdf', bg='light gray')
pdf_button.place(relx=0.5, rely=0.55, anchor='n')

txt_button = tk.Radiobutton(frame, image=txt_img, variable=file_type, value='txt', bg='light gray')
txt_button.place(relx=0.6, rely=0.55, anchor='n')

run_button = tk.Button(frame, text='Gerar Arquivo', command=main)
run_button.place(relx=0.5, rely=0.75, anchor='n')

open_file_button = tk.Button(frame, text='Abrir Arquivo', state='disabled', command=open_file)
open_file_button.place(relx=0.4, rely=0.85, anchor='n')

open_dir_button = tk.Button(frame, text='Abrir Diretório', state='disabled', command=open_directory)
open_dir_button.place(relx=0.6, rely=0.85, anchor='n')

result_label = tk.Label(frame, text='', bg='light gray')
result_label.place(relx=0.5, rely=0.95, anchor='n')

window.mainloop()
