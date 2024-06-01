import os
import shutil
import glob
import datetime
import difflib

if __name__ == '__main__':
    snapshots_path = snapshots


def create_snapshot(folder_path):
    files = os.listdir(folder_path)
    with open(f'{snapshots_path}/{os.path.basename(folder_path)}.txt', 'w') as f:
        for file in files:
            file_path = os.path.join(folder_path, file)
            file_creation_time = os.path.getctime(file_path)
            file_creation_time_str = datetime.datetime.fromtimestamp(
                file_creation_time).strftime('%d%m%Y%H%M%S')
            f.write(f'{file} {file_creation_time_str}\n')


def update_snapshot(folder_path):
    files = os.listdir(folder_path)
    with open(f'{snapshots_path}/{os.path.basename(folder_path)}.txt', 'w') as f:
        for file in files:
            file_path = os.path.join(folder_path, file)
            file_creation_time = os.path.getctime(file_path)
            file_creation_time_str = datetime.datetime.fromtimestamp(
                file_creation_time).strftime('%d%m%Y%H%M%S')
            f.write(f'{file} {file_creation_time_str}\n')


def compare_snapshot(folder_path):
    current_files = []
    snapshot_path = f'{snapshots_path}/{os.path.basename(folder_path)}.txt'
    if os.path.exists(snapshot_path):
        with open(snapshot_path, 'r') as f:
            snapshot_files = f.readlines()
        snapshot_files = [file.split() for file in snapshot_files]
        for entry in os.scandir(folder_path):
            current_files.append((entry.name, os.path.getctime(entry.path)))
        new_files = []
        deleted_files = []
        modified_files = []
        for snapshot_file in snapshot_files:
            file_name = snapshot_file[0]
            try:
                file_time = datetime.datetime.strptime(
                    snapshot_file[1], '%d%m%Y%H%M%S').timestamp()
            except:
                print(snapshot_file[0])
            if any(file[0] == file_name and abs(file[1] - file_time) > 10 for file in current_files):
                modified_files.append(file_name)
            elif not any(file[0] == file_name for file in current_files):
                deleted_files.append(file_name)
        for file in current_files:
            if not any(snapshot_file[0] == file[0] for snapshot_file in snapshot_files):
                new_files.append(file[0])
        return new_files, deleted_files, modified_files
    else:
        create_snapshot(folder_path)
        return [], [], []


def sort_files(folder_path, sort_by):
    files = os.listdir(folder_path)
    if sort_by == 'дата':
        files.sort(key=lambda x: os.path.getmtime(
            os.path.join(folder_path, x)))
        for file in files:
            file_date = datetime.datetime.fromtimestamp(os.path.getmtime(
                os.path.join(folder_path, file))).strftime('%Y-%m-%d %H:%M:%S')
            print(f'{file}: {file_date}')
    elif sort_by == 'размер':
        direction = input(
            'Введите направление сортировки (увеличение, уменьшение): ')
        if direction == 'увеличение':
            files.sort(key=lambda x: os.path.getsize(
                os.path.join(folder_path, x)))
        elif direction == 'уменьшение':
            files.sort(key=lambda x: os.path.getsize(
                os.path.join(folder_path, x)), reverse=True)
        for file in files:
            file_size = os.path.getsize(os.path.join(folder_path, file))
            print(f'{file}: {file_size}')
    elif sort_by == 'тип':
        files.sort(key=lambda x: x.split('.')[-1])
        current_type = None
        for file in files:
            file_type = file.split('.')[-1]
            if file_type != current_type:
                current_type = file_type
                print(f'\n{file_type}:')
            print(f'{file}', end=' ')
            if file != files[-1]:
                print(end=' ')
        print()
    return files


def main():
    folder_path = input(
        'Введите путь к папке, или "0" для выключения программы: ')
    if folder_path == '0':
        return
    new_files, deleted_files, modified_files = compare_snapshot(folder_path)
    if new_files:
        print(f'Новые файлы: {new_files}')
        update_snapshot(folder_path)
    if deleted_files:
        print(f'Удалённые файлы: {deleted_files}')
        update_snapshot(folder_path)
    if modified_files:
        print(f'поменянные файлы: {modified_files}')
        update_snapshot(folder_path)
    while True:
        sort_by = input(
            'Введите тип сортировки (дата, размер, тип), или "0" для выключения программы: ')
        if sort_by == '0':
            break
        sorted_files = sort_files(folder_path, sort_by)
        print(f'Отсортированные файлы: {sorted_files}')


if __name__ == '__main__':
    main()
