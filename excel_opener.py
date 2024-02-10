import pyexcel
from pyexcel._compact import OrderedDict
import os


def open_xlsx(file_path: str, file_name: str):
    idx = file_name.rfind('.')
    os.mkdir(f'{file_name[:idx]}')

    my_dict = pyexcel.get_dict(file_name=file_path, name_columns_by_row=0)

    phase_dif = my_dict.get('Разность фаз, гад')
    chanel_2 = my_dict.get('Канал 2, Y, дБ/В')
    chanel_1 = my_dict.get('Канал 1, Y, дБ/В')
    xs = int(my_dict.get('X, отсчёты')[-1]) + 1

    with open(f'{file_name[:idx]}/data_{file_name}.txt', 'w') as file:
        file.write('X, отсчёты\tКанал 1, Y, дБ/В\tКанал 2, Y, дБ/В\tРазность фаз, град.\n')
        for i in range(xs):
            file.write(f'{i}\t{chanel_1[i]}\t{chanel_2[i]}\t{phase_dif[i]}\n')
    file.close()


def open_txt(file_path: str, file_name: str):
    idx = file_name.rfind('.')

    if not os.path.exists(f'{file_name[:idx]}/data_{file_name}.txt'):
        open_xlsx(file_path, file_name)
    with open(f'{file_name[:idx]}/data_{file_name}.txt', 'r') as file:
        lines = file.readlines()
        data = tuple(line.split('\t') for line in lines)
    file.close()
    return data


def open_correlation_txt(index_data: int, excel_file: str):
    idx = excel_file.rfind('.')

    with open(f'{excel_file[:idx]}/correlation_txt{index_data}_{excel_file}.txt', 'r') as file:
        lines = file.readlines()
        data = tuple(line.split('\t') for line in lines)
    file.close()
    return data, 1


def create_correlation_txt(data: tuple, index_data: int, excel_file: str):
    idx = excel_file.rfind('.')
    y, x = data

    with open(f'{excel_file[:idx]}/correlation_txt{index_data}_{excel_file}.txt', 'w') as file:
        for i in range(0, len(x)):
            file.write(f'{y[i]}\t{i}\n')
    file.close()
