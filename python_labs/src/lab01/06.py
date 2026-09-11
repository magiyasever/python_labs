s = int(input())
ochno = 0
zaochno = 0
for _ in range(s):
    a = input().split()
    format = a[-1]
    if format == 'True':
        ochno += 1
    elif format == 'False':
        zaochno += 1
print(f'Очная форма: {ochno}, Заочная форма: {zaochno}')