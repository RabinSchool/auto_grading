import builtins as __builtin__
import pandas as pd

run = None

def print(*args,  **kwargs):

    if run != None and run.test_mode==True:
        with open('output.txt', "w") as out:
            __builtin__.print(*args, **kwargs, file=out)
        with open('output.txt', "r") as out:
            txt_batch = out.readline().strip()
        run.output_lst.append(txt_batch)
        return txt_batch
    else:
        txt = __builtin__.print(*args, **kwargs)
        return txt

def input(prompt=None):
    if run != None and run.test_mode==True:
        batch_input = run.input_lst[run.input_counter]
        run.input_counter += 1
    else:
        batch_input = __builtin__.input(prompt)
    return batch_input

def set_run(new_val):
    global run
    run=new_val



def import_tasks(grade,exercise):
  t=[]
  df = pd.read_csv('/content/tasks.csv',sep=';',on_bad_lines='skip')

  df = df[df['class']==grade]
  df = df[df['exercise']==exercise]
  # df = df[df['exercise'].str.contains(1)]
  # print(df[['function','func_arg_list','in_list','exp_out_list','output_type']])
  for i in range(len(df)):
    sublist=[]
    sublist.append(df.loc[i, "function"])
    sublist.append([]) if df.loc[i, "func_arg_list"]==None else  sublist.append(eval(df.loc[i, "func_arg_list"]))
    sublist.append([]) if df.loc[i, "in_list"]==None else  sublist.append(eval(df.loc[i, "in_list"] ))
    sublist.append([]) if df.loc[i, "exp_out_list"]==None else  sublist.append(eval(df.loc[i, "exp_out_list"]) )
    sublist.append(int(df.loc[i, "output_type"]))
    t.append(sublist)
  return t

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
