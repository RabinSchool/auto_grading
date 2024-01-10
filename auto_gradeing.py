tasks1=[
                                ['exercise1', [], [10, 20], ['hello 10', 'hello 20'], 1],
                                ['exercise1', [12], [10, 20], ['hello 10', 'hello 20'], 1],
                                ['exercise2', [7], [10, 20, 30, 40, 50, 50, 50], [250], 1],
                                ['exercise3', [40], [], [1040, 10], 2]
      ]
class CheckAssignment:

    def __init__(self):
        self.test_mode = False
        self.input_counter = 0
        self.input_lst = []
        self.output_lst = []
        self.run_results = {}
        # self.runs = tests



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

    def run_test(self,tasks,student_functions):
        for k,v in student_functions.items():
            if globals().get(k)==None:
                globals()[k]=v
        # position4 is 1 for  print , 2 for return
        ex_count = 0
        self.test_mode = True
        for i in range(len(tasks)):
            self.run_results[ex_count] = self.run_task(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3], tasks[i][4])
            ex_count += 1
        self.test_mode = False
