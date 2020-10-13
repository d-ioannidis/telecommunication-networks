import pandas as pd
import plotly.express as px
import csv

outfile = open('call_performance.csv', 'w', newline='')
w = csv.writer(outfile)

answer = None
flag = True

w.writerow(['Grade of Service (Percentage)', 'Concluded Load (Erl)'])

while flag is True:
    try:
        calls = int(input('Give the number of calls: '))
        duration = int(input('Give the duration of the calls (in minutes): '))
        missed_calls = int(input('Give the number of missed calls: '))

        while calls < 0:
            calls = int(input('Invalid input for calls, give again: '))
        while duration < 0:
            duration = int(input('Invalid input for duration, give again (in minutes): '))
        while missed_calls < 0 or missed_calls == 0:
            missed_calls = int(input('Invalid input for missed calls, give again: '))
    except ValueError:
        print('You gave an invalid input! Please give again said inputs.')
        continue

    print('')

    offered_load_erlangs = (calls * duration) / 60
    concluded_load_erlangs = (calls - missed_calls) * duration / 60
    lost_load_erlangs = offered_load_erlangs - concluded_load_erlangs

    offered_load_ccs = offered_load_erlangs * 36
    concluded_load_ccs = concluded_load_erlangs * 36
    lost_load_ccs = lost_load_erlangs * 36

    grade_of_service = lost_load_erlangs / offered_load_erlangs
    grade_of_service_percentage = grade_of_service * 100

    w.writerow(["{:.4f}".format(grade_of_service_percentage), "{:.4f}".format(concluded_load_erlangs)])

    print('The offered traffic load is (in Erlangs): ', "{:.4f}".format(offered_load_erlangs))
    print('The offered traffic load is (in CCS): ', "{:.4f}".format(offered_load_ccs))
    print('')
    print('The concluded traffic load is (in Erlangs): ', "{:.4f}".format(concluded_load_erlangs))
    print('The concluded traffic load is (in CCS): ', "{:.4f}".format(concluded_load_ccs))
    print('')
    print('The lost traffic load is (in Erlangs): ', "{:.4f}".format(lost_load_erlangs))
    print('The lost traffic load is (in CCS): ', "{:.4f}".format(lost_load_ccs))
    print('')
    print('The grade of service is: ', "{:.4f}".format(grade_of_service))

    while flag is True:
        answer = input('Do you want to continue? Yes/No: ')
        if answer == 'Yes' or answer == 'yes':
            break
        elif answer == 'No' or answer == 'no':
            flag = False
            continue
        else:
            print('Invalid reply given.')
    print('')

outfile.close()

df = pd.read_csv('call_performance.csv')
fig = px.line(df, x='Concluded Load (Erl)', y='Grade of Service (Percentage)',
              title='Grade of Service as a function of the given Concluded Load in Erlangs.')

fig.show()
