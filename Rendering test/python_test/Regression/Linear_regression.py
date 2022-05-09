import numpy as np
import matplotlib.pyplot as plt

X = np.random.rand(20)*8-4 # -4~4の範囲での一様乱数
y = np.sin(X) + np.random.randn(20)*0.2 # サインカーブの値にノイズを加えた

XX = np.linspace(-4,4,100) # -4から4の間を100等分した数列を生成

plt.xlabel('X')
#Out[8]: <matplotlib.text.Text at 0x10f8714a8>

plt.ylabel('y')
#Out[9]: <matplotlib.text.Text at 0x10f87c390>

plt.title('training data')
#Out[10]: <matplotlib.text.Text at 0x10f894cc0>

plt.grid()

plt.scatter(X, y, marker='x', c ='red') # markerでポイントするものの形状を指定。cで色を指定。これが散布図になる。
#Out[12]: <matplotlib.collections.PathCollection at 0x10f8d4978>

plt.plot(XX, np.sin(XX)) # サインカーブをプロットする。  
#Out[13]: [<matplotlib.lines.Line2D at 0x10f8dd080>]

plt.show()

A = np.empty((6,6)) # 行列Aの受け皿を作る
for i in range(6):
    for j in range(6):
        A[i][j] = np.sum(X**(i+j)




b = np.empty(6)
for i in range(6):
　　 b[i] = np.sum(X**i*y)

omega = np.dot(np.linalg.inv(A), b.reshape(-1,1)) # linalg.inv()で逆行列を求める。dot関数で内積を求めてくれる。
omega.shape

f = np.poly1d(omega.flatten()[::-1]) # ωを係数とした多項式を作る

XX = np.linspace(-4,4,100)

plt.xlabel('X')
#Out[56]: <matplotlib.text.Text at 0x10bcd3208>

plt.ylabel('y')
#Out[57]: <matplotlib.text.Text at 0x10bcd5b70>

plt.title('trained data')
#Out[58]: <matplotlib.text.Text at 0x10bcf2a90>

plt.grid()

plt.plot(XX, f(XX), color='green')
#Out[60]: [<matplotlib.lines.Line2D at 0x10bd214e0>]

plt.plot(XX, np.sin(XX), color='blue')
#Out[61]: [<matplotlib.lines.Line2D at 0x10bcd50b8>]

plt.show()