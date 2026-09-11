s = input('ФИО: ')
u = s.split()
fio = [u[0][0], u[1][0], u[2][0]]
k = len(s.strip())
r = ''.join(fio)
print('Инициалы:', r)
print('Длина (символов):', k)
