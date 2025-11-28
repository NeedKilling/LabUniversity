yy = 0.5
u = 1
v = 2
b = 1.5

# import numpy as np
# import matplotlib.pyplot as plt

# x = np.array([u+v, u+v+2, u+v+4, u+v+6, u+v+8])
# y = np.array([yy+2.5, yy+4.9, yy+8.0, yy+12.1, yy+16.9])

# # 1. Аппроксимация параболой МНК
# A_par = np.column_stack([np.ones_like(x), x, x**2])
# c0, c1, c2 = np.linalg.lstsq(A_par, y, rcond=None)[0]
# y_par = c0 + c1*x + c2*x**2
# ss_par = np.sum((y - y_par)**2)

# print(f"Парабола: y = {c0:.5f} + {c1:.5f}x + {c2:.5f}x²")
# print(f"par = {ss_par:.6f}")

# # 2. Аппроксимация экспоненты МНК
# Y = np.log(y)
# A_exp = np.column_stack([np.ones_like(x), x])
# ln_a, ln_b = np.linalg.lstsq(A_exp, Y, rcond=None)[0]

# a = np.exp(ln_a)
# b = np.exp(ln_b)
# y_exp = a * b**x
# ss_exp = np.sum((y - y_exp)**2)

# print(f"Экспонента: y = {a:.5f} · {b:.5f}ˣ")
# print(f"exp = {ss_exp:.6f}")

# # 3. Построение графиков
# xx = np.linspace(min(x)-1, max(x)+1, 100)
# yy_par = c0 + c1*xx + c2*xx**2
# yy_exp = a * b**xx

# plt.figure(figsize=(10, 6))
# plt.plot(x, y, 'ko', markersize=8, label='Исходные данные')
# plt.plot(xx, yy_par, 'b-', linewidth=2, label=f'Парабола: y = {c0:.3f} + {c1:.3f}x + {c2:.3f}x²')
# plt.plot(xx, yy_exp, 'r--', linewidth=2, label=f'Экспонента: y = {a:.3f}·{b:.3f}ˣ')
# plt.legend(fontsize=12)
# plt.grid(True, alpha=0.3)
# plt.xlabel('x', fontsize=12)
# plt.ylabel('y', fontsize=12)
# plt.title('Сравнение аппроксимаций: парабола vs экспонента', fontsize=14)
# plt.show()

# print("\nСравнение сумм квадратов отклонений:")
# print(f"Парабола:  {ss_par:.6f}")
# print(f"Экспонента: {ss_exp:.6f}")
# if ss_par < ss_exp:
#     print("Параболическая аппроксимация точнее")
# else:
#     print("Экспоненциальная аппроксимация точнее")








# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit, leastsq

# x = np.array([u+v, u+v+2, u+v+4, u+v+6])
# y = np.array([yy+2.5, yy+4.9, yy+8.0, yy+12.1])

# # 1. Решение с помощью curve_fit()
# def power_func(x, a, b):
#     return a * x**b

# p0 = [1, 1]
# popt, pcov = curve_fit(power_func, x, y, p0=p0)
# a_curve, b_curve = popt

# y_curve = power_func(x, a_curve, b_curve)
# ss_curve = np.sum((y - y_curve)**2)

# print(f"\n1. Решение с помощью curve_fit():")
# print(f"y = {a_curve:.5f} * x^({b_curve:.5f})")
# print(f"Сумма квадратов отклонений: {ss_curve:.6f}")

# # 2. Решение с помощью leastsq()
# def residuals(params, x, y):
#     a, b = params
#     return y - a * x**b

# p0_leastsq = [1, 1]
# result_leastsq = leastsq(residuals, p0_leastsq, args=(x, y), full_output=True)
# popt_leastsq = result_leastsq[0]
# a_leastsq, b_leastsq = popt_leastsq

# y_leastsq = power_func(x, a_leastsq, b_leastsq)
# ss_leastsq = np.sum((y - y_leastsq)**2)

# print(f"\n2. Решение с помощью optimize.leastsq():")
# print(f"y = {a_leastsq:.5f} * x^({b_leastsq:.5f})")
# print(f"Сумма квадратов отклонений: {ss_leastsq:.6f}")

