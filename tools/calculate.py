def calculate(query, history):
    print('[TOOL] calculate', query)
    res = eval(query)
    print('[TOOL] calculate -> ', res)
    return res