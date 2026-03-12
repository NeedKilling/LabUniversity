import numpy as np
from scipy import integrate

y = 8
u = 1
v = 2

a = v + 0.1 * u  # 2.1
b = 5 + 1.3 * v  # 7.6

def f(x):
    return np.sqrt(x**2 + v + y) 

L = b - a  # 5.5
n = 10
h = L / n  # 0.55
print("ЗАДАНИЕ 1 (часть б)")

# 1. Обобщенная формула трапеций
x_trap = np.linspace(a, b, n + 1)
y_trap = f(x_trap)
integral_trap = h * (0.5 * y_trap[0] + 0.5 * y_trap[-1] + np.sum(y_trap[1:-1]))

# 2. Обобщенная формула Симпсона
integral_simp = 0
if n % 2 == 0:
    coeff = np.ones(n + 1)
    coeff[1:-1:2] = 4  
    coeff[2:-2:2] = 2  
    integral_simp = h / 3 * np.sum(coeff * y_trap)

integral_scipy, error = integrate.quad(f, a, b)

print(f"\tМетод трапеций: {integral_trap:.10f}")
print(f"\tМетод Симпсона: {integral_simp:.10f}")
print(f"\tSciPy (quad):   {integral_scipy:.10f}")

# Задание 2: 
print("ЗАДАНИЕ 2")

# 1. Метод левых прямоугольников
x_left = np.linspace(a, b - h, n)
y_left = f(x_left)
integral_left_rect = h * np.sum(y_left)

# 2. Метод правых прямоугольников
x_right = np.linspace(a + h, b, n)
y_right = f(x_right)
integral_right_rect = h * np.sum(y_right)

# 3. Метод средних прямоугольников
x_mid = np.linspace(a + h/2, b - h/2, n)
y_mid = f(x_mid)
integral_mid_rect = h * np.sum(y_mid)

print(f"\tЛевых прямоугольников:  {integral_left_rect:.10f}")
print(f"\tПравых прямоугольников: {integral_right_rect:.10f}")
print(f"\tСредних прямоугольников: {integral_mid_rect:.10f}")
print(f"\tМетод трапеций:         {integral_trap:.10f}")
print(f"\tМетод Симпсона:         {integral_simp:.10f}")
print(f"\tТочное значение (SciPy): {integral_scipy:.10f}")