from sympy.combinatorics import Permutation
from collections import deque
from itertools import chain
from functools import wraps
from time import time

__all__ = ['Pivrot', 'results_table']


LOG = './pivrot.log'

def timeme(args_filter=None, kwargs_filter=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t1 = time()
            ret = func(*args, **kwargs)
            t2 = time()

            with open(LOG, 'a') as log:
                log_args = args_filter(args) if args_filter else args
                log_kwargs = kwargs_filter(kwargs) if kwargs_filter else kwargs

                log.write(
                    "{:.9f}\t: '{}'\t called with '{}' args and '{}' kwargs\n"
                    "".format(t2 - t1, func.__name__, log_args, log_kwargs)
                )

            return ret
        return wrapper if LOG else func
    return decorator

def pp_pivrot_inst(pivrot):
    return "<Pivrot Inst, n: {}>".format(pivrot.set_length)

def pp_pivrot_cls(pivrot):
    return "<Pivrot Cls>"


def pp_iter(iterable):
    return "<Iterable, len: {}>".format(len(iterable))

def pp_perm(perm):
    return "<Permutation, cycles: {}>".format(perm.cycles)


def args_pp_inst(args):
    try:
        return (pp_pivrot_inst(args[0]), ) + args[1:]
    except:
        import ipdb; ipdb.set_trace()

def args_pp_cls(args):
    return (pp_pivrot_cls(args[0]), ) + args[1:]   


def args_pp_iter(args):
    return (pp_iter(args[0]), ) + args[1:]

def args_pp_perm(args):
    return (pp_perm(args[0]), ) + args[1:]

def args_pp_run(args):
    return (pp_pivrot_cls(args[0]), pp_iter(args[1])) + args[2:]


class Pivrot:
    debug = False
    log = None
    
    @property
    @timeme(args_pp_inst)
    def input(self):
        return deque(range(self.set_length))
    
    @property
    @timeme(args_pp_inst)
    def output(self):
        return self._output
    
    @property
    @timeme(args_pp_inst)
    def perm(self):
        return self._perm
    
    @property
    @timeme(args_pp_inst)
    def order(self):
        return self._order
    
    @timeme(args_pp_inst)
    def __init__(self, set_length):
        self.set_length = set_length
        self._output = self.run(self.input)
        self._perm = self.make_perm(self._output)
        self._order = self.get_order(self._perm)
        
    @staticmethod
    @timeme(args_pp_iter)
    def algorithm(iterable):
        input = deque(iterable)
        output = deque()
        while input:
            output.appendleft(input.popleft())
            input.rotate(-1)
        return output
    
    @staticmethod
    @timeme(args_pp_iter)
    def make_perm(output):
        return Permutation(output)
    
    @staticmethod
    @timeme(args_pp_perm)
    def get_order(perm):
        return perm.order()
    
    @classmethod
    @timeme(args_pp_run)
    def run(cls, iterable, order=1):
        for _ in range(order):
            iterable = cls.algorithm(iterable)
        return iterable
    
    def measure_order(self, upper_bound=100000):
        output = self.output
        i = 1
        
        while output != self.input:
            output = self.run(output)
            if i < upper_bound:
                i = i + 1
            else:
                i = -1
                break                
            
        return i
    
    def check_order(self):
        assert self.order == self.measure_order()
        
def results_table(table_range, transform=None, runner=None):
    HEADERS = [
        "base length",
        "real length",
        "perm. order",
        "cycle count",
        "cycles",
    ]
    if runner is None:
        runner = Pivrot
    
    def head():
        yield '\t'.join(HEADERS)
        yield '\t'.join('-'*len(header) for header in HEADERS)
        
    def body():
        for base_length in table_range:
            length = (
                transform(base_length)
                if transform is not None
                else base_length
            )    
            
            pivrot = runner(length)
            order = pivrot.order
            
            cycle_lengths = list(
                sorted(pivrot.perm.cycle_structure.keys())
            )
            cycle_count = len(cycle_lengths)
            
            yield '\t\t'.join(str(cell) for cell in [
                    base_length,
                    length,
                    order,
                    cycle_count,
                    cycle_lengths
            ])
    
    return chain(head(), body())
