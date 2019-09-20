Symbol = str                # 通过 python 中的 str 对 Symbol符号表达式进行实现
Number = (int, float)       # 通过 python 中的int或float 对 Number列表表达式进行实现
Atom = (Symbol, Number)     # SimpleLisp 中的原子表达式是一个Symbol或Number
List = list                 # 通过 python 中的 list 对List列表表达式进行实现
Exp = (Atom, List)          # SimpleLisp中的 Exp表达式 是一个Atom或List
Env = dict                  # 通过 python 中的 dict 实现 SimpleLisp中的 环境Env

def tokenize(str):
    tokens = str.replace("(", " ( ").replace(")"," ) ").split()
    return tokens

def read_from_tokens(tokens):
    """
	输入：词数组
    输出：语法树

    输入词数组
    如果词数组为空，报错
    取出词数组中第一个元素
    如果此元素是‘）’符号，报错
    如果此元素是‘（’符号，准备构造语法树,只要下一个要取的元素不是‘）’符号，则从词数组中循环取元素。
         	要取的是普通字符，则取出字符，字符原子化（字符转数字，字符转字符），插入语法树中。
         	要取的是‘（’字符，开启新的语法树构造，返回新语法树，插入语法树中。
        在词数组中弹出‘）’符号
        返回构造完的语法树
    其他元素默认为原子表达式
    """
    if tokens == []:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == ")":
        raise SyntaxError("unexpected )")
    if token == "(":
        AST = []
        while tokens[0] != ")":
            if tokens[0] != "(":
                # 普通字符，则取出字符，字符原子化，插入AST中
                AST.append(atom(tokens.pop(0)))
            else:
                # （ 字符，构造新语法树，返回新AST，插入AST中
                AST.append(read_from_tokens(tokens))
        tokens.pop(0)
        return AST
    else:
        # 用户只输入了一个符号
        return atom(token)

def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

def parse(program):
    """
    功能：从字符串中读取一个表达式

    输入：字符串
    输出：抽象语法树
    """
    return read_from_tokens(tokenize(program))

import math
import operator as op
def standard_env():
    """
    生成环境
    """
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, …
    env.update({
        "+":op.add, "-":op.sub, "*":op.mul, "/":op.truediv,
        ">":op.gt, "<":op.lt, ">=":op.ge, "<=":op.le, "=":op.eq,
        "abs":     abs,
        "append":  op.add,
        "apply":   lambda proc, args: proc(args),
        "begin":   lambda *x: x[-1],
        "car":     lambda *x: x[0],
        "cdr":     lambda *x: x[1:],
        "eq?":     op.is_,
        "expt":    pow,
        "equal?":  op.eq,
        "length":  len,
        "list":    lambda *x: List(x),
        "max":     max,
        "min":     min,
        "not":     op.not_,
        "null?":   lambda x: x == [],
        "list?":   lambda x: isinstance(x, List),
        "number?": lambda x: isinstance(x, Number),
        "symbol?": lambda x: isinstance(x, Symbol),#bug 所有的simbol 都会eval变成数值
        "print":   print,   #bug 所有的simbol 都会eval变成数值
        "procedure?": callable,
        "round":   round,
    })
    return env
global_env = standard_env()

def eval(AST, env):
    """
    输入：AST，环境
    输出：结果

    如果是 数字表达式，返回数值
    如果是 符号表达式，返回在字典中找到的对应的值
    如果是 if列表表达式，求值test，如果为True，求值并返回conseq；否则求值并返回alt。
    如果是 define列表表达式，在对表达式 exp 求值，在环境中加入一组映射，key 是 symbol，
    value是表达式 exp 的值 。
    其余则是调用表达式，求值所有的 arg, 求值proc, 把proc过程应用于args值的列表
    """
    if isinstance(AST, Number):
        #print("debug the number is ", AST)
        return AST
    if isinstance(AST, Symbol):
        #print("debug the symbole is ", AST)
        return env[AST]
    if AST[0] == "if":
        (test, conseq, alt) = AST[1:]
        if eval(test, env):
            return eval(conseq, env)
        else:
            return eval(alt, env)
    if AST[0] == "define":
        (key, exp) = AST[1:]
        value = eval(exp, env)
        env[key] = value
        #print("debug just define a new value", key, value)
    else:
        proc = AST[0]
        proc = eval(proc, env)
        args = [eval(i, env) for i in AST[1:]]
        #print("degug the args is", args)
        return proc(*args)

def REPL():
    prompt = "请输入表达式："
    while True:
        userCommad = input(prompt)
        result = interpret(userCommad)
        #如果是define 之类返回None则不打印
        if result is not None:
            print(result)

def interpret(userCommad):
    return eval(read_from_tokens(tokenize(userCommad)), global_env)

REPL()
