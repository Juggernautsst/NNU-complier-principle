import numpy as np

def construct_precedence_matrix(precedence):
    # 初始化优先矩阵
    matrix = {op1: {op2: '' for op2 in precedence} for op1 in precedence}
    
    # 填充优先矩阵
    for op1 in precedence:
        for op2 in precedence:
            if op1 == '(' and op2 == ')':
                matrix[op1][op2] = '='
            elif op1 == ')' or op2 == '(':
                matrix[op1][op2] = '>'
            elif precedence[op1] < precedence[op2]:
                matrix[op1][op2] = '<'
            elif precedence[op1] >= precedence[op2]: 
                matrix[op1][op2] = '>'
            
    
    
    labeled_matrix = np.array([[''] + list(precedence.keys())])
    for op, row in matrix.items():
        labeled_matrix = np.vstack([labeled_matrix, [op] + list(row.values())])
    
    return labeled_matrix

# 定义运算符优先级
precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 0,
    ')': 0
}

# 构造优先矩阵
matrix = construct_precedence_matrix(precedence)

# 打印优先矩阵
print(matrix)
# 分析表达式的合法性
def is_valid_expression(expression, matrix):
    stack = ['#']
    for char in expression:
        if char in precedence:
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack[-1] != '(':
                    stack.pop()
                stack.pop()  # 弹出左括号
            else:
                while stack[-1] in precedence and precedence[stack[-1]] > precedence[char]:
                    stack.pop()
                stack.append(char)
        else:
            stack.append(char)
    return True

# 计算表达式的值
def evaluate_expression(expression):
    try:
        return eval(expression)
    except Exception as e:
        return str(e)


expression = "1+2-4*4/8"
matrix = construct_precedence_matrix(precedence)
if is_valid_expression(expression, matrix):
    result = evaluate_expression(expression)
    print(f"The result of the expression is: {result}")
else:
    print("The expression is not valid.")
