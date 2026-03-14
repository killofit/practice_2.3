from tkinter import *
import requests


def get_profile():
    username = entry.get().strip()
    if not username:
        result_text.insert(END, "Введите имя пользователя в поле сверху\n")
        return

    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            user = response.json()
            result_text.insert(END, f"Профиль: {username}\n")
            result_text.insert(END, f"Имя: {user.get('name', 'Не указано')}\n")
            result_text.insert(END, f"Ссылка на профиль: {user['html_url']}\n")
            result_text.insert(END, f"Количество репозиториев: {user['public_repos']}\n")
            result_text.insert(END, f"Количество подписчиков: {user['followers']}\n")
            result_text.insert(END, f"Количество подписок: {user['following']}\n")
        else:
            result_text.insert(END, f"{username} не найден\n")
    except:
        result_text.insert(END, "Ошибка соединения\n")


def get_repos():
    username = entry.get().strip()
    if not username:
        result_text.insert(END, "Введите имя пользователя в поле сверху\n")
        return

    try:
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)

        if response.status_code == 200:
            repos = response.json()
            result_text.insert(END, f"Найдено репозиториев: {len(repos)}\n")

            for repo in repos:
                result_text.insert(END, f"Название: {repo['name']}\n")
                result_text.insert(END, f"Ссылка: {repo['html_url']}\n")
                result_text.insert(END, f"Язык: {repo.get('language', 'Не указан')}\n")
                result_text.insert(END, f"Видимость: {'Приватный' if repo['private'] else 'Публичный'}\n")
                result_text.insert(END, f"Ветка по умолчанию: {repo['default_branch']}\n")
        else:
            result_text.insert(END, f"{username} не найден\n")
    except:
        result_text.insert(END, "Ошибка соединения\n")


def search_repos():
    query = entry.get().strip()
    if not query:
        result_text.insert(END, "Введите название для поиска в поле сверху\n")
        return

    try:
        url = f"https://api.github.com/search/repositories?q={query}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            repos = data.get('items', [])

            result_text.insert(END, f"Найдено репозиториев: {len(repos)}\n")

            for repo in repos[:5]:
                result_text.insert(END, f"Название: {repo['name']}\n")
                result_text.insert(END, f"Владелец: {repo['owner']['login']}\n")
                result_text.insert(END, f"Ссылка: {repo['html_url']}\n")
                result_text.insert(END, f"Язык: {repo.get('language', 'Не указан')}\n")
        else:
            result_text.insert(END, "Ошибка поиска\n")
    except:
        result_text.insert(END, "Ошибка соединения\n")


def clear_results():
    result_text.delete(1.0, END)


root = Tk()
root.title("GITHUB")
root.geometry("800x600")

label = Label(text="GITHUB", font=("Arial", 20), background="#00FF7F")
label.pack(anchor="n", pady=10)

entry = Entry(root, font=("Arial", 12), width=40)
entry.pack(pady=5)


result_text = Text(root, height=25, font=("Courier", 9))
result_text.pack(expand=True, fill=BOTH, padx=10, pady=5)

btn_frame = Frame(root)
btn_frame.pack(pady=5)

Button(btn_frame, text="Профиль", font=("Arial", 10),
       command=get_profile, background="#00FF7F", width=12).pack(side=LEFT, padx=2)
Button(btn_frame, text="Репозитории", font=("Arial", 10),
       command=get_repos, background="#00FF7F", width=12).pack(side=LEFT, padx=2)
Button(btn_frame, text="Поиск", font=("Arial", 10),
       command=search_repos, background="#00FF7F", width=12).pack(side=LEFT, padx=2)
Button(btn_frame, text="Очистить", font=("Arial", 10),
       command=clear_results, background="#00FF7F", width=12).pack(side=LEFT, padx=2)

root.mainloop()