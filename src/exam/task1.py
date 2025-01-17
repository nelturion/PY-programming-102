def longest_common_prefix(strs):
    if not strs:
        return ""

    # Инициализируем префикс первой строкой (максимум совпадения префиксов)
    prefix = strs[0]

    # Сравниваем с каждой строкой в массиве и уменьшаем префикс, пока он не станет общим для текущей строки
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]  # Убираем последний символ
            if not prefix:  # Если префикс стал пустым
                return ""

    return prefix

# Использование:
strs = ["flower", "flow", "flight"]
result = longest_common_prefix(strs)
print(result)

strs = ["aaabcccc", "aaabccc", "aaabcc", "aaab"]
result = longest_common_prefix(strs)
print(result)
