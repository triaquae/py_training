#_*_coding:utf-8_*_
__author__ = 'jieli'
import re
import sys


def remove_space(data_list):
    '''去除列表中的空格元素'''
    for i in data_list:
        if type(i) is not int:
            if len(i.strip()) == 0:
                data_list.remove(i)
    return  data_list

def fetch_data_from_bracket(data_list,first_right_bracket_pos):
    '''用递归的形式取出每一对括号里的数据并进行运算且得出结果'''
    print 'data list:',data_list

    left_bracket_pos,right_bracket_pos = data_list.index('('),data_list.index(')') +1
    print '\033[31;1mleft bracket pos:%s right_bracket_pos: %s\033[0m' %(left_bracket_pos,first_right_bracket_pos)
    data_after_strip = data_list[left_bracket_pos:right_bracket_pos]

    if data_after_strip.count("(") > 1:
        print 'fetch_data_from_bracket:%s \033[31;1m%s\033[0m left pos:%s'  %(data_after_strip,data_after_strip[1:] , left_bracket_pos)
        #return fetch_data_from_bracket(data_after_strip[left_bracket_pos+1:],first_right_bracket_pos)
        return fetch_data_from_bracket(data_after_strip[1:],first_right_bracket_pos)

    else:
        print 'last:',len(data_after_strip),data_after_strip
        bracket_start_pos = first_right_bracket_pos - len(data_after_strip) +1  # (takes two position
        calc_res = parse_operator(data_after_strip)
        return calc_res, bracket_start_pos,first_right_bracket_pos +1 #') takes one position'
def parse_bracket(formula):  #解析空格中的公式
    '''解析空格中的公式，并运算出结果'''
    pattern = r"\(.+\)"
    m = re.search(pattern,formula) #匹配出所有的括号 ‘3 / 1      - 2 * ( (60-30 * (4-2)) - 4*3/ (6-3*2) )’ 匹配完之后是'( (60-30 * (4-2)) - 4*3/ (6-3*2) )'
    if m:
        data_with_brackets = m.group()
        #print list(data_with_brackets)
        data_with_brackets = remove_space(list(data_with_brackets))
        #print data_with_brackets
        calc_res = fetch_data_from_bracket(data_with_brackets,data_with_brackets.index(')'))
        print '\033[32;1mResult:\033[0m', calc_res
        print calc_res[1],calc_res[2]
        print  data_with_brackets[calc_res[1]:calc_res[2]]
        del data_with_brackets[calc_res[1]:calc_res[2]]
        data_with_brackets.insert(calc_res[1], str(calc_res[0])) #replace formula string with caculation result 4
        return parse_bracket(''.join(data_with_brackets)) #继续处理其它的括号
    else: #no bracket in formula anymore
        print '\033[42;1mCaculation result:\033[0m' ,formula

def caculate_1(formula): # for multiplication and division
    result = int(formula[0])  # e.g ['4', '/', '2', '*', '5'], loop start from '/'
    last_operator = None
    formula = list(formula)
    nagative_mark = False
    for index,i in enumerate(formula[1:]):
        if i.isdigit():
            if nagative_mark:
                i = int('-'+i)
                nagative_mark = False
            else:
                i = int(i)
            #print '+++>',result,last_operator,i
            if last_operator == '*':
                result  *= i
            elif last_operator == '/':
                try:
                    result /= i
                except ZeroDivisionError,e:
                    print "\033[31;1mError:%s\033[0m" % e
                    sys.exit()
        elif i == '-':
            nagative_mark = True
        else:
            last_operator = i

    print '乘除运算结果:' , result
    return result
def caculate_2(data_list,operator_list):
    '''eg. data_list:['4', 3, 1372, '1']  operator_list:['-', '+', '-']'''
    data_list = remove_space(data_list)
    print 'caculater_2:',data_list,operator_list
    result = int(data_list[0])
    for i in data_list[1:]:
        if operator_list[0] == '+':
            result += int(i)
        elif operator_list[0] == '-':
            result -= int(i)
        del operator_list[0]

    print 'caculate_2 result:', result
    return  result
def parse_operator(formula):
    print '开始运算公式:',formula
    formula = formula[1:-1] #remove bracket

    low_priorities = re.findall('[+,-]',''.join(formula))
    data_after_removed_low_priorities = re.split('[+,-]', ''.join(formula))
    print '去掉加减后的公式列表,先算乘除:',data_after_removed_low_priorities

    for index,i in enumerate(data_after_removed_low_priorities):
        if i.endswith("*") or i.endswith("/") :
            data_after_removed_low_priorities[index] += '-' + data_after_removed_low_priorities[index+1]
            del data_after_removed_low_priorities[index+1]
    print '---------->handle nagative num:',data_after_removed_low_priorities
    #计算乘除运算
    nagative_mark = False

    for index,i in enumerate(data_after_removed_low_priorities):
        if not i.isdigit():
            if len(i.strip()) == 0:
                nagative_mark = True
            else:#remove space

                string_to_list = []
                if nagative_mark:
                    prior_l = '-' + i[0]  #
                    nagative_mark = False
                else:
                    prior_l = i[0]
                for l in i[1:] :
                    if l.isdigit():

                        if prior_l.isdigit() or len(prior_l) >1: # two letter should be combined
                            prior_l += l
                        else:
                            prior_l = l
                    else: # an operator * or /

                        string_to_list.append(prior_l)
                        string_to_list.append(l)
                        prior_l = l  #reset prior_l
                else:
                    string_to_list.append(prior_l)

                print '--->::', string_to_list
                calc_res = caculate_1(string_to_list) #乘除运算结果
                data_after_removed_low_priorities[index] = calc_res
                #print '--->string to list:',string_to_list
                #print '+>',index, re.split('[*,/]',i)
                '''operators = re.findall('[*,/]',i)
                data = re.split('[*,/]',i)
                combine_to_one_list = map(None,data,operators)
                combine_to_one_list =re.split("[\[,\],\(,),'',None]", str(combine_to_one_list))
                combine_to_one_list = ''.join(combine_to_one_list).split()
                print '-->',combine_to_one_list
                #print operators,data'''
            #caculate_1(combine_to_one_list)
        else :
            if nagative_mark:
                data_after_removed_low_priorities[index] = '-' + i
    print '去掉* 和 /后开始运算加减:', data_after_removed_low_priorities,low_priorities
    #计算加减运算
    return caculate_2(data_after_removed_low_priorities,low_priorities)
    #print formula
def main():
    while True:
        user_input = raw_input(">>>:").strip()
        if len(user_input) == 0:continue
        #parse_bracket(user_input)
        user_input = '(' + user_input + ')'
        #parse_bracket(' 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) ) ')
        parse_bracket(user_input)

        print '\033[43;1mpython计算器运算结果:\033[0m',eval(user_input)
if __name__ == '__main__':
    main()
