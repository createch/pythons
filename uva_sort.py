#!/usr/bin/env python
"""
Solves the UVA Online Judge Sort! problem.
http://uva.onlinejudge.org/external/113/11321.html
"""

infname = 'uva_input.txt'
outfname = 'uva_output.txt'
fout = None

def write(out):
    global fout
    fout.write(str(out) + '\n')


def output(group):
    odd = []
    even = []
    for n in group:
        if n % 2 == 0:
            even.append(n)
        else:
            odd.append(n)
    odd.sort(reverse=True)
    even.sort()
    for n in odd:
        write(n)
    for n in even:
        write(n)


def main():
    global fout
    fin = open(infname, 'r')
    fout = open(outfname, 'w')
    L = []
    M = 0
    N = 0
    for line in fin:
        nums = [int(i) for i in line.split()]
        if len(nums) == 2:
            if len(L) > 0:
                print L
                for i in range(0, len(L)):
                    if L[i]:
                        output(L[i])
            N = nums[0]
            M = nums[1]
            write("%d %d" % (N, M))
            L = [None] * ((M * 2) - 1)
        elif len(nums) == 1:
            num = nums[0]
            mod = abs(num) % M
            if num < 0:
                mod *= -1
            pos = M - 1 + mod
            if not L[pos]:
                L[pos] = []
            L[pos].append(num)


if __name__ == "__main__":
    #import cProfile
    #cProfile.run("main()")
    main()
