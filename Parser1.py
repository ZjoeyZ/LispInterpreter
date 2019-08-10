def tokenize(chars):
    "将字符串转换成由token组成的列表。"
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens):
    """
    输入：以list存储的 tokends
    输出：以list方式存储的 abstract Syntax Tree

    0，检测，如果有语法错误，则报错
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
    if tokens[0] == ")":
        raise SyntaxError('unexpected )')
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    if tokens[0] != "(":
        raise SyntaxError('No ( ')

    L = []
    tokens.pop(0)
    while True:
        if tokens[0] == ")":
            break
        else:
            if tokens[0] == "(":
                L.append(read_from_tokens(tokens))
                tokens.pop(0)
            else:
                elem = tokens.pop(0)
                L.append(atom(elem))
    return L


def atom(token):
    """
        输入：字符
        输出：整型，浮点型，或者字符
    """

    #无法用 if else 语句，必须要先转化token，再判断是否是相应数据类型，但是转化失败就无法判断了
    #所以为了转化失败，让解释器不抛出错误，我们使用token
    #而要用 if else 的高级语句 try except

    # if isinstance(token, int):
    #     return int(token)
    # elif isinstance(token, float):
    #     return float(token)
    # else:
    #     return str(token)

    try:
        return int(token)
    #如果传入 int() 中的是无效参数则执行 except
    except ValueError:
        try:
            return float(token)
        #如果传入 float() 中的是有效参数则执行 except
        except ValueError:
            return str(token)


def parse(program):
    "从字符串中读取Scheme表达式"
    return read_from_tokens(tokenize(program))


if __name__ == '__main__':
    program = "(begin (define r 10) (* pi (* r r)))"
    program = parse(program)
    print(program)
