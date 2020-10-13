class Expert:
    id = 0

    able = {}  # 能做的任务 {taskId : time}

    conc = []  # 现在做的任务 {Task}

    def __init__(self):
        self.able = {}
        self.conc = []

    # 计算各个任务擅长度
    def proficiency(self, key):
        sorted_able = sorted(self.able.items(), key=lambda x: x[1], reverse=False)
        count = 0
        for i in sorted_able:
            if i[0] == key:
                count += 1
                break
            else:
                count += 1
        return round(1 - count / len(sorted_able) + 1 / len(sorted_able), 1)

    def print(self):
        print("expert_id：" + str(self.id), end="  what i can do： ")
        print(self.able)


if __name__ == '__main__':
    x = Expert()
    x.able = {1: 36, 2: 20, 3: 40, 4: 17, 5: 82, 6: 34}
    print(x.proficiency(1))
    print(x.proficiency(2))
    print(x.proficiency(3))
    print(x.proficiency(4))
    print(x.proficiency(5))
    print(x.proficiency(6))
