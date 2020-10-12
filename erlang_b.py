import pandas as pd
import sys

sys.setrecursionlimit(10 ** 6)

data_array = pd.DataFrame(columns=['Lines', 'Load', 'Call Loss', 'Quality'])
writer = pd.ExcelWriter('erlang.xlsx', engine='xlsxwriter', options={'strings_to_numbers': True})

answer = None
flag = True

while flag is True:
    print('Warning! Large entries on both inputs might stop the execution of the program.')

    try:
        lines = int(input('Give the number of service lines (s): '))
        load = int(input('Give the number of the traffic load (a): '))

        while lines < 0 or lines == 0:
            lines = int(input('You gave an invalid input of service lines, give again (s): '))
        while load < 0:
            load = int(input('You gave an invalid input of the traffic load (a): '))
    except ValueError:
        print('Invalid inputs were given!')
        continue

    print('')

    def grade_of_service(s, a):
        if s == 0:
            return 1
        else:
            previous_grade_of_service = grade_of_service(s - 1, a)
            return float((a * previous_grade_of_service / (s + a * previous_grade_of_service)))

    quality_of_service = (load * (1 - grade_of_service(lines, load))) / lines

    print('The probability of a call blockage is ', "{:.4f}".format(grade_of_service(lines, load)))
    print('The quality of service expressed as a probability is', "{:.4f}".format(quality_of_service))

    print('')

    print('Grade of Service in percentage: ', "{:.4f}".format(grade_of_service(lines, load) * 100))
    print('Quality of Service in percentage: ', "{:.4f}".format(quality_of_service * 100))

    print('')

    data_array = data_array.append(
        {'Lines': lines, 'Load': load, 'Call Loss': "{:.4f}".format(grade_of_service(lines, load) * 100),
         'Quality': "{:.4f}".format(quality_of_service * 100)}, ignore_index=True)

    while flag is True:
        answer = input('Do you want to continue? Yes/No: ')
        if answer == 'Yes' or answer == 'yes':
            break
        elif answer == 'No' or answer == 'no':
            flag = False
        else:
            print('Invalid reply. ')
            print('')

data_array.to_excel(writer, index=False, sheet_name='Table')

worksheet = writer.sheets['Table']

workbook = writer.book
format1 = workbook.add_format()
format1.set_align('center')
format2 = workbook.add_format()
format2.set_border()

worksheet.set_column('A:D', 10, format1)

writer.save()