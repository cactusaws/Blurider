import os
import pandas as pd
from colorama import Fore, Style, Back, init  # Импортируем необходимые модули из colorama

init()  # Инициализация colorama для работы с цветом в Windows


def search_in_txt(file_path, query):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            if query.lower() in line.lower():  # Поиск без учета регистра
                yield file_path, line_number, line.strip()


def search_in_csv(file_path, query):
    df = pd.read_csv(file_path, encoding='utf-8', error_bad_lines=False)
    for line_number, row in df.iterrows():
        for col in df.columns:
            if query.lower() in str(row[col]).lower():  # Поиск без учета регистра
                yield file_path, line_number + 1, str(row[col])


def search_in_xlsx(file_path, query):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except FileNotFoundError:
        print(f"{Fore.RED}Ошибка: Файл {file_path} не найден.{Style.RESET_ALL}")
        return
    except Exception as e:
        print(f"{Fore.RED}Ошибка при чтении файла {file_path}: {e}{Style.RESET_ALL}")
        return
    for line_number, row in df.iterrows():
        for col in df.columns:
            if query.lower() in str(row[col]).lower():  # Поиск без учета регистра
                yield file_path, line_number + 1, str(row[col])


def main():
    folder_path = 'bd'
    if not os.path.exists(folder_path):
        print(Fore.RED + "Папка 'bd' не найдена. Пожалуйста, создайте её и добавьте файлы." + Style.RESET_ALL)
        return

    files = os.listdir(folder_path)
    if not files:
        print(Fore.RED + "В папке 'bd' нет файлов. Пожалуйста, добавьте файлы." + Style.RESET_ALL)
        return

    total_files = len(files)
    total_size = sum(
        os.path.getsize(os.path.join(folder_path, f)) for f in files if os.path.isfile(os.path.join(folder_path, f)))

    print(f"""
{Fore.YELLOW} ______   __                    _        __                
{Fore.RED}|_   _ \ [  |                  (_)      |  ]               
{Fore.YELLOW}  | |_) | | | __   _   _ .--.  __   .--.| | .---.  _ .--.  
{Fore.RED}  |  __'. | |[  | | | [ `/'`\][  |/ /'`\' |/ /__\\[ `/'`\] 
{Fore.YELLOW} _| |__) || | | \_/ |, | |     | || \__/  || \__., | |     
{Fore.RED}|_______/[___]'.__.'_/[___]   [___]'.__.;__]'.__.'[___]    

    """ + Style.RESET_ALL)
    print(f"{Fore.BLUE}Blurider{Fore.GREEN} - Поиск по вашим любым базам данным" + Style.RESET_ALL)
    print(f"{Fore.GREEN} Поиск только по: xlsx, txt, csv" + Style.RESET_ALL)
    print(f"{Fore.RED}• {Fore.MAGENTA}Вес баз данных: {Fore.BLUE}{total_size / (1024 * 1024):.2f} мегабайт" + Style.RESET_ALL)
    print(f"{Fore.RED}• {Fore.MAGENTA}Всего загружено баз данных: {Fore.BLUE}{total_files} {Fore.MAGENTA}файлов" + Style.RESET_ALL)
    print(f"{Fore.RED}• {Fore.MAGENTA}Софт был сделан t.me/gotooffi\n" + Style.RESET_ALL)
    query = input(Fore.BLUE + "Введите любой запрос: " + Style.RESET_ALL)

    found = False
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.txt'):
            for result in search_in_txt(file_path, query):
                found = True
                print(
                    f"{Fore.YELLOW}[Файл: {Fore.BLUE}{result[0]}{Fore.YELLOW}] <> [Строка: {Fore.BLUE}{result[1]}{Fore.YELLOW}] <> [Содержимое строки: {Fore.BLUE}{result[2]}]" + Style.RESET_ALL)
        elif file_name.endswith('.csv'):
            for result in search_in_csv(file_path, query):
                found = True
                print(
                    f"{Fore.YELLOW}[Файл: {Fore.BLUE}{result[0]}{Fore.YELLOW}] <> [Строка: {Fore.BLUE}{result[1]}{Fore.YELLOW}] <> [Содержимое строки: {Fore.BLUE}{result[2]}]" + Style.RESET_ALL)
        elif file_name.endswith('.xlsx'):
            for result in search_in_xlsx(file_path, query):
                found = True
                print(
                    f"{Fore.YELLOW}[Файл: {Fore.BLUE}{result[0]}{Fore.YELLOW}] <> [Строка: {Fore.BLUE}{result[1]}{Fore.YELLOW}] <> [Содержимое строки: {Fore.BLUE}{result[2]}]" + Style.RESET_ALL)

    if not found:
        print(Fore.RED + "Запрос не найден в файлах." + Style.RESET_ALL)


if __name__ == "__main__":
    main()