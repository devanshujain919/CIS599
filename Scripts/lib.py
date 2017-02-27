def __Levenshtein(str1, i, str2, j):
    print(i,j)
    if i <= 0 or j <= 0:
        return max([i, j])
    arr = [__Levenshtein(str1, i-1, str2, j) + 1, __Levenshtein(str1, i, str2, j-1) + 1]
    if str1[i - 1] != str2[j - 1]:
        arr.append(__Levenshtein(str1, i-1, str2, j-1) + 1)
    else:
        arr.append(__Levenshtein(str1, i-1, str2, j-1))
    return min(arr)

def Levenshtein(str1, str2):
    print(str1)
    print(len(str1))
    print(str2)
    print(len(str2))
    return __Levenshtein(str1, len(str1), str2, len(str2))

if __name__ == "__main__":
    print(Levenshtein("Badan_Singh", "n_singhdb"))