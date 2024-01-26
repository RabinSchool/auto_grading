import pandas as pd
import urllib.request
import builtins as __builtin__

# the key is the MD file source
questions_dic={
    '2':[2,3,4],
    '3':[9,10,11,12,13,14,15],
    '4':[4,5,6,7,8,9],
    '5':[1,2,3,4,5,6,7],
    '6':[2,3,4,5,6],
    '7a':[2,3,4,5,6,7,8,9,10,11,12],
    '7b':[100,101,102,103,104,107],
    '8a':[2,3,4,5],
    '8b':[11,12,13,14,15,16,17,18],
    '9':[],
    '10':[],
    '11':[4,6,7,8,9,10,11,12,13,14], # strings
    # '12':['3a','3b','4a','4b','5a','5b','6a',6,'7a','7b','8a','8b','9a','9b'], # functions
    '12a':['3a','3b','4a','4b','5a','5b','6a',6,'7a','7b'], # functions
    '12b':['8a','8b','9a','9b'], # functions
    '13a':[5,6,7,8],
    '13b':[101,102,103,104,105,106,107],
    '14':[201,202,203,204]
   }

def get_questions(exercise_key):
  if questions_dic.get(exercise_key)!=None:
    return questions_dic[exercise_key]
  else:
    return []
  

def import_tasks(grade,question_set,questions ):
  t=[]
  df = pd.read_csv('./tasks.csv',sep=',',on_bad_lines='skip',encoding='utf-8')

  df = df[df['class']==grade]
  df.question_set = df.question_set.astype(str)
  # ignore last letter of exercise_set
  exerciser_set=str(question_set)[:-1] if not str(question_set).isnumeric() else str(question_set)
  df = df[df['question_set'].isin([exerciser_set])]     
  df = df[df['function'].isin([f'ex{str(q)}' for q in questions]) ]
  # df = df[df['question_set'].str.contains(1)]
  #   print(df[['function','func_arg_list','in_list','exp_out_list','return_values']])

  for key, value in df.iterrows():
    sublist=[]
    sublist.append(value["function"])
    sublist.append([]) if value["func_arg_list"]==None else  sublist.append(eval(value["func_arg_list"]))
    sublist.append([]) if value["in_list"]==None else  sublist.append(eval(value["in_list"] ))
    sublist.append([]) if value["exp_out_list"]==None else  sublist.append(eval(value["exp_out_list"]) )
    sublist.append([]) if value["return_values"]==None else  sublist.append(eval(value["return_values"]) )
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




    def run_task(self,func, parms, in_list, expected_result, return_values):
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
            expected_result = [str(x) for x in expected_result]
            if self.output_lst == expected_result:
              if (return_values == list(result)):
                return True,func_call,'Excellent'
              else:
                return False,func_call,f'Returned: {str(result)} != Expected return: {str(return_values)}'
            else:
              if (return_values == list(result)):
                return False,func_call,f'Printed: {str(self.output_lst)} != Expected print: {str(expected_result)}'
              else:
                return False,func_call,f'Returned: {result} != Expected return: {str(return_values)} and Printed: {str(self.output_lst)} != Expected print: {str(expected_result)}'
          

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
    # tasks = function :0 , func_arg_list :1 ,   in_list :2  ,  exp_out_list :3  ,  return_values :4
    for i in range(len(tasks)):
        run.test_mode = True
        run_results[ex_count] = run.run_task(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3], tasks[i][4])
        run.test_mode = False

        if run_results[ex_count][0]==True:
            correct_answer+=1
            output += f'Ok {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]}  '
            # print(output)
            output += '\n'
        else:
            output += f'X  {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]} \tMessage: {run_results[ex_count][2]}'
            # print(output)
            output += '\n'

        ex_count += 1
    # print('----------')
    # print('grade:',round(100 * correct_answer / len(run_results)))
    if  len(run_results)!=0:
      score =round(100 * correct_answer / len(run_results))
    else:
      score = 0
    return score,output


