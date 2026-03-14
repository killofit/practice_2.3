from tkinter import *
import psutil
import time


def monitoring():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    result_text.insert(END, f"Загрузка CPU: {cpu}% \n")
    result_text.insert(END, f"Использовано RAM: {memory.percent}% \n")
    result_text.insert(END, f"Загруженность диска: {disk.percent}% \n")

root = Tk()
root.title("Системный монитор")
root.geometry("700x400")

btn = Button(text="ПРОВЕРИТЬ", font=("Arial", 14), command=monitoring, background="#6A5ACD")
btn.pack(anchor="se", ipadx=13, ipady=13)

label = Label(text="Системный монитор", font=("Arial", 28), background="#6A5ACD")
label.pack(anchor="nw")

result_text = Text(root, height=20, font=("Courier", 13))
result_text.pack(expand=True, padx=10, pady=5)

root.mainloop()