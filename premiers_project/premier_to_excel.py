import xlsxwriter
from premier_2023_data import array


def writer(parametr):

    book = xlsxwriter.Workbook(
        r"C:\Users\My End_1ess C\Desktop\premier_data.xlsx")
    page = book.add_worksheet("premiers")

    row = 3
    column = 1
    id = 1

    # Merge columns

    page.merge_range('B2:H2', 'Merged Range')
    page.merge_range('J2:M2', 'Merged Range')
    page.merge_range('O2:S2', 'Merged Range')
    page.merge_range('U2:V2', 'Merged Range')
    page.merge_range('X2:Z2', 'Merged Range')

    # Width columns

    page.set_column('B:B', 5)
    page.set_column('C:C', 35)
    page.set_column('D:D', 15)
    page.set_column('E:E', 5)
    page.set_column('F:F', 5)
    page.set_column('G:G', 10)
    page.set_column('H:H', 15)

    page.set_column('J:J', 5)
    page.set_column('K:K', 7)
    page.set_column('L:L', 11)
    page.set_column('M:M', 11)

    page.set_column('O:O', 5)
    page.set_column('P:P', 13)
    page.set_column('Q:Q', 16)
    page.set_column('R:R', 15)
    page.set_column('S:S', 15)

    page.set_column('U:U', 5)
    page.set_column('V:V', 15)

    page.set_column('X:X', 5)
    page.set_column('Y:Y', 15)
    page.set_column('Z:Z', 20)

    # Color

    format_for_main_headers1 = book.add_format(
        {'bg_color': '#F4FF61', 'align': 'center', 'bold': True})
    format_for_main_headers2 = book.add_format(
        {'bg_color': '#F4FF61', 'align': 'center', 'bold': True})
    format_for_main_headers3 = book.add_format(
        {'bg_color': '#F4FF61', 'align': 'center', 'bold': True})
    format_for_main_headers4 = book.add_format(
        {'bg_color': '#F4FF61', 'align': 'center', 'bold': True})
    format_for_main_headers5 = book.add_format(
        {'bg_color': '#F4FF61', 'align': 'center', 'bold': True})

    format1 = book.add_format(
        {'bg_color': '#F4FF61', 'border': 1, 'align': 'center'})
    format2 = book.add_format(
        {'bg_color': '#65FF61', 'border': 1, 'align': 'center'})
    format3 = book.add_format(
        {'bg_color': '#62FAFE', 'border': 1, 'align': 'center'})
    format4 = book.add_format(
        {'bg_color': '#6174FF', 'border': 1, 'align': 'center'})
    format5 = book.add_format(
        {'bg_color': '#FB61FF', 'border': 1, 'align': 'center'})

    # Headers

    page.write(row-2, column, 'Premiers', format_for_main_headers1)
    page.write(row-1, column, 'Id', format1)
    page.write(row-1, column+1, 'Title', format1)
    page.write(row-1, column+2, 'Duration', format1)
    page.write(row-1, column+3, 'Age', format1)
    page.write(row-1, column+4, 'Mpaa', format1)
    page.write(row-1, column+5, 'Budget', format1)
    page.write(row-1, column+6, 'Movie distributor', format1)

    page.write(row-2, column+8, 'Ratings', format_for_main_headers2)
    page.write(row-1, column+8, 'Id', format2)
    page.write(row-1, column+9, 'Rating', format2)
    page.write(row-1, column+10, 'Rating votes', format2)
    page.write(row-1, column+11, 'Rating IMDB', format2)

    page.write(row-2, column+13, 'Dates', format_for_main_headers3)
    page.write(row-1, column+13, 'Id', format3)
    page.write(row-1, column+14, 'Year of release', format3)
    page.write(row-1, column+15, 'Premiere in Russia', format3)
    page.write(row-1, column+16, 'World premiere', format3)
    page.write(row-1, column+17, 'Online premiere', format3)

    page.write(row-2, column+19, 'Genres', format_for_main_headers4)
    page.write(row-1, column+19, 'Id', format4)
    page.write(row-1, column+20, 'Genre', format4)

    page.write(row-2, column+22, 'team', format_for_main_headers5)
    page.write(row-1, column+22, 'Id', format5)
    page.write(row-1, column+23, 'Producer', format5)
    page.write(row-1, column+24, 'Main Character', format5)

    # Бежим по кортежу
    for item in parametr():

        # Id фильма
        page.write(row, column, id, format1)

        # Категории title, duration, age, mpaa, budget
        page.write(row, column+1, item[0], format1)
        page.write(row, column+2, item[5]['Продолжительность'], format1)
        page.write(row, column+3, item[5]['Возраст'], format1)
        page.write(row, column+4, item[5]['MPAA'], format1)
        page.write(row, column+5, item[5]['Бюджет'], format1)
        page.write(row, column+6, item[-2], format1)

        column += 8

        # Категория Rating
        page.write(row, column, id, format2)
        for i in range(1, 4):
            page.write(row, column+i, item[i], format2)

        column += 5

        # Категория Dates
        page.write(row, column, id, format3)
        page.write(row, column+1, item[5]['Год выпуска'], format3)
        page.write(row, column+2, item[5]['Премьера в России'], format3)
        page.write(row, column+3, item[5]['Премьера в мире'], format3)
        page.write(row, column+4, item[5]['Премьера онлайн'], format3)

        column += 6

        # Категория Genres
        for i in range(len(item[4])):
            page.write(row+i, column, id, format4)
            page.write(row+i, column+1, item[4][i], format4)

        column += 3

        # Категория Team
        for i in range(1, len(item[-1])):
            page.write(row+i-1, column, id, format5)
            page.write(row+i-1, column+1, item[-1][0], format5)
            page.write(row+i-1, column+2, item[-1][i], format5)

        # Условие для правильных вертикальных отступов между премьерами
        if len(item[4]) > len(item[-1]):
            row += len(item[4])
        else:
            row += len(item[-1])

        column = 1
        print(f'DONE  ||  ID: {id}  TITLE: {item[0]}')
        id += 1

    book.close()


writer(array)
