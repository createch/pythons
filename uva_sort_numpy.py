#!/usr/bin/env python
"""
Uses NumPy to solve the UVA Online Judge Sort! problem.
http://uva.onlinejudge.org/external/113/11321.html
"""

import numpy
import linecache

out_str = ""

def write(out, fout):
    global out_str
    fout.write(str(out) + '\n')
    out_str += str(out) + '\n'


def write_set(N, M, arr, sorted_order, fout):
    out_str = "%s %s\n" % (N, M)
    buffer_count = 0
    for i in sorted_order:
        out_str += str(arr[i]['num'][0][0]) + "\n"
        buffer_count += 1
        if buffer_count == 500:
            fout.write(out_str)
            out_str = ""
            buffer_count = 0
    fout.write(out_str)


def main():
    fin_name = 'uva_input.txt'
    fout = open('uva_output.txt', 'w')

    line_num = 0
    N = 0
    M = 0
    arr = None
    row = 0
    new_set_line_number = 0

    for line_num, line in enumerate(open(fin_name, 'r')):

        if line_num == new_set_line_number:
            if arr is not None:
                print "built array, now sorting"
                sorted_order = numpy.argsort(arr, axis=0, order=['mod', 'even'])
                print "sorted array, now writing"
                # write_set(N, M, arr, sorted_order, fout)
            print "new  set"
            arr = None
            new_set = [int(i) for i in line.split()]
            N = new_set[0]
            M = new_set[1]
            if N == 0:
                fout.write("0 0\n")
                break
            print N, M
            new_set_line_number += N + 1
            dtype = [('num', 'int32'), ('even', 'int32'), ('mod', 'int32')]
            arr = numpy.empty((N, 1), dtype=dtype)
            row = 0
        else:
            num = int(line)
            mod = abs(num) % M
            if num < 0:
                mod *= -1
            if num % 2 == 0:
                even = num
            else:
                even = num * -1
            arr[row] = (num, even, mod)
            row += 1


if __name__ == "__main__":
    profile = True
    if profile:
        import cProfile
        cProfile.run("main()")
    else:
        main()
