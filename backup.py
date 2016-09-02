import os
import time

# файлы и каталоги, которые необходимо скопировать, собираются в список
source = ['/home/victor/.bash_history',
          '/home/victor/.profile',
          '/home/victor/.python_history',
          '/home/victor/.ssh',
          '/home/victor/.yandex',
          '/home/victor/Scripts',
          '/home/victor/WORKSPACE'
]

source = ['/home/victor/WORKSPACE/PYTHON/Other']

# резервные копии должны храниться в специально отведённом каталоге
target_dir = '/media/victor/Data/Backup/local'

# файлы и папки помещаются в zip-архив
# текущая дата служит именем подкаталога
today = target_dir + os.sep + time.strftime('%Y%m%d')
# текущее время - имя zip-архива
now = time.strftime('%H%M%S')

# каталог должен существовать
if not os.path.exists(today):
    os.mkdir(today)
    print('Каталог успешно создан:', today)

# имя zip-архива
target = today + os.sep + now + '.zip'

# для архивирования используется команда zip
zip_command = 'zip -qr {0} {1}'.format(target, ' '.join(source))

if os.system(zip_command) == 0:
    print('Резервная копия успешно создана в', target)
else:
    print('Не удалось создать резервную копию')

