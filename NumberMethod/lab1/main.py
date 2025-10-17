

# v = 48 a = 8
# import matplotlib.pyplot as plt
# from sympy import *
# import scipy.optimize
# import numpy as np
# def f(x):
#  return (48+x)**3-2*x**2-8*x-17
# z = scipy.optimize.root(f, x0=3)
# print("Корень уравнения %.4f" % z.x[0])
# print("Значение функции в точке %.4f равно %.11f" % (z.x[0],z.fun[0]))
# print("Количество итераций %i" % z.nfev)


# x = np.linspace(-36, -34, 10)
# y = f(x)

# plt.title(r"$График \ функции \ y \ =(v+x)^3-2x^2-ax-17$",
#  fontsize=14)

# for cor in z.x:
#     plt.scatter(cor, 0, color='blue', s=100, zorder=5, label=f'Корень: x ≈ {cor:.4f}')
#     plt.annotate(f'x ≈ {cor:.4f}', 
#             xy=(cor, 0), 
#             xytext=(cor + 0.1, 0.5),
#             arrowprops=dict(arrowstyle='->', color='blue'),
#             fontsize=12,
#             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

# plt.xlabel("X",color='k',fontstyle="italic",
#  fontsize=18,fontfamily = 'serif') # ось абсцисс
# plt.ylabel("Y",color='k',fontstyle="italic",
#  fontsize=18,fontfamily = 'serif') # ось ординат
# plt.grid() # включение отображение сетки
# plt.plot(x, f(x),linewidth=3,c='red'); plt.show()


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////

# v = 48 a = 8 y = 20, ϑ = 13, μ = 5
# import matplotlib.pyplot as plt
# from sympy import *
# import scipy.optimize
# import numpy as np
# def f(x):
#  return 8*x**3 - (20+13)*x**2 - 5*x + 48
# z = scipy.optimize.fsolve(f, x0=[-1,0.5,4])

# print(f"корень уровнения:",z)
# # print("Корень уравнения %.4f" % z.x[0])
# # print("Значение функции в точке %.4f равно %.11f" % (z.x[0],z.fun[0]))
# # print("Количество итераций %i" % z.nfev)


# x = np.linspace(-2, 5, 100)
# y = f(x)

# plt.title(r"$График \ функции \ y \ =(v+x)^3-2x^2-ax-17$",
#  fontsize=14)

# for cor in z:
#     plt.scatter(cor, 0, color='blue', s=100, zorder=5, label=f'Корень: x ≈ {cor:.4f}')
#     plt.annotate(f'x ≈ {cor:.4f}', 
#             xy=(cor, 0), 
#             xytext=(cor + 0.1, 0.5),
#             arrowprops=dict(arrowstyle='->', color='blue'),
#             fontsize=12,
#             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

# plt.xlabel("X",color='k',fontstyle="italic",
#  fontsize=18,fontfamily = 'serif') # ось абсцисс
# plt.ylabel("Y",color='k',fontstyle="italic",
#  fontsize=18,fontfamily = 'serif') # ось ординат
# plt.grid() # включение отображение сетки

# plt.plot(x, f(x),linewidth=3,c='red'); plt.show()

#///////////////////////////////////////////////////////////////////////////////////////


# v = 48 a = 8 y = 2 u = 7 b = 22
# import matplotlib.pyplot as plt
# from sympy import *
# import scipy.optimize
# import numpy as np


# def f(value):
#     x1,x2,x3,x4 = value
#     y = 3*x1 + x2 + x3 + 2*x4 - 8
#     y2 = x1 - 7*x2 + 48*x3 + 4*x4 - 22
#     y3 = -5*x1 + 0 -x3 - 7*x4 + 5 
#     y4 = x1 - 6*x2 + 8*x3 + 6*x4 - 3
#     return [y,y2,y3,y4]

# z = scipy.optimize.fsolve(f, [0, 0, 0, 0])

# print(z)

