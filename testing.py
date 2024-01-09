

def print(*args, **kwargs):
    if run.test_mode == True:
        with open('output.txt', "w") as out:
            __builtin__.print(*args, **kwargs, file=out)
        with open('output.txt', "r") as out:
            txt_batch = out.readline().strip()

        run.output_lst.append(txt_batch)
        return txt_batch
    else:
        txt = __builtin__.print(*args, **kwargs)
        return txt


def input(msg):

    if run.test_mode == True:
        batch_input = run.input_lst[run.input_counter]
        run.input_counter += 1
    else:
        batch_input = __builtin__.input(msg)
    return batch_input


class CheckAssign:

    def __init__(self,tests):
        self.test_mode = False
        self.input_counter = 0
        self.input_lst = []
        self.output_lst = []
        self.run_results = {}
        self.runs = tests



    def print_results(self):
        for key, val in self.run_results.items():
            print(key, val)

    def run_task(self,func, parms, in_list, expected_result, result_type):
        try:

            self.input_lst=in_list
            self.input_counter = 0
            self.output_lst = []
            result = eval(func + '(' + str(parms)[1:-1] + ')')
            if type(result) == tuple:
                result = list(result)
            else:
                result = [result]

            func_call = func + '(' + str(parms)[1:-1] + ')'
            if result_type == 1:
                expected_result = [str(x) for x in expected_result]
                return (self.output_lst == expected_result), func_call, '' if (
                        self.output_lst == expected_result) else 'expected print: ' + str(
                    expected_result) + ' printed: ' + str(self.output_lst)
            else:
                return (expected_result == list(result)), func_call, '' if (
                        expected_result == list(result)) else 'expected return: ' + str(
                    expected_result) + ' returned: ' + str(result)
        except Exception as e:
            func_call = func + '(' + str(parms)[1:-1] + ')'
            return False, func_call, e

    def run_test(self):
        # position4 is 1 for  print , 2 for return
        ex_count = 0
        self.test_mode = True
        for i in range(len(self.runs)):
            self.run_results[ex_count] = self.run_task(self.runs[i][0], self.runs[i][1], self.runs[i][2], self.runs[i][3], self.runs[i][4])
            ex_count += 1
        self.test_mode = False

run = CheckAssign([['exercise1', [], [10, 20], ['hello 10', 'hello 20'], 1],
        ['exercise1', [12], [10, 20], ['hello 10', 'hello 20'], 1],
        ['exercise2', [7], [10, 20, 30, 40, 50, 50, 50], [250], 1],
        ['exercise3', [40], [], [1040, 10], 2]])

run.run_test()
run.print_results()
