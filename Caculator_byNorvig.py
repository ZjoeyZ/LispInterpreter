Symbol = str  # 通过python中的str对Symbol进行实现
Number = (int, float)  # 通过python中的int或float对Symbol进行实现
Atom = (Symbol, Number)  # Scheme中的Atom是一个Symbol或Number
List = list  # 通过python中的list对List进行实现
Exp = (Atom, List)  # Scheme中的Exp是一个Atom或List
Env = dict  # Scheme中的environment(将在之后定义)


# 是一个{variable: value}的字典

def tokenize(chars):
    "将字符串转换成由token组成的列表。"
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens):
    """
    输入：以list存储的 tokends
    输出：以list方式存储的 abstract Syntax Tree

    0，检测，如果有')'语法错误，则报错
    1，生成空list，弹出第一个元素"("
    2，无限循环循环：取后一个的tokens元素：
                是')'
                    结束读取
                不是')'
                    是'('
                        生成子树：调用read_from_tokens
                        把生成新list 加入到这个list
                        弹出
                    不是'('
                        次元素原子化
                        加入到新的list

    3，返回 list
    """
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    if tokens[0] == ")":
        raise SyntaxError('unexpected )')

    token = tokens.pop(0)
    if token == ')':
        raise SyntaxError('unexpected )')

    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    else:
        return atom(token)


def atom(token):
    """
        输入：字符
        输出：整型，浮点型，或者字符
    """

    # 无法用 if else 语句，必须要先转化token，再判断是否是相应数据类型，但是转化失败就无法判断了
    # 所以为了转化失败，让解释器不抛出错误，我们使用token
    # 而要用 if else 的高级语句 try except

    # if isinstance(token, int):
    #     return int(token)
    # elif isinstance(token, float):
    #     return float(token)
    # else:
    #     return str(token)

    try:
        return int(token)
    # 如果传入 int() 中的是无效参数则执行 except
    except ValueError:
        try:
            return float(token)
        # 如果传入 float() 中的是有效参数则执行 except
        except ValueError:
            return str(token)


def parse(program):
    "从字符串中读取Scheme表达式"
    return read_from_tokens(tokenize(program))


import math
import operator as op


def standard_env() -> Env:
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'expt': pow,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: List(x),
        'list?': lambda x: isinstance(x, List),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'print': print,
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


global_env = standard_env()


def eval(x: Exp, env=global_env) -> Exp:
    "在一个环境中求表达式的值."
    if isinstance(x, Symbol):  # variable reference
        return env[x]
    elif isinstance(x, Number):  # constant number
        return x
    elif x[0] == 'if':  # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':  # definition
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    else:  # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)


def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop.提示-读取-计算-打印 循环"
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(schemestr(val))


def schemestr(exp):
    "Convert a Python object back into a Scheme-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


if __name__ == '__main__':
    program = "(begin (define r 10) (* pi (* r r)))"
    program = parse(program)
    print(eval(program))
    print(program)
    repl()
