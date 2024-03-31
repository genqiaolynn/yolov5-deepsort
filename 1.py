def pairs(s):
    count = 0
    one_count = 0
    n = len(s)

    for i in range(n):
        if s[i] == '1':
            one_count += 1
            count += one_count

    return count


if __name__ == "__main__":
    print(pairs("100101"))         # Output: 10
    print(pairs("101"))            # Output: 2
    print(pairs("100100111001"))   # Output: 19