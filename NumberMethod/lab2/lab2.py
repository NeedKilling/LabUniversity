
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, leastsq

# ЗАДАНИЕ 1 - Аппроксимация параболой и экспонентой
print("ЗАДАНИЕ 1")
print("=" * 50)

# Исходные данные (принимаем μ=0, v=0, γ=0, θ=0)
x1 = np.array([0, 2, 4, 6, 8])
y1 = np.array([2.5, 4.9, 8.0, 12.1, 16.9])

print("Исходные данные:")
for i in range(len(x1)):
    print(f"x = {x1[i]}, y = {y1[i]}")

# 1. Аппроксимация параболой y = c0 + c1*x + c2*x^2
A1 = x1[:, np.newaxis]**[0, 1, 2]
res1 = np.linalg.lstsq(A1, y1, rcond=None)

print("\nЗначения коэффициентов параболы:")
for i in range(3):
    print(f"c({i}) = {res1[0][i]:.7f}")

c0, c1, c2 = res1[0][0], res1[0][1], res1[0][2]
print(f"Уравнение параболы: y = {c0:.6f} + ({c1:.6f})*x + ({c2:.6f})*x^2")
print(f"Сумма квадратов отклонений: {res1[1][0]:.6f}")

# 2. Аппроксимация экспонентой y = a*b^x
def exp_func(x, a, b):
    return a * b**x

p0_exp = [2.5, 1.2]
popt_exp, pcov_exp = curve_fit(exp_func, x1, y1, p0=p0_exp)
a_exp, b_exp = popt_exp

y_exp = exp_func(x1, a_exp, b_exp)
ss_exp = np.sum((y1 - y_exp)**2)

print(f"\nУравнение экспоненты: y = {a_exp:.6f} * ({b_exp:.6f})^x")
print(f"Сумма квадратов отклонений: {ss_exp:.6f}")

# График для задания 1
x1_smooth = np.linspace(min(x1), max(x1), 100)
y1_par = c0 + c1*x1_smooth + c2*x1_smooth**2
y1_exp = exp_func(x1_smooth, a_exp, b_exp)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(x1, y1, 'bo', label="Исходные данные")
plt.plot(x1_smooth, y1_par, 'g-', label=f"Парабола: y = {c0:.3f} + {c1:.3f}x + {c2:.3f}x²")
plt.plot(x1_smooth, y1_exp, 'r--', label=f"Экспонента: y = {a_exp:.3f}·{b_exp:.3f}ˣ")
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('Задание 1: Аппроксимация параболой и экспонентой')
plt.xlabel('x')
plt.ylabel('y')

# ЗАДАНИЕ 2 - Аппроксимация степенной функцией
print("\n" + "=" * 50)
print("ЗАДАНИЕ 2")
print("=" * 50)

# Исходные данные (принимаем μ=0, v=0, γ=0, θ=0)
x2 = np.array([0, 2, 4, 6])
y2 = np.array([2.5, 4.9, 8.0, 12.1])

print("Исходные данные:")
for i in range(len(x2)):
    print(f"x = {x2[i]}, y = {y2[i]}")

# 1. Решение с помощью curve_fit()
def power_func(x, a, b):
    return a * x**b

p0_power = [1, 1]
popt_curve, pcov_curve = curve_fit(power_func, x2, y2, p0=p0_power)
a_curve, b_curve = popt_curve

y_curve = power_func(x2, a_curve, b_curve)
ss_curve = np.sum((y2 - y_curve)**2)

print(f"\nРешение с помощью curve_fit():")
print(f"y = {a_curve:.6f} * x^({b_curve:.6f})")
print(f"Сумма квадратов отклонений: {ss_curve:.6f}")

# 2. Решение с помощью leastsq()
def residuals(params, x, y):
    a, b = params
    return y - a * x**b

p0_leastsq = [1, 1]
result_leastsq = leastsq(residuals, p0_leastsq, args=(x2, y2), full_output=True)
popt_leastsq = result_leastsq[0]
a_leastsq, b_leastsq = popt_leastsq

y_leastsq = power_func(x2, a_leastsq, b_leastsq)
ss_leastsq = np.sum((y2 - y_leastsq)**2)

print(f"\nРешение с помощью leastsq():")
print(f"y = {a_leastsq:.6f} * x^({b_leastsq:.6f})")
print(f"Сумма квадратов отклонений: {ss_leastsq:.6f}")

# График для задания 2
x2_smooth = np.linspace(0.1, 6, 100)
y2_curve = power_func(x2_smooth, a_curve, b_curve)
y2_leastsq = power_func(x2_smooth, a_leastsq, b_leastsq)

plt.subplot(1, 2, 2)
plt.plot(x2, y2, 'bo', label="Исходные данные")
plt.plot(x2_smooth, y2_curve, 'g-', label=f"curve_fit: y = {a_curve:.3f}·x^({b_curve:.3f})")
plt.plot(x2_smooth, y2_leastsq, 'r--', label=f"leastsq: y = {a_leastsq:.3f}·x^({b_leastsq:.3f})")
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('Задание 2: Аппроксимация степенной функцией')
plt.xlabel('x')
plt.ylabel('y')

plt.tight_layout()
plt.show()

# Сравнение результатов
print("\n" + "=" * 50)
print("ИТОГИ")
print("=" * 50)
print("Задание 1:")
print(f"  Парабола:    SS = {res1[1][0]:.6f}")
print(f"  Экспонента:  SS = {ss_exp:.6f}")

print("\nЗадание 2:")
print(f"  curve_fit:   SS = {ss_curve:.6f}")
print(f"  leastsq:     SS = {ss_leastsq:.6f}")
