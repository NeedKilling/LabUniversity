import numpy as np 
import matplotlib.pyplot as plt 
import scipy.optimize 
from scipy.optimize import * 
x=np.linspace(0,6,13); 
y=np.array([5.02, 6.08, 3.33, -0.93, -0.22, 7.83, 16.52, 15.55, 2.67, -11.42, -11.78, 5.09, 25.25]) 
def f(x, a, b, c):  
    return  a*x*np.cos(b*x)+c; 
args,_  = curve_fit(f, x, y)  
a, b, c = args[0], args[1], args[2] 
print("Коэффициенты кривой:") 
print("a= %.6f" % a) 
print("b= %.6f" % b) 
print("c= %.6f" % c) 
print("Уравнение кривой Y=%.6f*x*cos(%.6fx)+%.6f" % (a,b,c)) 
v=np.sum((f(x, a, b, c)-y)**2) 
print("Сумма площадей квадратов отклонений равна  %.6f" % v) 
plt.plot(x, y, 'bo', label="Исходные\nданные")  
plt.plot(x, f(x, a, b, c), label="Аппроксимирующая\nкривая")  
plt.legend() 
plt.show()