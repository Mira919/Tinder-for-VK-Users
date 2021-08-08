import datetime

start_time = datetime.datetime.now()
print(f'Программа начала свою работу')

finish_time = datetime.datetime.now()
run_time = finish_time - start_time
print('Программа закончила работу')
print(f'Программа выполнялась {str(run_time)[:9]} секунды')