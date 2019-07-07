import random
import time
from copy import deepcopy

from app.models import Job
from .. import db


from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

max_machine = 6
max_jops = 36



gunter_matrix = []
time_matrix = []
gunter_drawing_matrix = []
gunter_drawing_tag = ('加工跑道', '工件加工顺序', '工件序号', '加工时间', '工件约束', '跑道约束', '起始时间', '结束时间')

for_cart_lists_x = []
for_cart_lists_y = []
for_gunter_y = []
for_gunter_width = []
for_gunter_color = []
for_gunter_start = []
for_cart_name = ['iteration times', 'time']


# 判断一个解是否为有效解
def determination(solution):
    # 键为产品, 值为机器
    _dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    # _dict = {1: [], 2: [], 3: []}
    for operation in solution:
        _dict[operation[0]].append(operation[1])
        if len(_dict[operation[0]]) > 1:
            if _dict[operation[0]][-1] < _dict[operation[0]][-2]:
                return 'Infeasible solution'
    return 'feasible solution'


# 计算一个解的排程时间
def calculate_total_time(solution, context):
    if determination(solution) == 'Infeasible solution':
        return 'Infeasible solution'

    # 键为机器，值为产品
    _dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    # _dict = {1: [], 2: [], 3: []}
    # 创建机器进度指针和产品进度指针
    machine_pointer = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    product_poniter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    # machine_pointer = {1: 0, 2: 0, 3: 0}
    # product_poniter = {1: 0, 2: 0, 3: 0}
    for operation in solution:
        _dict[context[operation[0]][operation[1]][0]].append(operation[0])
        # operation[0]:产品编号 operation[1]：工序编号
        # context[operation[0]][operation[1]][0]:机器编号
        start = max(machine_pointer[context[operation[0]]
        [operation[1]][0]], product_poniter[operation[0]])
        end = start + context[operation[0]][operation[1]][1]
        machine_pointer[context[operation[0]][operation[1]][0]] = end
        product_poniter[operation[0]] = end
    return max([machine_pointer[i] for i in machine_pointer]), _dict


# 实施退火算法
def simulated_annealing_algorithm(solution, T, alpha, Tend, context):
    '''
    solution:初始解
    T:初始温度
    alpha:温度衰减系数0
    Tend:温度衰减的最低值
    '''
    # 出现过的最优解
    best_solution = {'objective': calculate_total_time(solution, context)[0],
                     'machine-schedule': calculate_total_time(solution, context)[1],
                     'solution': deepcopy(solution)}
    # 生成一组可行解
    solutions = []
    for _ in range(20):
        # 生成新的20个可行解
        new_performance = 'Infeasible solution'
        while new_performance == 'Infeasible solution':
            int_1 = random.randint(0, 7)
            int_2 = random.randint(0, 7)
            tmp_solution = deepcopy(solution)
            tmp_solution[int_1], tmp_solution[int_2] = tmp_solution[int_2], tmp_solution[int_1]
            new_performance = calculate_total_time(tmp_solution, context)
        solutions.append(tmp_solution)

    # 总迭代次数
    iteration = 0
    # 在同一目标值时的重复次数
    iteration_at_optimal = 0

    # 终止条件为温度降到Tend或者连续无法出现最优解的次数达到1000次
    while T >= Tend and iteration_at_optimal <= 1000:
        iteration += 1  # 自增迭代次数
        for index, one_solution in enumerate(solutions):
            old_solution = deepcopy(one_solution)
            old_performance = calculate_total_time(old_solution, context)
            # 生成新的可行解
            new_performance = 'Infeasible solution'
            while new_performance == 'Infeasible solution':
                int_1 = random.randint(0, 7)
                int_2 = random.randint(0, 7)
                solution = deepcopy(old_solution)
                solution[int_1], solution[int_2] = solution[int_2], solution[int_1]
                new_performance = calculate_total_time(solution, context)
            # 如果新解的目标值优于已知最优解，则取代已知最优解
            if new_performance[0] <= best_solution['objective']:
                best_solution = {'objective': new_performance[0],
                                 'machine-schedule': new_performance[1],
                                 'solution': deepcopy(solution)}
            # 计算新解和其上一个解的目标值差值（新解为其上一个解的邻解）
            delta = new_performance[0] - old_performance[0]
            # 如果有优化，则在新目标值得重复次数重设为0
            if delta < 0:
                iteration_at_optimal = 0
            # 如果没有优化，则一定概率退回上一个解，或以新解作为下一次迭代的起点
            elif delta == 0:
                iteration_at_optimal += 1
            else:  # delta > 0
                iteration_at_optimal += 1
                rand = random.uniform(0, 1)
                keep_probability = np.exp(-delta / T)
                if keep_probability > rand:
                    pass  # 保留当前的解
                else:  # 保留上一次的解
                    solution = old_solution
            solutions[index] = solution
        T = alpha * T  # 温度的衰减使得保留当前劣解的概率降低

        if iteration % 100 == 0:
            for_cart_lists_x.append(iteration)
            for_cart_lists_y.append(best_solution['objective'])

    print('退出迭代时的参数状态：', T, '>=', Tend, ',', iteration_at_optimal, '<=', 1000)
    return best_solution, iteration


