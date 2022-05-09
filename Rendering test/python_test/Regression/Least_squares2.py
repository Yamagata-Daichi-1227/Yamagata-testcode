#matplotlib inline
 
import matplotlib.pyplot as plt
import numpy as np
 
x = np.array([58, 70, 81, 84, 132, 230, 262, 289, 295, 321])
y = np.array([374, 385, 375, 401, 439, 578, 616, 640, 689, 799])
 
# 一次関数
def func01(x):
    return a * x + b
 
# グラフ描画
def func_plot():
    z = func01(x)
 
    plt.scatter(x, y)
    plt.plot(x, z, color='red')
 
    plt.xlabel('CPC')
    plt.ylabel('Click')
    plt.xlim(0, 400)
    plt.ylim(0, 900)
    plt.grid()
    plt.show()
# aとbのパラメータを仮に1、2としてみる
a = ((x * y).mean() - (x.mean() * y.mean())) / ((x ** 2).mean() - x.mean() ** 2)
b = -(a * x.mean()) + y.mean()
 
func_plot()
