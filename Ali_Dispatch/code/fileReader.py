import csv
from Expert import Expert
from Task import Task
import copy


def getExpert():
    experts = []
    with open("../data/process_time_matrix.csv") as f:
        reader = list(csv.reader(f))
        for e in reader[1:]:
            expert = Expert()
            expert.id = int(e[0])
            for index in range(1, len(e)):
                if int(e[index]) != 999999:
                    expert.able[index] = int(e[index])

            # 根据各个专家最擅长的任务进行排序
            # expert.able = sorted(expert.able.items(), key=lambda d: d[1], reverse=False)
            experts.append(expert)

        return experts


def getTask():
    tasks = []
    with open("../data/work_order.csv") as f:
        reader = list(csv.reader(f))
        for t in reader:
            task = Task()
            task.id = int(t[0])
            task.create_time = int(t[1])
            task.category = int(t[2])
            task.response_time = int(t[3])
            tasks.append(task)
        return tasks


def resultTest():
    with open("result.csv") as f:
        reader = list(csv.reader(f))
        x = []
        for i in reader:
            x.append([int(i[0]), int(i[1]), int(i[2])])

        x.sort(key=lambda x: x[0])
        xx = []

        for i in x:
            print(i)
            if i not in xx:
                xx.append(i)
            else:
                print("已经存在：")

        # for i in xx:
        #     print(i)

        print("")
        print(len(x))
        print(len(xx))

        print("漏了")

        count = 1
        for i in x:
            if i[0] == count:
                print(i)
                count += 1
            else:
                break


if __name__ == '__main__':
    tasks = getTask()

    ex = getExpert()

    count = [0 for i in range(108)]
    for i in tasks:
        count[i.category] += 1

    for i in range(1, len(count)):
        print("任务类型：", end=" ")
        print(i, end="   任务数量：")
        print(count[i],end="   专家数量：")

        cando = 0
        for k in ex:
            if i in k.able:
                cando += 1
        print(cando,end="   ")

        print(round(count[i]/cando,1))

    #
    # count = 0
    # for i in ex:
    #     count+=len(i.able)
    #
    # print(count)