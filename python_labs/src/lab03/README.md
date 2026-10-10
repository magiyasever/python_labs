Отчет по лабораторной работе №3 — Тексты и частоты слов

Задание A — Библиотечный модуль src/lib/text.py

Реализован переиспользуемый модуль src/lib/text.py, содержащий функции для нормализации текста, токенизации, подсчета частоты слов и формирования топа слов.

1. Функция normalize

Преобразует строку: приведение к нижнему регистру (casefold), замена ё/Ё на е/Е и удаление управляющих символов и лишних пробелов.



def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    '''Нормализует текст
    Args:
        text: Исходный текст
        casefold: Bool значение
                    True: Переводит все буквы в строчные
                    False: Оставляет всё как есть
        yo2e: Заменяет ё/Ё на е/Е

    Returns:
        обработанный текст
    '''
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()

    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
    
    result = []
    for char in text:
        if unicodedata.category(char) == "Cc":
            result.append(' ')
        else:
            result.append(char)
    new_text = ''.join(result)
    return ' '.join(new_text.split())



<img width="359" height="108" alt="Снимок экрана — 2026-10-10 в 16 49 52" src="https://github.com/user-attachments/assets/813179c0-7a39-444a-bc14-1a21e6308a15" /> 


Рис. 1. Результат работы и тестов функции normalize
