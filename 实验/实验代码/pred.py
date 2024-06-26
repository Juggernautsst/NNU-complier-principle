# First
def calculate_first(grammar):

    first = {}
    for non_terminal in grammar:
        first[non_terminal] = set()
    while True:
        updated = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                for symbol in production:
                    old_size = len(first[non_terminal])
                    if symbol.isupper():
                        if symbol in first:
                            first[non_terminal].update(first[symbol])
                            updated |= len(first[non_terminal]) != old_size
                    else:
                        first[non_terminal].add(symbol)
                        updated |= len(first[non_terminal]) != old_size
                    if symbol not in first or '' not in first[symbol]:
                        break
        if not updated:
            break
    return first

# Follow
def calculate_follow(grammar, first):

    follow = {}
    for non_terminal in grammar:
        follow[non_terminal] = set()
    follow['S'].add('$')
    while True:
        updated = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol.isupper():
                        if i == len(production) - 1:
                            old_size = len(follow[symbol])
                            follow[symbol].update(follow[non_terminal])
                            updated |= len(follow[symbol]) != old_size
                        else:
                            for j in range(i + 1, len(production)):
                                if production[j].islower():
                                    old_size = len(follow[symbol])
                                    follow[symbol].add(production[j])
                                    updated |= len(follow[symbol]) != old_size
                                    break
                                elif production[j].isupper():
                                    old_size = len(follow[symbol])
                                    follow[symbol].update(first[production[j]])
                                    updated |= len(follow[symbol]) != old_size
                                    if '' not in first[production[j]]:
                                        break
        if not updated:
            break
    return follow

def calculate_predict_table(grammar, first, follow):
    predict_table = {}
    for non_terminal, productions in grammar.items():
        predict_table[non_terminal] = {}
        for production in productions:
            if production[0].isupper():
                for symbol in first[production[0]]:
                    if symbol != '':
                        predict_table[non_terminal][symbol] = production
                if '' in first[production[0]]:
                    for symbol in follow[non_terminal]:
                        predict_table[non_terminal][symbol] = production
            else:
                predict_table[non_terminal][production[0]] = production
                if production[0] == '':
                    for symbol in follow[non_terminal]:
                        predict_table[non_terminal][symbol] = production
    return predict_table 

def parse(input_string, start_symbol, predict_table):
    def helper(stack, cursor, depth):
        if not stack:
            return cursor == len(input_string)
        if cursor == len(input_string) or depth > 100:  
            return False
        top = stack[-1]
        if top.isupper():
            if input_string[cursor] in predict_table[top]:
                for production in predict_table[top][input_string[cursor]]:
                    if helper(stack[:-1] + list(production[::-1]), cursor, depth + 1): 
                        return True
        else:
            if top == input_string[cursor]:
                return helper(stack[:-1], cursor + 1, depth + 1)  
            else:
                return False  

    return helper([start_symbol], 0, 0)  # Initialize depth

# 测试函数
grammar = {
    'S': ['AB', 'BC'],
    'A': ['a', 'aA'],
    'B': ['b', 'bB'],
    'C': ['c']
}
first = calculate_first(grammar)
follow = calculate_follow(grammar, first)
predict_table = calculate_predict_table(grammar, first, follow)




print('First:', first)
print('Follow:', follow)
print(predict_table)

input_string = 'c'
start_symbol = 'C'
is_recognizable = parse(input_string, start_symbol, predict_table)

print(is_recognizable)