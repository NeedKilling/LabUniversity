import numpy as np
o = 8
u = 1
v = 2
# x = np.array([-1.0, 1.0, 3.0, u+4.0])
# y = np.array([8.0, 6.0+o, 6.0, v])

# A = np.zeros((4, 4))
# for i in range(4):
#     A[i] = [x[i]**3, x[i]**2, x[i], 1]

# coeffs = np.linalg.solve(A, y)
# a, b, c, d = coeffs

# print("Коэффициенты полинома:")
# print(f"a = {a:.6f}, b = {b:.6f}, c = {c:.6f}, d = {d:.6f}")
# print()

# x_star1 = -2.0
# x_star2 = 0.5

# P_x_star1 = a*x_star1**3 + b*x_star1**2 + c*x_star1 + d
# P_x_star2 = a*x_star2**3 + b*x_star2**2 + c*x_star2 + d

# print(f"P({x_star1}) = {P_x_star1}")
# print(f"P({x_star2}) = {P_x_star2}")
# print()


# import numpy as np
# import math

# u = 1
# v = 8

# x_data = np.array([2.0, 3.0, v + 5])  
# y_data = np.array([4.0, u, 24.0])    

# print("Данные:")
# for i in range(3):
#     print(f"x={x_data[i]}, y={y_data[i]}")
# print()

# A = np.zeros((3, 3))
# for i in range(3):
#     x = x_data[i]
#     A[i, 0] = math.log(x)          
#     A[i, 1] = x * math.exp(-0.5 * x)  
#     A[i, 2] = x**2                   

# coeffs = np.linalg.solve(A, y_data)
# c1, c2, c3 = coeffs

# print("Найденные коэффициенты:")
# print(f"c1 = {c1:.8f}")
# print(f"c2 = {c2:.8f}")
# print(f"c3 = {c3:.8f}")
# print()





















# import numpy as np
# import matplotlib.pyplot as plt

# # Данные из предыдущих заданий
# x_data = np.array([1.0, 2+u/(v+1), 6.0,7.0])
# y_data = np.array([-1.0, 6.0, 18.0, u]) 

# x_star1 = 3.4
# x_star2 = 4.4

# def quadratic_interpolation(x, x_points, y_points):
#     distances = np.abs(x_points - x)
#     idx = np.argsort(distances)[:3]
#     x_vals = x_points[idx]
#     y_vals = y_points[idx]
#     A = np.vstack([x_vals**2, x_vals, np.ones_like(x_vals)]).T
#     coeffs = np.linalg.solve(A, y_vals)
    
#     return coeffs[0]*x**2 + coeffs[1]*x + coeffs[2]

# def cubic_interpolation(x, x_points, y_points):
#     distances = np.abs(x_points - x)
#     idx = np.argsort(distances)[:4]
#     x_vals = x_points[idx]
#     y_vals = y_points[idx]
    
#     A = np.vstack([x_vals**3, x_vals**2, x_vals, np.ones_like(x_vals)]).T
#     coeffs = np.linalg.solve(A, y_vals)
    
#     return coeffs[0]*x**3 + coeffs[1]*x**2 + coeffs[2]*x + coeffs[3]

# y_quad_1 = quadratic_interpolation(x_star1, x_data, y_data)
# y_quad_2 = quadratic_interpolation(x_star2, x_data, y_data)

# y_cubic_1 = cubic_interpolation(x_star1, x_data, y_data)
# y_cubic_2 = cubic_interpolation(x_star2, x_data, y_data)

# print("Результаты интерполяции:")
# print(f"Для x* = {x_star1}:")
# print(f"  Квадратичная интерполяция: y = {y_quad_1:.6f}")
# print(f"  Кубическая интерполяция:   y = {y_cubic_1:.6f}")
# print()

# print(f"Для x* = {x_star2}:")
# print(f"  Квадратичная интерполяция: y = {y_quad_2:.6f}")
# print(f"  Кубическая интерполяция:   y = {y_cubic_2:.6f}")
# print()

# def create_smooth_curve(method, x_range, x_points, y_points, degree):
#     if method == 'quadratic':
#         coeffs = np.polyfit(x_points, y_points, 2)
#         poly = np.poly1d(coeffs)
#         return poly(x_range)
#     else: 
#         coeffs = np.polyfit(x_points, y_points, 3)
#         poly = np.poly1d(coeffs)
#         return poly(x_range)

# x_min, x_max = min(x_data) - 1, max(x_data) + 1
# x_smooth = np.linspace(x_min, x_max, 400)

# y_quad_smooth = create_smooth_curve('quadratic', x_smooth, x_data, y_data, 2)
# y_cubic_smooth = create_smooth_curve('cubic', x_smooth, x_data, y_data, 3)

# plt.figure(figsize=(12, 8))

# # Основной график
# plt.subplot(2, 1, 1)
# plt.plot(x_data, y_data, 'ko', markersize=8, label='Исходные точки')
# plt.plot(x_smooth, y_quad_smooth, 'b-', linewidth=2, alpha=0.7, label='Квадратичная аппроксимация')
# plt.plot(x_smooth, y_cubic_smooth, 'r-', linewidth=2, alpha=0.7, label='Кубическая аппроксимация')

# # Точки интерполяции
# plt.plot(x_star1, y_quad_1, 'bo', markersize=10, label=f'Квадр. x*={x_star1}')
# plt.plot(x_star1, y_cubic_1, 'ro', markersize=10, label=f'Куб. x*={x_star1}')
# plt.plot(x_star2, y_quad_2, 'bo', markersize=10)
# plt.plot(x_star2, y_cubic_2, 'ro', markersize=10)

# plt.grid(True, alpha=0.3)
# plt.xlabel('x', fontsize=12)
# plt.ylabel('y', fontsize=12)
# plt.title('Интерполяция функции', fontsize=14)
# plt.legend(loc='best')
# plt.axhline(y=0, color='k', linewidth=0.5)
# plt.axvline(x=0, color='k', linewidth=0.5)

