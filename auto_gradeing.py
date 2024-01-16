import pandas as pd
import urllib.request
import builtins as __builtin__



def import_tasks(grade,exercise):
  t=[]
  df = pd.read_csv('./tasks.csv',sep=',',on_bad_lines='skip',encoding='cp1255')

  df = df[df['class']==grade]
  df = df[df['exercise']==exercise]
  # df = df[df['exercise'].str.contains(1)]
  #   print(df[['function','func_arg_list','in_list','exp_out_list','output_type']])

  for key, value in df.iterrows():
    sublist=[]
    sublist.append(value["function"])
    sublist.append([]) if value["func_arg_list"]==None else  sublist.append(eval(value["func_arg_list"]))
    sublist.append([]) if value["in_list"]==None else  sublist.append(eval(value["in_list"] ))
    sublist.append([]) if value["exp_out_list"]==None else  sublist.append(eval(value["exp_out_list"]) )
    sublist.append(int(value["output_type"]))
    t.append(sublist)
  return t


run = None

def print(*args,  **kwargs):

    if run != None and run.test_mode==True:
        with open('output.txt', "w",encoding='ISO-8859-8') as out:
            __builtin__.print(*args, **kwargs, file=out)
        with open('output.txt', "r",encoding='ISO-8859-8') as out:
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

# def set_run(new_val):
#     global run
#     run=new_val



class CheckAssignment:

    def __init__(self):
        self.test_mode = False
        self.input_counter = 0
        self.input_lst = []
        self.output_lst = []
        self.run_result = {}
        # self.runs = tests




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

def run_test(tasks,student_functions):
    output = ''
    correct_answer = 0
    run_results = {}
    for k,v in student_functions.items():
        if globals().get(k)==None:
            globals()[k]=v


    ex_count = 0
    global run
    run=CheckAssignment()
    # tasks = function :0 , func_arg_list :1 ,   in_list :2  ,  exp_out_list :3  ,  output_type :4
    for i in range(len(tasks)):
        run.test_mode = True
        run_results[ex_count] = run.run_task(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3], tasks[i][4])
        run.test_mode = False
        if run_results[ex_count][0]==True:
            correct_answer+=1
            output += f'Ok {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]} \tprinted: {run.output_lst} \texpected print: {tasks[i][3]}  '
            # print(output)
            output += '\n'
        else:
            output += f'X  {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]} \tprinted: {run.output_lst} \texpected print: {tasks[i][3]}   \tError message: {run_results[ex_count][2]}'
            # print(output)
            output += '\n'

        ex_count += 1
    # print('----------')
    # print('grade:',round(100 * correct_answer / len(run_results)))
    score =round(100 * correct_answer / len(run_results))
    return score,output


