import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')

# Загрузка данных
df = pd.read_csv('filtered_sbdb_data.csv')

# Преобразование типов данных
df['pdes'] = df['pdes'].astype(str)
df['diameter'] = pd.to_numeric(df['diameter'], errors='coerce')

# Создание категорий по диаметру
df['diameter_category'] = pd.cut(df['diameter'], 
                                bins=[0, 2, 20, np.inf],
                                labels=['<2 км', '2-20 км', '>20 км'],
                                right=False)

# Определение родительского тела и указанных астероидов

parent_body_id = '24'  # Themis
specified_asteroids = ['62', '90', '222', '461','515','938']  # Пример, замените на указанные преподавателем

df['special'] = 'Обычный'
df.loc[df['pdes'] == parent_body_id, 'special'] = 'Родительское тело'
df.loc[df['pdes'].isin(specified_asteroids), 'special'] = 'Указанный астероид'

# Цветовая схема
colors = {'<2 км': 'lightblue', '2-20 км': 'lightgreen', '>20 км': 'salmon'}
special_colors = {'Обычный': 'gray', 'Родительское тело': 'red', 'Указанный астероид': 'blue'}

# 1. Построение гистограмм для всех параметров
parameters = ['spec_B', 'spec_T', 'a', 'e', 'i', 'q', 'H', 'rot_per']
fig, axes = plt.subplots(4, 2, figsize=(15, 20))
axes = axes.flatten()

for i, param in enumerate(parameters):
    if param in df.columns and not df[param].isna().all():
        # Фильтруем NaN значения
        data = df[param].dropna()
        
        if len(data) > 0:
            axes[i].hist(data, bins=20, alpha=0.7, edgecolor='black')
            axes[i].set_xlabel(param)
            axes[i].set_ylabel('Частота')
            axes[i].set_title(f'Распределение {param}')
            axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('Гистограммы параметров для всего семейства Themis', fontsize=16, y=1.02)
plt.show()

# 2. Гистограммы по категориям диаметра
fig, axes = plt.subplots(4, 2, figsize=(15, 20))
axes = axes.flatten()

for i, param in enumerate(parameters):
    if param in df.columns:
        for category, color in colors.items():
            category_data = df[df['diameter_category'] == category][param].dropna()
            if len(category_data) > 0:
                axes[i].hist(category_data, bins=15, alpha=0.7, 
                           label=category, color=color, edgecolor='black')
        
        axes[i].set_xlabel(param)
        axes[i].set_ylabel('Частота')
        axes[i].set_title(f'Распределение {param} по категориям диаметра')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('Распределение параметров по категориям диаметра', fontsize=16, y=1.02)
plt.show()

# 3. Поиск резонансов с Юпитером
# Орбитальный период Юпитера ~11.86 лет -> большая полуось ~5.2 а.е.
jupiter_a = 5.2

# Основные резонансы с Юпитером (отношение периодов)
resonances = {
    '1:1': 1.0,
    '2:1': 2.0,
    '3:1': 3.0,
    '3:2': 3/2,
    '4:1': 4.0,
    '4:3': 4/3,
    '5:2': 5/2,
    '5:3': 5/3
}

# Вычисление резонансных больших полуосей
resonance_positions = {}
for name, ratio in resonances.items():
    resonance_a = jupiter_a / (ratio**(2/3))
    resonance_positions[name] = resonance_a

# Визуализация резонансов
plt.figure(figsize=(12, 6))
a_data = df['a'].dropna()

# Гистограмма большой полуоси
plt.hist(a_data, bins=30, alpha=0.7, edgecolor='black')
plt.xlabel('Большая полуось (а.е.)')
plt.ylabel('Частота')
plt.title('Распределение большой полуоси с резонансами Юпитера')

# Добавление линий резонансов
for name, position in resonance_positions.items():
    if position >= a_data.min() and position <= a_data.max():
        plt.axvline(x=position, color='red', linestyle='--', alpha=0.7)
        plt.text(position, plt.ylim()[1]*0.9, f'{name}\n{position:.2f}', 
                ha='center', va='top', fontsize=8)

plt.grid(True, alpha=0.3)
plt.show()









# 4. Сравнение с первыми 500 астероидами
# Загрузка данных первых 500 астероидов (предполагаем, что они есть в sbdb)

