from operator import add, sub, mul
from itertools import permutations 
from functools import reduce
import datetime
#operator_list = [add , sub, mul]
operator_dict = {add: '+' , sub: '-', mul: '*'}

"""
a,b,c,d

# a+b *c -d
"""

def reduce_opt(opts, alist):
    global i 
    i = -1
    def func(x, y):
        global i
        i += 1
        return opts[i](x, y)
    return reduce(func, alist)

       

def caculate_24(alist):
    result = [] 
    for per in permutations(alist):
        for ol in permutations(list(operator_dict.keys()) * 2, 3):
            #if per == (10, 2, 5, 1):
            #    print(ol, per)
            r = reduce_opt(ol, per) 
            if r == 24:
                result.append((per, ol)) 
                break
    return result 



def print_24_result(solution):
    """
    ((1 + 2) * 3) - 4
    """
    per, ols = solution 
    result = ''
    assert len(per) == 4 and len(ols) == 3
    i = 0 
    i_num = 0
    i_ol = 0
    while i < 7:
        if i == 0:
            result += '(('
        if i % 2 == 0:
            result += str(per[i_num])
            i_num += 1
            if 0 < i_ol < 3:
                result += ')'
        else:
            result += operator_dict[ols[i_ol]]
            i_ol += 1
        i += 1
    print(result)

         
 




if __name__ == '__main__':
    start = datetime.datetime.now()
    inp = [10, 2, 5, 1]
    output = caculate_24(inp) 
    print(output)
    print('用时: {}'.format(datetime.datetime.now() - start))
    for out in output:
        print_24_result(out)