#//////////////////////////////////////////////////////////////////////////////////////////

# v = 48 a = 8 b = 3 y = 17 u = 7
# import matplotlib.pyplot as plt
# from sympy import *
# import scipy.optimize
# import numpy as np


# def f(value):
#     x1,x2,x3,x4 = value
#     y = 3*x1 + 17*x2 + 48*x3 + x4 - 10*7 - 8    
#     y2 = x1 - 3*7*x2 + 2*x3 + 4*8*x4 - 9 - 17
#     y3 = -5*x1 + 48*x2 - 1*x3 - 7*x4 + 5
#     y4 = 48*x1 - 6*x2 + 2*x3 + 6*x4 - 7
#     return [y,y2,y3,y4]

# z = scipy.optimize.root(f, [0, 0, 0, 0],method='hybr')

# print(f"x1 = {z.x[0]:.6f}")
# print(f"x2 = {z.x[1]:.6f}")
# print(f"x3 = {z.x[2]:.6f}")
# print(f"x4 = {z.x[3]:.6f}")

# print(f"\nСтатус решения: {z.message}")
# print(f"Количество итераций: {z.nfev}")

#////////////////////////////////////////////////////////////////////////////////////////////////////////











import matplotlib.pyplot as plt
from sympy import *
import scipy.optimize
import numpy as np
import sympy as sp




# def g(z):   
#   x=z[0];y=z[1] 
#   f=np.zeros(2) 
#   f[0]=3*np.log(x) + y*np.sin(x) + y**2 - 12 
#   f[1]=x/(y**2+1)+2**x - 3*y**2 - 22 
#   return f 
# z = scipy.optimize.fsolve(g, [3.5, 1.5])
# print("Решение системы уравнений: x= %.6f y=%.6f" %  
#       (z[0],z[1])) 
# print("Значение левой части первого уравнения равно %.12f "  
#  % g(z)[0]) 
# 35 
# print("Значение левой части второго уравнения равно %.12f " 
#  % g(z)[1])
# x, y = symbols('x y') 
# p1 = plot_implicit(Eq(3*log(x) + y*sin(x) + y**2 ,12),  
#   (x, -1, 6),adaptive=False,show=False) 
# p2=plot_implicit(Eq(x/(y**2+1)+2**x - 3*y**2,22),  
#  (x, -1, 6),adaptive=False,show=False,line_color='red') 
# p3 = plot_implicit(Eq((x - z[0])**2 + (y - z[1])**2, 0.01),  
#                   (x, z[0]-0.3, z[0]+0.3), (y, z[1]-0.3, z[1]+0.3), 
#                   adaptive=False, show=False, line_color='black') 
# p1.append(p2[0])
# p1.append(p3[0])

# p1.title = f'Решение: x={z[0]:.3f}, y={z[1]:.3f}'
# p1.show()






# def g(z):   
#   x=z[0];y=z[1] 
#   f=np.zeros(2) 
#   f[0]=x**2 - y**3 + x/(np.sin(y)+2) + 2**x -15 
#   f[1]=x*np.cos(y)**2+np.exp(x-y) - y**2 - 17
#   return f 
# z = scipy.optimize.fsolve(g, [3, 2])
# print("Решение системы уравнений: x= %.6f y=%.6f" %  
#       (z[0],z[1])) 
# print("Значение левой части первого уравнения равно %.12f "  
#  % g(z)[0]) 
# 35 
# print("Значение левой части второго уравнения равно %.12f " 
#  % g(z)[1])

# x, y = symbols('x y') 
# p1 = plot_implicit(Eq(x**2 - y**3 + x/(sin(y)+2) + 2**x ,15),  
#   (x, 1, 4),adaptive=False,show=False) 
# p2=plot_implicit(Eq(x*cos(y)**2+exp(x-y) - y**2, 17),  
#  (x, 1, 4),adaptive=False,show=False,line_color='red') 
# p3 = plot_implicit(Eq((x - z[0])**2 + (y - z[1])**2, 0.01),  
#                   (x, z[0]-0.3, z[0]+0.3), (y, z[1]-0.3, z[1]+0.3), 
#                   adaptive=False, show=False, line_color='black') 
# p1.append(p2[0])
# p1.append(p3[0])

