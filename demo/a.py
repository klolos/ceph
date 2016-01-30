def f(l=[], a=None):
    if a:
        l.append(a)
    print l


if __name__ == "__main__":
    f([1], 5)
    f(a=3)
    f(a=4)

