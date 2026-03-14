from tkinter import *
import requests
import json

currencies = {}
groups = {}

try:
    with open("resource/save.json2", 'r') as f:
        groups = json.load(f)
    print("Группы загружены из файла")
except:
    groups = {}


def load_data():
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        if response.status_code == 200:
            global currencies
            currencies = response.json()['Valute']
            result_text.insert(END, "Данные загружены\n")
        else:
            result_text.insert(END, "Ошибка загрузки\n")
    except:
        result_text.insert(END, "Ошибка соединения\n")

def show_all():
    if not currencies:
        result_text.insert(END, "Сначала загрузите данные\n")
    else:
        for code, info in currencies.items():
            result_text.insert(END, f"{code:<5} {info['Name']:<25} {info['Value']:.2f}\n")

def find_currency():
    if not currencies:
        result_text.insert(END, "Сначала загрузите данные\n")
    else:
        code = entry.get().upper()
        if code in currencies:
            info = currencies[code]
            result_text.insert(END, f"{code} - {info['Name']}\n")
            result_text.insert(END, f"Курс: {info['Value']} руб.\n")
            result_text.insert(END, f"Предыдущий курс: {info['Previous']} руб.\n")
        else:
            result_text.insert(END, "Введите код валюты в поле сверху\n")
            result_text.insert(END, "Валюта не найдена\n")

def create_group():
    if not currencies:
        result_text.insert(END, "Сначала загрузите данные\n")
    else:
        result_text.insert(END, "Введите название группы в поле сверху\n")
        name = entry.get()
        if name and name not in groups:
            groups[name] = []
            result_text.insert(END, f"Группа '{name}' создана\n")
            with open("resource/save.json2", 'w') as f:
                json.dump(groups, f)
            result_text.insert(END, "Сохранено в файл\n")
        else:
            result_text.insert(END, "Такая группа уже есть \n")

def show_groups():
    if not groups:
        result_text.insert(END, "Нет групп\n")
    else:
        for name, currencies_list in groups.items():
            if currencies_list:
                result_text.insert(END, f"{name}: {', '.join(currencies_list)}\n")
            else:
                result_text.insert(END, f"{name}: пусто\n")

def add_to_group():
    if not groups:
        result_text.insert(END, "Сначала создайте группу\n")
    else:
        data = entry.get().split()
        if len(data) == 2:
            group, code = data[0], data[1].upper()
            if group in groups:
                if code in currencies:
                    if code not in groups[group]:
                        groups[group].append(code)
                        with open("resource/save.json2", 'w') as f:
                            json.dump(groups, f)
                        result_text.insert(END, f"{code} добавлен в группу {group}\n")
                    else:
                        result_text.insert(END, "Такая валюта уже есть в группе\n")
                else:
                    result_text.insert(END, "Валюта не найдена\n")
            else:
                result_text.insert(END, "Группа не найдена\n")
        else:
            result_text.insert(END, "Введите в поле сверху: группа код_валюты Пример(ЛОЛ USD)\n")

def remove_from_group():
    if not groups:
        result_text.insert(END, "Нет групп\n")
    else:
        data = entry.get().split()
        if len(data) == 2:
            group, code = data[0], data[1].upper()
            if group in groups and groups[group]:
                if code in groups[group]:
                    groups[group].remove(code)
                    with open("resource/save.json2", 'w') as f:
                        json.dump(groups, f)
                    result_text.insert(END, f"{code} удален из группы\n")
                else:
                    result_text.insert(END, "Валюты нет в группе\n")
            else:
                result_text.insert(END, "Группа пуста или не найдена\n")
        else:
            result_text.insert(END, "Введите в поле сверху: группа код_валюты Пример(ЛОЛ USD)\n")

root = Tk()
root.title("Курсы валют")
root.geometry("900x600")

label = Label(text="МОНИТОРИНГ КУРСОВ ВАЛЮТ", font=("Arial", 28), background="#00BFFF")
label.pack(anchor="n", pady=10)

entry = Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=5)

result_text = Text(root, height=20, font=("Courier", 15))
result_text.pack(expand=True, fill=BOTH, padx=10, pady=5)

btn_frame = Frame(root)
btn_frame.pack(pady=10)

Button(btn_frame, text="Загрузить", font=("Arial", 10),
       command=load_data, background="#00BFFF", width=10).pack(side=LEFT, padx=2)
Button(btn_frame, text="Все валюты", font=("Arial", 10),
       command=show_all, background="#00BFFF", width=10).pack(side=LEFT, padx=2)
Button(btn_frame, text="Найти валюту", font=("Arial", 10),
       command=find_currency, background="#00BFFF", width=10).pack(side=LEFT, padx=2)
Button(btn_frame, text="Создать группу", font=("Arial", 10),
       command=create_group, background="#00BFFF", width=13).pack(side=LEFT, padx=2)
Button(btn_frame, text="Показать группы", font=("Arial", 10),
       command=show_groups, background="#00BFFF", width=15).pack(side=LEFT, padx=2)
Button(btn_frame, text="Добавить валюту в группу", font=("Arial", 10),
       command=add_to_group, background="#00BFFF", width=20).pack(side=LEFT, padx=2)
Button(btn_frame, text="Удалить", font=("Arial", 10),
       command=remove_from_group, background="#00BFFF", width=10).pack(side=LEFT, padx=2)

root.mainloop()