# p1.title = f'Решение: x={z[0]:.3f}, y={z[1]:.3f}'
# p1.show()

##########################################
# import matplotlib.pyplot as plt
# import scipy.optimize
# import numpy as np

# def g(z):   
#     x=z[0]; y=z[1] 
#     f=np.zeros(2) 
#     f[0]=x**2 - y**3 + x/(np.sin(y)+2) + 2**x -15 
#     f[1]=x*np.cos(y)**2 + np.exp(x-y) - y**2 - 17
#     return f 

# z = scipy.optimize.fsolve(g, [3, 2])
# print("Решение системы уравнений: x= %.6f y=%.6f" % (z[0], z[1])) 
# print("Значение левой части первого уравнения равно %.12f" % g(z)[0]) 
# print("Значение левой части второго уравнения равно %.12f" % g(z)[1])

# # Создаем сетку для построения графиков
# x_vals = np.linspace(-2, 4, 300)
# y_vals = np.linspace(-2, 3, 300)
# X, Y = np.meshgrid(x_vals, y_vals)

# # Вычисляем значения уравнений
# Z1 = X**2 - Y**3 + X/(np.sin(Y)+2) + 2**X - 15  # Первое уравнение
# Z2 = X*np.cos(Y)**2 + np.exp(X-Y) - Y**2 - 17   # Второе уравнение

# # Построение графика
# plt.figure(figsize=(10, 8))

# # Строим контурные линии для уравнений (уровень 0)
# contour1 = plt.contour(X, Y, Z1, levels=[0], colors='blue', linewidths=2)
# contour2 = plt.contour(X, Y, Z2, levels=[0], colors='red', linewidths=2)

# # Отмечаем найденное решение
# plt.plot(z[0], z[1], 'ko', markersize=10, label=f'Решение: ({z[0]:.3f}, {z[1]:.3f})')

# # Добавляем аннотацию к решению
# plt.annotate(f'({z[0]:.3f}, {z[1]:.3f})', 
#              xy=(z[0], z[1]), 
#              xytext=(z[0] + 0.2, z[1] + 0.3),
#              arrowprops=dict(arrowstyle='->', color='black'),
#              fontsize=12,
#              bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

# # Настройки графика
# plt.title('Графическое решение системы уравнений\n'
#           r'$x^2 - y^3 + \frac{x}{\sin y + 2} + 2^x = 15$' '\n'
#           r'$x \cos^2 y + e^{x-y} - y^2 = 17$', fontsize=12)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.grid(True, alpha=0.3)
# plt.legend()

# # Добавляем подписи для кривых
# plt.text(2.5, 2.5, 'Уравнение 1', color='blue', fontsize=10)
# plt.text(2.5, -1.5, 'Уравнение 2', color='red', fontsize=10)

# # Устанавливаем пределы осей
# plt.xlim(-2, 4)
# plt.ylim(-2, 3)

# plt.tight_layout()
# plt.show()
###############################



# def g(z):   
#   x=z[0];y=z[1] 
#   f=np.zeros(2) 
#   f[0]=x/(y**2+1)+2*x*cos(y)+exp(-x)+x*y - 38 
#   f[1]=3*x*y/(sin(x) + 2) + ln(Abs(y) + 6) - x**2 - 5
#   return f 
# z = scipy.optimize.fsolve(g, [4.5, -1.5])
# print("Решение системы уравнений: x= %.6f y=%.6f" %  
#       (z[0],z[1])) 
# print("Значение левой части первого уравнения равно %.12f "  
#  % g(z)[0]) 
# 35 
# print("Значение левой части второго уравнения равно %.12f " 
#  % g(z)[1])