first_500 = pd.read_csv('sbdb_query_results.csv')
first_500 = first_500.head(500)  # Берем первые 500

# Создаем объединенный DataFrame для сравнения
comparison_params = ['a', 'e', 'i', 'albedo']

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()

for i, param in enumerate(comparison_params):
    if param in df.columns and param in first_500.columns:
        # Данные семейства
        family_data = df[param].dropna()
        
        # Данные первых 500 астероидов
        first_500_data = first_500[param].dropna().head(len(family_data))  # Берем столько же
        
        if len(family_data) > 0 and len(first_500_data) > 0:
            # Используем логарифмическую шкалу если семейство большое
            log_scale = len(family_data) >= 500
            
            axes[i].hist(family_data, bins=20, alpha=0.7, label='Семейство Themis', 
                       color='blue', edgecolor='black', log=log_scale)
            axes[i].hist(first_500_data, bins=20, alpha=0.7, label='Первые 500 астероидов', 
                       color='orange', edgecolor='black', log=log_scale)
            
            axes[i].set_xlabel(param)
            axes[i].set_ylabel('Частота' + (' (лог)' if log_scale else ''))
            axes[i].set_title(f'Сравнение {param}')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('Сравнение семейства Themis с первыми 500 астероидами', fontsize=16, y=1.02)
plt.show()

# 5. Дополнительные визуализации с выделением особых астероидов
# Scatter plot с выделением особых астероидов
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# a vs e
scatter1 = axes[0, 0].scatter(df['a'], df['e'], c=df['special'].map(special_colors), 
                            alpha=0.7, s=30)
axes[0, 0].set_xlabel('Большая полуось (a)')
axes[0, 0].set_ylabel('Эксцентриситет (e)')
axes[0, 0].set_title('a vs e с выделением особых астероидов')

# i vs albedo
if 'albedo' in df.columns:
    scatter2 = axes[0, 1].scatter(df['i'], df['albedo'], c=df['special'].map(special_colors), 
                                alpha=0.7, s=30)
    axes[0, 1].set_xlabel('Наклонение (i)')
    axes[0, 1].set_ylabel('Альбедо')
    axes[0, 1].set_title('i vs albedo')

# H vs diameter
scatter3 = axes[1, 0].scatter(df['H'], df['diameter'], c=df['special'].map(special_colors), 
                            alpha=0.7, s=30)
axes[1, 0].set_xlabel('Абсолютная магнитуда (H)')
axes[1, 0].set_ylabel('Диаметр')
axes[1, 0].set_title('H vs diameter')

# Создаем легенду для особых астероидов
legend_elements = [Patch(facecolor=color, label=label) 
                  for label, color in special_colors.items()]
axes[1, 1].legend(handles=legend_elements, loc='center')
axes[1, 1].axis('off')
axes[1, 1].set_title('Легенда')

plt.tight_layout()
plt.show()

# 6. Статистика по резонансам
print("Анализ резонансов с Юпитером:")
print("=" * 50)

for name, position in resonance_positions.items():
    if position >= df['a'].min() and position <= df['a'].max():
        # Астероиды вблизи резонанса (±0.1 а.е.)
        near_resonance = df[(df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)]
        print(f"Резонанс {name} ({position:.3f} а.е.): {len(near_resonance)} астероидов")
        
        if len(near_resonance) > 0:
            print(f"  ID астероидов: {', '.join(near_resonance['pdes'].astype(str).tolist())}")

# 7. Сохранение результатов анализа
# Добавляем информацию о резонансах
df['resonance'] = 'Нет'
for name, position in resonance_positions.items():
    mask = (df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)
    df.loc[mask, 'resonance'] = name

# Сохраняем обогащенные данные
df.to_csv('themis_family_analysis.csv', index=False)
print(f"\nРезультаты анализа сохранены в themis_family_analysis.csv")

# Вывод основной статистики
print(f"\nОбщая статистика семейства Themis:")
print(f"Всего астероидов: {len(df)}")
print(f"С диаметром >20 км: {len(df[df['diameter_category'] == '>20 км'])}")
print(f"С диаметром 2-20 км: {len(df[df['diameter_category'] == '2-20 км'])}")
print(f"С диаметром <2 км: {len(df[df['diameter_category'] == '<2 км'])}")
print(f"Астероидов в резонансе: {len(df[df['resonance'] != 'Нет'])}")