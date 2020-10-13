from fileReader import *
import copy


def fillRes(res=[]):
    f = open("result.csv", "w", encoding="utf-8", newline="")
    [csv.writer(f).writerow(i) for i in res]
    f.close()


# 打印专家群目前的状态
def expertsStatus(experts=[]):
    a, b, c, d, e = 0, 0, 0, 0, 0

    for i in experts:
        if len(i.conc) == 0:
            a += 1
        elif len(i.conc) == 1:
            b += 1
        elif len(i.conc) == 2:
            c += 1
        elif len(i.conc) == 3:
            d += 1
        else:
            e += 1
    print("超负荷:" + str(e) + "人 " + " 满负荷:" + str(d) + "人   双任务: " + str(c) + "人  单任务: " + str(b) + "人  无任务:" + str(a))


# 根据category获得当前可用的专家
def availableExperts(category=""):
    return [i for i in experts if category in i.able.keys() and i.conc.__len__() < 3]


if __name__ == '__main__':
    tasks = getTask()
    experts = getExpert()

    time = 481
    res = []
    hover_task = []  # 当前待执行任务队列
    stop = False

    while (len(res) != 8840):

        # 去除每个专家在当前时间已经完成的任务 && 添加结果
        for e in experts:
            if len(e.conc) > 3:
                print("并发超限")

            for t in e.conc:
                if t.end <= time:
                    if t.redirect > 5:
                        print("转发次数超限")
                        t.print()
                    if [t.id, e.id, t.start] in res:
                        print("重复内容")

                    res.append([t.id, e.id, t.start])
                    e.conc.remove(t)

        # 转移任务NTR，（防止牛逼的人闲着，垃圾别做了，让空闲的大佬做）
        # 遍历每个专家的每个任务，if 待执行时间 > 当前能解决的专家的最快时间，对其进行转移，转移次数不超过5
        for e in experts:
            for t in e.conc:
                wait_time = t.end - time
                cur_experts = [i for i in experts if t.category in i.able.keys() and len(i.conc) < 3 and i != e]
                cur_experts.sort(key=lambda x: x.able[t.category], reverse=False)

                for cur_expert in cur_experts:
                    if wait_time > cur_expert.able[t.category] and t.redirect < 5:
                        # 换人
                        e.conc.remove(t)
                        t.start = time
                        t.end = t.start + cur_expert.able[t.category]
                        t.redirect += 1
                        cur_expert.conc.append(t)
                        break

        # 获得当前时刻发布的所有任务
        cur_tasks = [i for i in tasks if i.create_time == time]

        # 把当前任务加入hover_task，剩余响应时间低的优先
        hover_task += cur_tasks
        hover_task.sort(key=lambda x: x.response_time)

        for t in hover_task:

            # #优先处理任务类型为1的任务
            # if t.category == 1:
            #
            #     pass
            #
            # else:

            # 找出所有 能解决当前类别任务&&并发低于3 的专家
            cur_experts = availableExperts(t.category)

            # 无可用专家
            if len(cur_experts) == 0 :

                if t.category in [1,2,3] or t.response_time <= 1:
                    #对响应时间最低的处理
                    green_experts = [i for i in experts if t.category in i.able.keys()]  # 所有此任务满负荷的专家
                    green_experts.sort(key=lambda x: x.able[t.category], reverse=False)

                    stop = False
                    for e in green_experts:
                        for c in e.conc:
                            # 当前专家此任务转发为5 || 此任务为当前t同类型任务（加快效率）
                            if c.redirect == 5 or c.category == t.category or e.proficiency(t.category) < 0.6:
                                continue

                            # 当前类型任务是否可以安排别人先做，空出位置
                            other = [i for i in experts if
                                     c.category in i.able.keys() and len(i.conc) < 3]
                            other.sort(key=lambda x: x.able[c.category])

                            # 考虑将满负荷专家中 不擅长&&有人可做&&刚开始执行 的任务踢出让位
                            if len(other) != 0 and t.end - time > other[0].able[c.category] and c.start == time:
                                hover_task.remove(t)
                                e.conc.remove(c)

                                c.start = time
                                c.end = time + other[0].able[c.category]
                                c.redirect += 1
                                other[0].conc.append(c)

                                t.start = time
                                t.end = time + e.able[t.category]
                                t.redirect += 1
                                e.conc.append(t)

                                stop = True
                                break

                        if stop: break

                t.response_time -= 1


            else:
                hover_task.remove(t)

                # 找出当前专家中熟练度最高来解决问题
                cur_experts.sort(key=lambda x: x.able[t.category], reverse=False)

                t.start = time
                t.end = time + cur_experts[0].able[t.category]
                t.redirect += 1

                cur_experts[0].conc.append(t)  # 专家并发+1


        time += 1

        print("time:" + str(time) + "    hover_task:" + str(hover_task.__len__()))
        expertsStatus(experts)
        print("")

    fillRes(res)