# x, y = symbols('x y') 
# p1 = plot_implicit(Eq(x/(y**2+1)+2*x*cos(y)+exp(-x)+x*y,38),  
#   (x, -3, 10),(y, -1,10),adaptive=False,show=False) 
# p2=plot_implicit(Eq(3*x*y/(sin(x) + 2) + ln(Abs(y) + 6) - x**2, 5),  
#  (x, -3, 10),(y, -1,10),adaptive=False,show=False,line_color='red') 

# p3 = plot_implicit(Eq((x - z[0])**2 + (y - z[1])**2, 0.01),  
#                   (x, z[0]-0.3, z[0]+0.3), (y, z[1]-0.3, z[1]+0.3), 
#                   adaptive=False, show=False, line_color='black') 
# p1.append(p2[0])
# p1.append(p3[0])

# p1.title = f'Решение: x={z[0]:.3f}, y={z[1]:.3f}'
# p1.show()



# def g(z):   
#   x=z[0];y=z[1] 
#   f=np.zeros(2) 
#   f[0]=x**2+y**2 - 5*x*y - 3
#   f[1]=5*y/(x**2+1)+4*np.cos(x) - 6
#   return f 
# z = scipy.optimize.fsolve(g, [1, 2])
# print("Решение системы уравнений: x= %.6f y=%.6f" %  
#       (z[0],z[1])) 
# print("Значение левой части первого уравнения равно %.12f "  
#  % g(z)[0]) 

# print("Значение левой части второго уравнения равно %.12f " 
#  % g(z)[1])

# x, y = symbols('x y') 
# p1 = plot_implicit(Eq(x**2+y**2 - 5*x*y , 3),  
#   (x, -6, 6),adaptive=False,show=False) 
# p2=plot_implicit(Eq(5*y/(x**2+1)+4*cos(x), 6),  
#  (x, -6, 6),adaptive=False,show=False,line_color='red') 
# p3 = plot_implicit(Eq((x - z[0])**2 + (y - z[1])**2, 0.01),  
#                   (x, z[0]-0.3, z[0]+0.3), (y, z[1]-0.3, z[1]+0.3), 
#                   adaptive=False, show=False, line_color='black') 
# p1.append(p2[0])
# p1.append(p3[0])

# p1.title = f'Решение: x={z[0]:.3f}, y={z[1]:.3f}'
# p1.show()



#############################################################################
import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np

def g(z):   
    x=z[0]; y=z[1] 
    f=np.zeros(2) 
    f[0]=x**2 + y**2 - 5*x*y - 3
    f[1]=5*y/(x**2+1) + 4*np.cos(x) - 6
    return f 

z = scipy.optimize.fsolve(g, [1, 2])
print("Решение системы уравнений: x= %.6f y=%.6f" % (z[0], z[1])) 
print("Значение левой части первого уравнения равно %.12f" % g(z)[0]) 
print("Значение левой части второго уравнения равно %.12f" % g(z)[1])

# Создаем сетку для построения графиков
x_vals = np.linspace(-6, 6, 500)
y_vals = np.linspace(-6, 6, 500)
X, Y = np.meshgrid(x_vals, y_vals)

# Вычисляем значения уравнений
Z1 = X**2 + Y**2 - 5*X*Y - 3  # Первое уравнение
Z2 = 5*Y/(X**2+1) + 4*np.cos(X) - 6  # Второе уравнение

# Построение графика
plt.figure(figsize=(10, 8))

# Строим контурные линии для уравнений (уровень 0)
contour1 = plt.contour(X, Y, Z1, levels=[0], colors='blue', linewidths=2)
contour2 = plt.contour(X, Y, Z2, levels=[0], colors='red', linewidths=2)

# Отмечаем найденное решение
plt.plot(z[0], z[1], 'ko', markersize=10, label=f'Решение: ({z[0]:.3f}, {z[1]:.3f})')

