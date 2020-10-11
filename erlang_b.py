"""A program used to calculate the Grade of Service and Quality of Service of a Telecommunication Network with two given inputs;
the number of service lines and traffic load respectively, inserted in the Erlang B recursive formula and as a result, it extracts
the overall call blockage and performance, both expressed as a probability and then as a percentage. With the help of the
pandas library, it is also able to create an MS Excel file named 'erlang.xlsx' which includes a table with four columns and a dynamic
multitude of rows which can be defined by how many inputs are given. https://en.wikipedia.org/wiki/Erlang_(unit)#Erlang_B_formula

This project is helpful for those who may have to check how successful a Telecommunication Network can be, by simply typing in two inputs.
Used libraries for this project is pandas and xlsxwriter as its engine."""

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

worksheet.set_column('A:A', 10, format1)
worksheet.set_column('B:B', 10, format1)
worksheet.set_column('C:C', 10, format1)
worksheet.set_column('D:D', 10, format1)

writer.save()
