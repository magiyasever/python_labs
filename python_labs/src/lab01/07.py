s = input()
first = next(i for i, ch in enumerate(s) if ch.isupper())
digit_pos = next(i for i, ch in enumerate(s) if ch.isdigit())
step = (digit_pos + 1) - first
result = []
i = first
while True:
    result.append(s[i])
    if s[i] == '.':
        break
    i += step

print(''.join(result))