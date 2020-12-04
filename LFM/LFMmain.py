import numpy
import Rdata


R = numpy.array(Rdata.R0)

K = 10
max_iter = 5000
alpha = 0.0002
lamda = 0.004


# 核心算法
def LFM(R, K, max_iter, alpha=0.0002, lamda=0.002):
    # 基本维度参数定义
    num_of_user = len(R)
    num_of_movie = len(R[0])

    # P、Q初始值，随机生成
    P = numpy.random.rand(num_of_user, K)
    Q = numpy.random.rand(num_of_movie, K)
    Q = Q.T

    # 开始迭代
    for ino in range(10000):
        # 对所有的用户u、物品i做遍历，对应的特征向量Pu，Qi梯度下降
        for i in range(num_of_user):
            for j in range(num_of_movie):
                # 对于每一个大于0的评分，求出预测的评分误差
                if R[i][j] > 0:
                    eui = numpy.dot(P[i, :], Q[:, j]) - R[i][j]

                    # 带入公式，按照梯度下降算法更新当前的Pu与Qi
                    for k in range(K):
                        P[i][k] = P[i][k] - alpha * (2 * eui * Q[k][j] + 2 * lamda * P[i][k])
                        Q[k][j] = Q[k][j] - alpha * (2 * eui * P[i][k] + 2 * lamda * Q[k][j])

        # u、i遍历完成，所有的特征向量更新完成，可以得到P、Q，可以计算预测评分矩阵

        # 计算当前损失函数
        C = 0
        for i in range(num_of_user):
            for j in range(num_of_movie):
                if R[i][j] > 0:
                    C += (numpy.dot(P[i, :], Q[:, j]) - R[i][j]) ** 2
                    for k in range(K):
                        C += lamda * (P[i][k] ** 2 + Q[k][j] ** 2)
        if C < 0.01:
            break

    return P, Q, C

P,Q,cost = LFM(R,K,max_iter,alpha,lamda)
predR = P.dot(Q)
#预测矩阵
with open("output.txt", 'w') as f:
    for t in predR:
        f.write(str(t))
        f.write(",\n")
