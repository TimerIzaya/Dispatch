class Task:
    id = -1

    create_time = -1  #创建时间 （默认初始化）

    start = -1  #开始处理时间

    end = -1  #处理完毕时间

    category = -1 #任务种类 （默认初始化）

    response_time = -1  #剩余响应时间 （默认初始化）

    redirect = 0  #被转发次数

    def print(self):
        print("id:" + str(self.id) +
              "  create_time:" + str(self.create_time) +
              "  category:" + str(self.category) +
              "  start:" + str(self.start) +
              "  end:" + str(self.end) +
              "  response_time:" + str(self.response_time) +
              "  redirect:" + str(self.redirect))
