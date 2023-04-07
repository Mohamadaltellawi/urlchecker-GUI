import requests
import argparse
import tkinter as tk
from tkinter import filedialog
from tabulate import tabulate

def check_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls]

    results = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                status = 'Alive'
            else:
                status = 'Dead'
        except requests.exceptions.RequestException:
            status = 'Dead'

        results.append([url, status])

    return results

def run_gui():
    def browse_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            file_path_var.set(file_path)

    def check_urls_gui():
        file_path = file_path_var.get()
        if file_path:
            results = check_urls(file_path)
            table = tabulate(results, headers=['URL', 'Status'])
            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, table)

    root = tk.Tk()
    root.title('URL Checker')

    file_path_var = tk.StringVar()
    file_path_entry = tk.Entry(root, textvariable=file_path_var, width=40)
    file_path_entry.grid(row=0, column=0, padx=10, pady=10)

    browse_button = tk.Button(root, text='Browse', command=browse_file)
    browse_button.grid(row=0, column=1, padx=10, pady=10)

    check_button = tk.Button(root, text='Check URLs', command=check_urls_gui)
    check_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    output_text = tk.Text(root, height=10, width=50)
    output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='Check the status of URLs in a file')
    parser.add_argument('file', type=str, help='Path to the file containing URLs')
    args = parser.parse_args()

    results = check_urls(args.file)
    print(tabulate(results, headers=['URL', 'Status']))

if __name__ == '__main__':
    run_gui()


