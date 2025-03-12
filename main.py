import os
import gzip

# Нет привязки к папке, главное, чтобы запускаемый файл (*.py) был там же где и логи
logs_folder = os.path.dirname(os.path.realpath(__file__))  # Папка с исходными файлами

# имя директории для результата
FOLDER_RESULT_NAME = 'result'

# окончания в имени логов
END_NAMES: str = 'log.gz'
REQUIRED_SUBSTRINGS = ['IpAppCallControlManager.callEventNotify',
                       'IpCall.routeReq']

# Список допустимых префиксов для 8-й позиции
ALLOWED_PREFIXES = ['1234400511', '1234710011', '1234600411', '1234600611']


def create_folder_result(path: str, name_folder: str) -> str:
    path_result = os.path.join(path, name_folder)
    if not os.path.isdir(path_result):
        os.mkdir(path_result)
    return path_result


def create_file_for_result(path: str, name: str) -> str:
    """Вернет str с путем и именем файла для записи результатов обработки"""

    file_for_result = os.path.join(path, name)

    if os.path.isdir(path):
        with open(file_for_result, 'w'):
            pass
    return file_for_result


def collect_all_log_name(path: str, postfix_needed_files: str) -> list[str]:
    needed_files = list()
    if not os.path.isdir(path):
        return needed_files

    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)) \
                and filename.endswith(postfix_needed_files):
            needed_files.append(filename)
    return sorted(needed_files)


def write_result(path_with_name: str, text: str) -> None:
    with open(path_with_name, 'a', encoding='utf-8') as file:
        try:
            file.write(text)
        except IOError as e:
            print(f'Ошибка записи в файл: {e}')


def read_and_filter_log_file(path: str, namefile: str, path_for_result: str) -> None:
    with gzip.open(os.path.join(path, namefile), mode='r') as file:
        result: list[str] = []
        temp_pair: dict[str, str] = {}

        for line in file:
            line_for_filter = line.decode('utf-8').split(' ')
            if len(line_for_filter) < 7 or len(line_for_filter[5]) < 10:
                continue

            if line_for_filter[5] == REQUIRED_SUBSTRINGS[0] and line_for_filter[7][:10] in ALLOWED_PREFIXES:
                temp_pair[line_for_filter[2]] = (f'{line_for_filter[3]}\t{line_for_filter[4]}\t'
                                                 f'{line_for_filter[6]}\t{line_for_filter[7]}')  # 3 4 6 7
            elif line_for_filter[5] == REQUIRED_SUBSTRINGS[1] and line_for_filter[2] in temp_pair:
                temp = temp_pair.pop(line_for_filter[2])
                result.append(f'{temp}\t{line_for_filter[6]}\t{line_for_filter[7]}')

        if result:
            text_for_write = str.join('', result)
            write_result(path_for_result, text_for_write)


def main():
    # создаем директорию для результата
    folder_result = create_folder_result(logs_folder, FOLDER_RESULT_NAME)

    # собираем список файлов для проверки
    files_for_read = collect_all_log_name(logs_folder, END_NAMES)

    if files_for_read:
        files_for_write: set = set()
        size_array = len(files_for_read)
        for file, i in zip(files_for_read, range(size_array)):
            # Создаем файл для записи результата. Если уже есть, удаляем старый
            name_split = file.split('-')[1:4]
            file_name = f'{str.join('-', name_split)}.txt'
            print(f'{i + 1}/{size_array}\tЧитаю: "{file}"\t\tЗапишу данные в: "{file_name}"')
            if file_name not in files_for_write:
                path_for_result = create_file_for_result(folder_result, file_name)
                files_for_write.add(file_name)
            else:
                path_for_result = os.path.join(folder_result, file_name)

            read_and_filter_log_file(logs_folder, file, path_for_result)


if __name__ == '__main__':
    main()
