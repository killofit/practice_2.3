from tkinter import *
import requests


def check_sites():
    urls = [
        "https://github.com/",
        "https://www.binance.com/en",
        "https://tomtit.tomsk.ru/",
        "https://jsonplaceholder.typicode.com/",
        "https://moodle.tomtit-tomsk.ru/"
    ]

    for url in urls:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                status = "доступен"
            elif response.status_code == 403:
                status = "вход запрещен"
            elif response.status_code == 404:
                status = "не найден"
            else:
                status = f"код {response.status_code}"

            result_text.insert(END, f"URL: {url} – {status} – {response.status_code}\n")

        except:
            result_text.insert(END, f"URL: {url} – не доступен – ошибка\n")

root = Tk()
root.title("Проверка сайтов")
root.geometry("700x400")

btn = Button(text="ПРОВЕРИТЬ", font=("Arial", 14), command=check_sites, background="#EE82EE")
btn.pack(anchor="se", ipadx=13, ipady=13)

label = Label(text="Проверка сайтов", font=("Arial", 28), background="#EE82EE")
label.pack(anchor="nw")

result_text = Text(root, height=20, font=("Courier", 13))
result_text.pack(expand=True, padx=10, pady=5)

root.mainloop()