# Добавляем аннотацию к решению
plt.annotate(f'({z[0]:.3f}, {z[1]:.3f})', 
             xy=(z[0], z[1]), 
             xytext=(z[0] + 0.5, z[1] + 0.5),
             arrowprops=dict(arrowstyle='->', color='black'),
             fontsize=12,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

# Настройки графика
plt.title('Графическое решение системы уравнений\n'
          r'$x^2 + y^2 - 5xy = 3$' '\n'
          r'$\frac{5y}{x^2 + 1} + 4\cos x = 6$', fontsize=12)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)
plt.legend()

# Добавляем подписи для кривых
plt.text(-4, 4, 'Уравнение 1', color='blue', fontsize=10)
plt.text(3, -4, 'Уравнение 2', color='red', fontsize=10)

# Добавляем линии осей
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)

# Устанавливаем пределы осей
plt.xlim(-6, 6)
plt.ylim(-6, 6)

plt.tight_layout()
plt.show()
#############################################################33

# def g(z):   
#   x=z[0];y=z[1] 
#   f=np.zeros(2) 
#   f[0]=x**2 * np.cos(y) - 5*x*y - 3
#   f[1]=5*y/(ln(x**2+1))+4*x - y - 6
#   return f 
# z = scipy.optimize.fsolve(g, [2, 1])
# print("Решение системы уравнений: x= %.6f y=%.6f" %  
#       (z[0],z[1])) 
# print("Значение левой части первого уравнения равно %.12f "  
#  % g(z)[0]) 

# print("Значение левой части второго уравнения равно %.12f " 
#  % g(z)[1])

# x, y = symbols('x y') 
# p1 = plot_implicit(Eq(x**2 * cos(y) - 5*x*y , 3),  
#   (x, -3, 6),adaptive=False,show=False) 
# p2=plot_implicit(Eq(5*y/(ln(x**2+1))+4*x - y, 6),  
#  (x, -3, 6),adaptive=False,show=False,line_color='red') 

# p3 = plot_implicit(Eq((x - z[0])**2 + (y - z[1])**2, 0.01),  
#                   (x, z[0]-0.3, z[0]+0.3), (y, z[1]-0.3, z[1]+0.3), 
#                   adaptive=False, show=False, line_color='black') 
# p1.append(p2[0])
# p1.append(p3[0])

# p1.title = f'Решение: x={z[0]:.3f}, y={z[1]:.3f}'
# p1.show()





# def g(z):   
#   x=z[0];y=z[1] 
#   f=np.zeros(2) 
#   f[0]= np.sqrt(x) * np.cos(y) - 5*x*y - 3
#   f[1]= 5*y/(x**2+y**2+1) + x - y - 4
#   return f 
# z = scipy.optimize.fsolve(g, [1, 1])

# print("Решение системы уравнений: x= %.6f y=%.6f" %  
#       (z[0],z[1])) 
# print("Значение левой части первого уравнения равно %.12f "  
#  % g(z)[0]) 

# print("Значение левой части второго уравнения равно %.12f " 
#  % g(z)[1])

# x, y = symbols('x y') 
# p1 = plot_implicit(Eq(sqrt(x) * cos(y) - 5*x*y , 3),  
#   (x, -0.1, 6),adaptive=False,show=False) 
# p2=plot_implicit(Eq(5*y/(x**2+y**2+1) + x - y, 4),  
#  (x, -0.1, 6),adaptive=False,show=False,line_color='red') 

# p3 = plot_implicit(Eq((x - z[0])**2 + (y - z[1])**2, 0.01),  
#                   (x, z[0]-0.3, z[0]+0.3), (y, z[1]-0.3, z[1]+0.3), 
#                   adaptive=False, show=False, line_color='black') 

# p1.append(p2[0])
# p1.append(p3[0])

# p1.title = f'Решение: x={z[0]:.3f}, y={z[1]:.3f}'
# p1.show()













