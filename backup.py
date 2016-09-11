import os
import time
import zipfile
import configparser


# копируемые файлы и каталоги собираются в список
# имена с пробелами нужно заключать в двочные кавычки или raw-string
source = ['/home/victor/WORKSPACE/PYTHON/AByteOfPython/test_dir']

# резервные копии должны храниться в специально отведённом каталоге
target_dir = '/media/victor/Data/Backup/local'

# файлы и папки помещаются в zip-архив
# текущая дата служит именем подкаталога
today = target_dir + os.sep + time.strftime('%Y%m%d')
# текущее время - имя zip-архива
now = time.strftime('%H%M%S')

# имя zip-архива должно содержать время
# пользователь может добавить к имени архива комментарий
comment = input('Введите комментарий (""): ')
if len(comment) == 0:
    target = today + os.sep + now + '.zip'
else:
    target = today + os.sep + now + \
        '_' + comment.replace(' ', '_') + '.zip'

# каталог должен существовать
if not os.path.exists(today):
    os.mkdir(today)
    print('Каталог успешно создан:', today)

# для архивирования используется модуль zipfile
# Создание нового архива
with zipfile.ZipFile(target, 'w') as archive:
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
print('Резервная копия успешно создана в', target)

# if os.system(zip_command) == 0:
#     print('Резервная копия успешно создана в', target)
# else:
#     print('Не удалось создать резервную копию')