def make_gunter_matrix(solutions, contexts):
    index = 0
    for solution in solutions:
        row = solution[0]
        column = solution[1]
        single_context = contexts[row][column]
        # 指针 跑道 工件 时间
        single_gunter_element = (index, row, single_context[0], single_context[1])
        index += 1
        gunter_matrix.append(single_gunter_element)

    last_appear_machine = [0, -1, -1, -1, -1, -1, -1]
    last_appear_jop = [0, -1, -1, -1, -1, -1, -1]

    for e in gunter_matrix:
        if last_appear_machine[e[1]] == -1 and last_appear_jop[e[2]] == -1:
            time_matrix.append((e[0], 0, 0, e[3], e[3]))
        else:
            if last_appear_machine[e[1]] != -1 and last_appear_jop[e[2]] == -1:
                time_matrix.append((e[0], time_matrix[last_appear_machine[e[1]]][3]
                                    , 0, time_matrix[last_appear_machine[e[1]]][3] + e[3], e[3]))

            elif last_appear_jop[e[2]] != -1 and last_appear_machine[e[1]] == -1:
                time_matrix.append((e[0], 0, time_matrix[last_appear_jop[e[2]]][3]
                                    , time_matrix[last_appear_jop[e[2]]][3] + e[3], e[3]))

            elif last_appear_machine[e[1]] != -1 and last_appear_jop[e[2]] != -1:
                if time_matrix[last_appear_machine[e[1]]][3] > time_matrix[last_appear_jop[e[2]]][3]:
                    time_matrix.append((e[0], time_matrix[last_appear_machine[e[1]]][3]
                                        , time_matrix[last_appear_jop[e[2]]][3]
                                        , time_matrix[last_appear_machine[e[1]]][3] + e[3], e[3]))
                elif time_matrix[last_appear_machine[e[1]]][3] < time_matrix[last_appear_jop[e[2]]][3]:
                    time_matrix.append((e[0], time_matrix[last_appear_machine[e[1]]][3]
                                        , time_matrix[last_appear_jop[e[2]]][3]
                                        , time_matrix[last_appear_jop[e[2]]][3] + e[3], e[3]))
                else:
                    time_matrix.append((e[0], time_matrix[last_appear_machine[e[1]]][3]
                                        , time_matrix[last_appear_jop[e[2]]][3]
                                        , time_matrix[last_appear_machine[e[1]]][3] + e[3], e[3]))
        last_appear_machine[e[1]] = e[0]
        last_appear_jop[e[2]] = e[0]


def draw_gunter_graph(g_matrix, t_matrix):
    plt.figure('figure2', figsize=(12, 4), dpi=250)
    names = []
    for t in t_matrix:
        for_gunter_start.append(t[3] - t[4])
    for g in g_matrix:
        for_gunter_y.append(g[1])
        for_gunter_width.append(g[3])
        if g[2] == 1:
            for_gunter_color.append("red")
        elif g[2] == 2:
            for_gunter_color.append("blue")
        elif g[2] == 3:
            for_gunter_color.append("orange")
        elif g[2] == 4:
            for_gunter_color.append("green")
        elif g[2] == 5:
            for_gunter_color.append("gray")
        elif g[2] == 6:
            for_gunter_color.append("purple")

    plt.barh(y=for_gunter_y, width=for_gunter_width, height=0.3, left=for_gunter_start
             , align="center", color=for_gunter_color)
    plt.yticks((1, 2, 3, 4, 5, 6),
               (u'Machine 1', u'Machine 2', u'Machine 3', u'Machine 4', u'Machine 5', u'Machine 6'))
    plt.title('Gunter Graph')
    print(names)
    dtime = datetime.now()
    un_time = time.mktime(dtime.timetuple())
    path = '/Projects/PyCharm/PyMES/app/static/img/gunter/gunter_cart' + int(un_time).__str__() + '.png'
    filename = 'gunter_cart' + int(un_time).__str__() + '.png'
    plt.savefig(path)
    plt.show()
    return path, un_time, filename


def calculate_result(input_path, context, init_solution, order_id):
    best_solution, iteration = simulated_annealing_algorithm(
        init_solution, 0.04, 0.999, 0.001, context)
    make_gunter_matrix(best_solution['solution'], context)
    input_path, un_time, filename = draw_gunter_graph(gunter_matrix, time_matrix)
    result = Job(id=int(un_time).__str__(),
                 order_id=order_id,
                 input_path=input_path.__str__(),
                 best_time=best_solution['objective'].__str__(),
                 best_aps=best_solution['machine-schedule'].__str__(),
                 best_solution=gunter_matrix.__str__(),
                 result_img_path='/static/img/gunter/' + filename)
    db.session.add(result)
    db.session.commit()

    return result.id



