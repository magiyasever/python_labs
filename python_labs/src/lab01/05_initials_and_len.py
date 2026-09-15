s = input('ФИО: ')
u = s.split()
fio = [word[0].upper() for word in u]
r = ''.join(fio)
new = ' '.join(u)
k = len(new)
print('Инициалы:', r + '.')
print('Длина (символов):', k)