import os
import time
import zipfile
import json
import configparser

CONFIG_PATH = r'backup.ini'


def load_config(path):
    """Загрузка конфигурации из указанного пути.

    Функция возвращает объект SafeConfigParser
    """
    config = configparser.SafeConfigParser()
    config.read(path)
    return config


def main():
    """Точка входа."""

    # получаем конфигурацию
    CONFIG = load_config(CONFIG_PATH)
    # в конфигурации указан путь для хранения резервной копии
    target = json.loads(CONFIG.get('BACKUP', 'target'))


    # копируемые файлы и каталоги собираются в список
    # имена с пробелами нужно заключать в двочные кавычки или raw-string
    source = json.loads(CONFIG.get('BACKUP', 'source'))

    # файлы и папки помещаются в zip-архив
    # текущая дата служит именем подкаталога
    today = os.path.join(target, time.strftime('%Y%m%d'))
    # текущее время - имя zip-архива
    now = time.strftime('%H%M%S')

    # имя zip-архива должно содержать время
    # пользователь может добавить к имени архива комментарий
    comment = input('Введите комментарий (""): ')
    if len(comment) == 0:
        target_path = os.path.join(today, now + '.zip')
    else:
        target_path = os.path.join(today,
            now + '_' + comment.replace(' ', '_') + '.zip')

    # каталог должен существовать
    if not os.path.exists(today):
        os.mkdir(today)
        print('Каталог успешно создан:', today)

    # для архивирования используется модуль zipfile
    # Создание нового архива
    with zipfile.ZipFile(target_path, 'w') as archive:
        # нужно пройтись по всем указанным директориям и файлам
        for item in source:
            if os.path.isdir(item):
                for root, dirs, files in os.walk(item, followlinks=True): # Список всех файлов и папок в директории folder
                    for file in files:
                        path = os.path.join(root, file)
                        if not os.path.exists(path):
                            print('Пропускаю несуществующий файл:', path)
                            continue
                        realpath = os.path.realpath(path)
                        print(realpath)
                        archive.write(realpath, arcname=path)  # Создание относительных путей и запись файлов в архив
                        # archive.write(os.path.join(root, file))
            else:
                archive.write(item)
    print('Резервная копия успешно создана в', target_path)

    # if os.system(zip_command) == 0:
    #     print('Резервная копия успешно создана в', target_path)
    # else:
    #     print('Не удалось создать резервную копию')


if __name__ == '__main__':
    main()