# # 3. Построение графиков
# xx = np.linspace(min(x)-1, max(x)+1, 100)  
# yy_curve = power_func(xx, a_curve, b_curve)
# yy_leastsq = power_func(xx, a_leastsq, b_leastsq)

# plt.figure(figsize=(10, 6))
# plt.plot(x, y, 'ko', markersize=8, label='Исходные данные')
# plt.plot(xx, yy_curve, 'b-', linewidth=2, label=f'curve_fit: y = {a_curve:.3f}·x^({b_curve:.3f})')
# plt.plot(xx, yy_leastsq, 'r--', linewidth=2, label=f'leastsq: y = {a_leastsq:.3f}·x^({b_leastsq:.3f})')
# plt.legend(fontsize=12)
# plt.grid(True, alpha=0.3)
# plt.xlabel('x', fontsize=12)
# plt.ylabel('y', fontsize=12)
# plt.title('Аппроксимация степенной функцией y = a·x^b', fontsize=14)
# plt.show()





import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

x = np.array([u+v, u+v+1, u+v+2, u+v+3, u+v+4])
y = np.array([yy+b, yy+b+1, yy+b+3, yy+b+4, yy+b+8])

# 1. Парабола y = c0 + c1*x + c2*x^2
def residuals_par(params, x, y):
    c0, c1, c2 = params
    return y - (c0 + c1*x + c2*x**2)

c0, c1, c2 = leastsq(residuals_par, [1, 1, 1], args=(x, y))[0]
K_par = np.sum(residuals_par([c0, c1, c2], x, y)**2)

# 2. Экспонента y = a*e^(b*x)
def residuals_exp(params, x, y):
    a, b = params
    return y - (a * np.exp(b * x))

a_exp, b_exp = leastsq(residuals_exp, [1, 0.1], args=(x, y))[0]
K_exp = np.sum(residuals_exp([a_exp, b_exp], x, y)**2)

# 3. Логарифмическая y = a + b*ln(x)
def residuals_log(params, x, y):
    a, b = params
    return y - (a + b * np.log(x))

a_log, b_log = leastsq(residuals_log, [1, 1], args=(x, y))[0]
K_log = np.sum(residuals_log([a_log, b_log], x, y)**2)

# Построение графиков
x_smooth = np.linspace(min(x)-0.5, max(x)+0.5, 100)
y_par = c0 + c1*x_smooth + c2*x_smooth**2
y_exp = a_exp * np.exp(b_exp * x_smooth)
y_log = a_log + b_log * np.log(x_smooth)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(x, y, 'ko', markersize=6, label='Данные')
plt.plot(x_smooth, y_par, 'r-', linewidth=2, label=f'K={K_par:.4f}')
plt.title('Параболическая аппроксимация')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)

equation_par = f'y = {c0:.3f} + {c1:.3f}·x + {c2:.3f}·x²\nK = {K_par:.4f}'
plt.text(0.05, 0.95, equation_par, transform=plt.gca().transAxes, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
         verticalalignment='top', fontsize=10)

plt.subplot(1, 3, 2)
plt.plot(x, y, 'ko', markersize=6, label='Данные')
plt.plot(x_smooth, y_exp, 'g-', linewidth=2, label=f'K={K_exp:.4f}')
plt.title('Экспоненциальная аппроксимация')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)

equation_exp = f'y = {a_exp:.3f}·e^({b_exp:.3f}·x)\nK = {K_exp:.4f}'
plt.text(0.05, 0.95, equation_exp, transform=plt.gca().transAxes, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
         verticalalignment='top', fontsize=10)

plt.subplot(1, 3, 3)
plt.plot(x, y, 'ko', markersize=6, label='Данные')
plt.plot(x_smooth, y_log, 'm-', linewidth=2, label=f'K={K_log:.4f}')
plt.title('Логарифмическая аппроксимация')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, alpha=0.3)

equation_log = f'y = {a_log:.3f} + {b_log:.3f}·ln(x)\nK = {K_log:.4f}'
plt.text(0.05, 0.95, equation_log, transform=plt.gca().transAxes, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
         verticalalignment='top', fontsize=10)

plt.tight_layout()
plt.show()
