def tokenize(chars):
    "将字符串转换成由token组成的列表。"
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    "从字符串中读取Scheme表达式"
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):
    """
    输入：tokens list 输出：list
    0，检测，如果有语法错误，则报错
    1，生成空list
    2,
        while
            取后一个的tokens元素，不是')'
                true
                    不是（
                        true：元素原子化，加入到新的list,重复
                        false：调用read_from_tokens 生成新list 加入到这个list
                        弹出 token 中的 第一个 ）
                false
                    break
    3，返回 list
    """
    if tokens[0] == ")":
        raise SyntaxError('unexpected )')
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')

    # print("Debug: ")
    # print("Debug: now the tokens is ", tokens)

    if tokens[0] != "(":
        raise SyntaxError('No ( ')

    L = []
    tokens.pop(0)
    while True:
        if tokens[0] != ")":
            if tokens[0] != "(":
                elem = tokens.pop(0)
                # print("Debug: add elem ", elem, "to ", L)
                L.append(atom(elem))
            else:
                L.append(read_from_tokens(tokens))
                tokens.pop(0)
        else:
            break
    return L


def atom(token):
    "数字转为对应的Python数字，其余的转为符号"
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


if __name__ == '__main__':
    program = "(begin (define r 10) (* pi (* r r)))"
    program = parse(program)
    print(program)
