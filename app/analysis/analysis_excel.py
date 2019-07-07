import xlrd

context = {1: {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0)},
           2: {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0)},
           3: {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0)},
           4: {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0)},
           5: {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0)},
           6: {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0)}}

init_solution = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
                 (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
                 (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
                 (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                 (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5),
                 (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)]


def resolve_excel(path):
    data = xlrd.open_workbook(path, encoding_override='utf-8')
    sheet = data.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    if sheet.cell(0, 0).value == 'MES':
        for i in range(1, nrows):
            for j in range(1, ncols):
                elem = (int(sheet.cell(i, j).value.split(',')[0]), int(sheet.cell(i, j).value.split(',')[1]))
                context[i][j] = elem

    return context, init_solution
