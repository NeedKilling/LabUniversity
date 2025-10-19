import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')

# Установка стиля 
plt.style.use('default')
sns.set_style("whitegrid")

# Загрузка данных
df = pd.read_csv('filtered_sbdb_data.csv')

df['pdes'] = df['pdes'].astype(str)
df['diameter'] = pd.to_numeric(df['diameter'], errors='coerce')

df['diameter_category'] = pd.cut(df['diameter'], 
                                bins=[0, 2, 20, np.inf],
                                labels=['<2 км', '2-20 км', '>20 км'],
                                right=False)

# Определение родительского тела и указанных астероидов
parent_body_id = '24'  # Themis
specified_asteroids = ['62', '90', '222', '461','515','938'] 

df['special'] = 'Обычный'
df.loc[df['pdes'] == parent_body_id, 'special'] = 'Родительское тело'
df.loc[df['pdes'].isin(specified_asteroids), 'special'] = 'Указанный астероид'

special_colors = {'Обычный': 'lightgray', 'Родительское тело': 'red', 'Указанный астероид': 'blue'}

# 1. Гистограммы для всех параметров с выделением особых астероидов
parameters = ['spec_B', 'spec_T', 'a', 'e', 'i', 'q', 'H', 'rot_per']
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()

for i, param in enumerate(parameters):
    if param in df.columns:
       
        total_count = len(df)
        available_count = df[param].notna().sum()
        missing_count = total_count - available_count
        missing_percent = (missing_count / total_count) * 100
        
        if available_count > 0:
            data = df[param].dropna()
            axes[i].hist(data, bins=20, alpha=0.5, edgecolor='black', 
                        color='purple', linewidth=0.5, label=f'Все астероиды ({available_count}/{total_count})')
            
            parent_data = df[df['special'] == 'Родительское тело'][param].dropna()
            if len(parent_data) > 0:
                axes[i].axvline(x=parent_data.iloc[0], color='red', linestyle='-', 
                              linewidth=3, alpha=0.4, label='Родительское тело')
            
            specified_data = df[df['special'] == 'Указанный астероид'][param].dropna()
            for j, value in enumerate(specified_data):
                axes[i].axvline(x=value, color='blue', linestyle='--', 
                              linewidth=2, alpha=0.4, label='Указанный астероид' if j == 0 else "")
            
            axes[i].set_xlabel("", fontsize=10)
            axes[i].set_ylabel('Частота', fontsize=10)
            axes[i].set_title(f'Распределение {param} (пропуски: {missing_percent:.1f}%)', fontsize=8)
            axes[i].grid(True, alpha=0.3)
            
            if len(parent_data) > 0 or len(specified_data) > 0:
                axes[i].legend(fontsize=8)
            else:
                axes[i].legend(fontsize=8) 
        else:
            axes[i].text(0.5, 0.5, f'Нет данных\nдля {param}\n(100% пропусков)', 
                        ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
            axes[i].set_title(f'Распределение {param}', fontsize=11)
            axes[i].set_xlabel("", fontsize=10)
            axes[i].set_ylabel('Частота', fontsize=10)
# Убираем пустые subplots
for i in range(len(parameters), len(axes)):
    axes[i].set_visible(False)
plt.tight_layout()
plt.suptitle('Гистограммы параметров для всего семейства Themis', fontsize=14, y=1.02)
plt.show()

# 2
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()

colors = {'<2 км': 'lightblue', '2-20 км': 'lightgreen', '>20 км': 'salmon'}

for i, param in enumerate(parameters):
    if param in df.columns:
        valid_data = False
        
        total_counts = {}
        available_counts = {}
        
        for category in colors.keys():
            category_data = df[df['diameter_category'] == category]
            total_counts[category] = len(category_data)
            available_counts[category] = category_data[param].notna().sum()

        for category, color in colors.items():
            category_data = df[df['diameter_category'] == category][param].dropna()
            if len(category_data) > 0:
                axes[i].hist(category_data, bins=15, alpha=0.6, 
                           label=f'{category} ({available_counts[category]}/{total_counts[category]})', 
                           color=color, edgecolor='white', linewidth=0.5)
                valid_data = True

        parent_data = df[df['special'] == 'Родительское тело'][param].dropna()
        if len(parent_data) > 0:
            axes[i].axvline(x=parent_data.iloc[0], color='red', linestyle='-', 
                          linewidth=3, alpha=0.4, label='Родительское тело')
        
        specified_data = df[df['special'] == 'Указанный астероид'][param].dropna()
        for j, value in enumerate(specified_data):
            axes[i].axvline(x=value, color='blue', linestyle='--', 
                          linewidth=2, alpha=0.4, label='Указанный астероид' if j == 0 else "")
        
        if valid_data:
            axes[i].set_xlabel("", fontsize=10)
            axes[i].set_ylabel('Частота', fontsize=10)
            
            total_with_data = df[param].notna().sum()
            total_all = len(df)
            axes[i].set_title(f'{param} (данные: {total_with_data}/{total_all})', fontsize=11)
            
            axes[i].legend(fontsize=8)
            axes[i].grid(True, alpha=0.3)
        else:
            axes[i].text(0.5, 0.5, f'Нет данных\nдля {param}', 
                        ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
            axes[i].set_title(f'{param} (нет данных)', fontsize=11)

# Убираем пустые subplots
for i in range(len(parameters), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.suptitle('Распределение параметров по категориям диаметра', fontsize=14, y=1.02)
plt.show()

# 3. Поиск резонансов с Юпитером с выделением особых астероидов
jupiter_a = 5.2

# Основные резонансы с Юпитером
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

plt.figure(figsize=(14, 8))
a_data = df['a'].dropna()

n, bins, patches = plt.hist(a_data, bins=30, alpha=0.7, edgecolor='white', 
                           color='lightsteelblue', linewidth=0.5, label='Все астероиды')

y_max = max(n) * 1.1
resonance_lines = []  # Для легенды

for name, position in resonance_positions.items():
    if position >= a_data.min() and position <= a_data.max():
        line = plt.axvline(x=position, color='orange', linestyle='--', alpha=0.7, linewidth=1.5)
        resonance_lines.append(line)
        plt.text(position, y_max * 0.9, f'{name}\n{position:.2f}', 
                ha='center', va='top', fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="yellow", alpha=0.7))

parent_a = df[df['special'] == 'Родительское тело']['a'].dropna()
if len(parent_a) > 0:
    plt.axvline(x=parent_a.iloc[0], color='red', linestyle='-', 
                linewidth=4, alpha=0.4, label='Родительское тело')

specified_a = df[df['special'] == 'Указанный астероид']['a'].dropna()
for j, value in enumerate(specified_a):
    plt.axvline(x=value, color='blue', linestyle='--', 
                linewidth=3, alpha=0.4, label='Указанный астероид' if j == 0 else "")

if resonance_lines:
    plt.axvline(x=0, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Резонансы с Юпитером')

plt.xlabel('Большая полуось (а.е.)', fontsize=12)
plt.ylabel('Количество астероидов', fontsize=12)
plt.title('Распределение большой полуоси с резонансами Юпитера и выделением особых астероидов', fontsize=13)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()





# ДОПОЛНИТЕЛЬНО: Анализ какие резонансы попадают в область семейства Themis
print("АНАЛИЗ РЕЗОНАНСОВ С ЮПИТЕРОМ:")
print("=" * 50)
print(f"Диапазон большой полуоси семейства Themis: {a_data.min():.3f} - {a_data.max():.3f} а.е.")
print(f"Большая полуось Юпитера: {jupiter_a} а.е.")
print("\nРезонансы, попадающие в область семейства Themis:")

themis_min = a_data.min()
themis_max = a_data.max()

resonances_in_range = []
for name, position in resonance_positions.items():
    if themis_min <= position <= themis_max:
        resonances_in_range.append((name, position))
        print(f"  {name}: {position:.3f} а.е. (в диапазоне)")

if not resonances_in_range:
    print("  Нет резонансов в диапазоне семейства Themis")
else:
    print(f"\nВсего резонансов в диапазоне: {len(resonances_in_range)}")
    
    # Проверяем, находятся ли особые астероиды близко к резонансам
    print("\nБлизость особых астероидов к резонансам:")
    resonance_threshold = 0.02  # 0.02 а.е. = порог близости
    
    # Родительское тело
    if len(parent_a) > 0:
        parent_value = parent_a.iloc[0]
        for name, resonance_pos in resonances_in_range:
            distance = abs(parent_value - resonance_pos)
            if distance <= resonance_threshold:
                print(f"  Родительское тело ({parent_value:.3f} а.е.) близко к резонансу {name} ({resonance_pos:.3f} а.е.)")
    
    # Указанные астероиды
    for asteroid_id in specified_asteroids:
        asteroid_data = df[df['pdes'] == asteroid_id]['a'].dropna()
        if len(asteroid_data) > 0:
            asteroid_value = asteroid_data.iloc[0]
            for name, resonance_pos in resonances_in_range:
                distance = abs(asteroid_value - resonance_pos)
                if distance <= resonance_threshold:
                    print(f"  Астероид {asteroid_id} ({asteroid_value:.3f} а.е.) близко к резонансу {name} ({resonance_pos:.3f} а.е.)")







# 5. Сравнение распределений параметров с первыми 500 астероидами
df_500 = pd.read_csv('sbdb_query_500.csv')

df_500['pdes'] = df_500['pdes'].astype(str)
df_500['diameter'] = pd.to_numeric(df_500['diameter'], errors='coerce')
if 'albedo' in df_500.columns:
    df_500['albedo'] = pd.to_numeric(df_500['albedo'], errors='coerce')

df_500['special'] = 'Обычный'
df_500.loc[df_500['pdes'] == parent_body_id, 'special'] = 'Родительское тело'
df_500.loc[df_500['pdes'].isin(specified_asteroids), 'special'] = 'Указанный астероид'

# Параметры для сравнения
comparison_params = ['a', 'e', 'i']
if 'albedo' in df.columns and 'albedo' in df_500.columns:
    comparison_params.append('albedo')

print(f"Размер семейства Themis: {len(df)} астероидов")
print(f"Первые 500 астероидов: {len(df_500)} астероидов")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()

colors = {
    'Themis': '#1f77b4',  
    'Первые 500': '#ff7f0e',  
    'Родительское тело': '#d62728', 
    'Указанный астероид': '#2ca02c' 
}

for i, param in enumerate(comparison_params):
    if i < len(axes):
        if param in df.columns and param in df_500.columns:
            themis_data = df[param].dropna()
            first_500_data = df_500[param].dropna()
            if len(themis_data) > 0 and len(first_500_data) > 0:
                sns.kdeplot(data=themis_data, ax=axes[i], color=colors['Themis'], 
                           linewidth=2.5, fill=True, alpha=0.6, label=f'Семейство Themis ({len(themis_data)})',
                           bw_adjust=0.8)
                sns.kdeplot(data=first_500_data, ax=axes[i], color=colors['Первые 500'], 
                           linewidth=2.5, fill=True, alpha=0.6, label=f'Первые 500 ({len(first_500_data)})',
                           bw_adjust=0.8)
                sns.rugplot(data=themis_data, ax=axes[i], color=colors['Themis'], height=0.03, alpha=0.5)
                sns.rugplot(data=first_500_data, ax=axes[i], color=colors['Первые 500'], height=0.03, alpha=0.5)
                
                themis_special = df[df['special'] != 'Обычный']
                themis_parent_shown = False
                themis_specified_shown = False
                
                for _, asteroid in themis_special.iterrows():
                    if pd.notna(asteroid[param]):
                        if asteroid['special'] == 'Родительское тело':
                            color = colors['Родительское тело']
                            linestyle = '-'
                            label = 'Родительское тело (Themis)' if not themis_parent_shown else ""
                            themis_parent_shown = True
                        else:
                            color = colors['Указанный астероид']
                            linestyle = '--'
                            label = 'Указанный астероид (Themis)' if not themis_specified_shown else ""
                            themis_specified_shown = True
                        
                        axes[i].axvline(x=asteroid[param], color=color, linestyle=linestyle,
                                      linewidth=2, alpha=0.4, label=label)
                
                five00_special = df_500[df_500['special'] != 'Обычный']
                five00_parent_shown = False
                five00_specified_shown = False

                axes[i].set_xlabel(param, fontsize=12, fontweight='bold')
                axes[i].set_ylabel('Плотность вероятности', fontsize=11)
                axes[i].set_title(f'Сравнение распределения {param}', fontsize=14, fontweight='bold', pad=15)
                
                stats_text = f'Themis: n={len(themis_data)}\n500: n={len(first_500_data)}'
                axes[i].text(0.02, 0.98, stats_text, transform=axes[i].transAxes, 
                            fontsize=9, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                
                axes[i].legend(fontsize=9, framealpha=0.9, loc='upper right')
                axes[i].grid(True, alpha=0.2, linestyle='--')
                axes[i].tick_params(axis='both', which='major', labelsize=10)
        
        else:
            axes[i].text(0.5, 0.5, f'Нет данных\nдля {param}', 
                        ha='center', va='center', transform=axes[i].transAxes, 
                        fontsize=14, style='italic')
            axes[i].set_title(f'Сравнение {param}', fontsize=14, fontweight='bold')
            axes[i].set_xlabel(param)

for i in range(len(comparison_params), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.suptitle('Сравнение распределений параметров: Семейство Themis vs Первые 500 астероидов', 
             fontsize=16, fontweight='bold', y=1.02)
plt.show()



# 6. Графики цветовых параметров и альбедо в стиле как на фото
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()
colors = {
    'BV': '#1f77b4',
    'UB': '#2ca02c', 
    'IR': '#ff7f0e',
    'albedo': '#d62728',
    'Родительское тело': "#c9653e",
    'Указанный астероид': "#25b53d"
}
color_params = ['BV', 'UB', 'IR', 'albedo']
titles = ['Распределение BV', 'Распределение UB', 'Распределение IR', 'Распределение Albedo']

for i, param in enumerate(color_params):
    if i >= len(axes):
        break
        
    if param not in df.columns:
        axes[i].text(0.5, 0.5, f'Нет данных\nдля {param}', 
                    ha='center', va='center', transform=axes[i].transAxes, 
                    fontsize=14, style='italic')
        axes[i].set_title(titles[i], fontsize=14, fontweight='bold')
        continue
    
    data = df[param].dropna()
    if len(data) == 0:
        axes[i].text(0.5, 0.5, f'Недостаточно данных\n{param}', 
                    ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
        axes[i].set_title(titles[i], fontsize=14, fontweight='bold')
        continue
    sns.kdeplot(data=data, ax=axes[i], color=colors[param], 
                linewidth=2.5, fill=True, alpha=0.6, bw_adjust=0.8)
    
    sns.rugplot(data=data, ax=axes[i], color=colors[param], height=0.05, alpha=0.5)

    parent_data = df[df['special'] == 'Родительское тело'][param].dropna()
    parent_shown = False
    for value in parent_data:
        label = 'Родительское тело' if not parent_shown else ""
        axes[i].axvline(x=value, color=colors['Родительское тело'], linestyle='-', 
                       linewidth=3, alpha=0.8, label=label)
        parent_shown = True

    specified_data = df[df['special'] == 'Указанный астероид'][param].dropna()
    specified_shown = False
    for value in specified_data:
        label = 'Указанный астероид' if not specified_shown else ""
        axes[i].axvline(x=value, color=colors['Указанный астероид'], linestyle='--', 
                       linewidth=2, alpha=0.7, label=label)
        specified_shown = True
    
    axes[i].set_xlabel(param, fontsize=12, fontweight='bold')
    axes[i].set_ylabel('Плотность вероятности', fontsize=11)
    axes[i].set_title(titles[i], fontsize=14, fontweight='bold', pad=15)
    
    stats_text = f'n={len(data)}\nμ={data.mean():.2f}\nσ={data.std():.2f}'
    axes[i].text(0.02, 0.98, stats_text, transform=axes[i].transAxes, 
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    if len(parent_data) > 0 or len(specified_data) > 0:
        axes[i].legend(fontsize=9, framealpha=0.9)
    
    axes[i].grid(True, alpha=0.2, linestyle='--')
    axes[i].tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.suptitle('Распределение цветовых параметров и альбедо семейства Themis', 
             fontsize=16, fontweight='bold', y=1.02)
plt.show()

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()

color_combinations = [
    ('BV', 'UB', 'BV vs UB'),
    ('BV', 'IR', 'BV vs IR'), 
    ('UB', 'IR', 'UB vs IR'),
    ('BV', 'albedo', 'BV vs Albedo')
]

for i, (x_param, y_param, title) in enumerate(color_combinations):
    if i >= len(axes):
        break
        
    if x_param not in df.columns or y_param not in df.columns:
        axes[i].text(0.5, 0.5, f'Нет данных\nдля {x_param} и {y_param}', 
                    ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
        axes[i].set_title(title, fontsize=14, fontweight='bold')
        continue
    valid_data = df.dropna(subset=[x_param, y_param])
    
    if len(valid_data) == 0:
        axes[i].text(0.5, 0.5, f'Недостаточно данных\nдля {x_param} и {y_param}', 
                    ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
        axes[i].set_title(title, fontsize=14, fontweight='bold')
        continue
    size_map = {'Обычный': 40, 'Указанный астероид': 80, 'Родительское тело': 120}

    for special_type in ['Обычный', 'Указанный астероид', 'Родительское тело']:
        data_subset = valid_data[valid_data['special'] == special_type]
        if len(data_subset) > 0:
            if special_type == 'Обычный':
                color = 'lightgray'
                alpha = 0.9
                edgecolor = 'none'
            elif special_type == 'Указанный астероид':
                color = colors['Указанный астероид']
                alpha = 0.8
                edgecolor = 'black'
            else: 
                color = colors['Родительское тело']
                alpha = 0.9
                edgecolor = 'black'
            
            axes[i].scatter(data_subset[x_param], data_subset[y_param],
                          c=color, s=size_map[special_type], marker='o',
                          alpha=alpha, edgecolors=edgecolor,
                          linewidth=1 if special_type != 'Обычный' else 0,
                          label=special_type)
    
    axes[i].set_xlabel(x_param, fontsize=12, fontweight='bold')
    axes[i].set_ylabel(y_param, fontsize=12, fontweight='bold')
    axes[i].set_title(title, fontsize=14, fontweight='bold', pad=15)
    axes[i].legend(fontsize=9, framealpha=0.9)
    axes[i].grid(True, alpha=0.2, linestyle='--')
    axes[i].tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.suptitle('Диаграммы рассеяния цветовых параметров семейства Themis', 
             fontsize=16, fontweight='bold', y=1.02)
plt.show()



# Цветовая схема
palette = {
    'BV': '#1f77b4',
    'UB': '#2ca02c', 
    'IR': '#ff7f0e',
    'albedo': '#d62728',
    'Обычный': 'lightgray',
    'Указанный астероид': 'blue',
    'Родительское тело': 'red'
}

# Параметры для анализа
color_params = ['BV', 'UB', 'IR', 'albedo']

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()

for i, param in enumerate(color_params):
    if param not in df.columns:
        axes[i].text(0.5, 0.5, f'Нет данных для {param}', 
                    ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
        axes[i].set_title(f'Все точки {param}', fontsize=14, fontweight='bold')
        continue
    
    plot_data = df[[param, 'special']].dropna()
    
    if len(plot_data) == 0:
        axes[i].text(0.5, 0.5, f'Недостаточно данных\n{param}', 
                    ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
        axes[i].set_title(f'Все точки {param}', fontsize=14, fontweight='bold')
        continue
    
    # Множественные слои точек для максимальной видимости
    # Слой 1: Основные точки
    sns.stripplot(data=plot_data, y=param, x=0, ax=axes[i],
                  hue='special', palette=palette, 
                  size=8, alpha=0.8, jitter=0.3)
    
    # Слой 2: Дополнительные точки для плотности
    sns.stripplot(data=plot_data, y=param, x=0, ax=axes[i],
                  hue='special', palette=palette, 
                  size=5, alpha=0.6, jitter=0.2, legend=False)
    
    # Слой 3: Еще больше точек
    sns.stripplot(data=plot_data, y=param, x=0, ax=axes[i],
                  color='black', size=3, alpha=0.3, jitter=0.15, legend=False)
    
    axes[i].set_xlabel('')
    axes[i].set_ylabel(param, fontsize=12, fontweight='bold')
    axes[i].set_title(f'Все точки {param} (n={len(plot_data)})', fontsize=14, fontweight='bold')
    axes[i].grid(True, alpha=0.3, axis='y')
    axes[i].set_xticks([])

plt.tight_layout()
plt.suptitle('Максимальное количество точек - все цветовые параметры и альбедо', 
             fontsize=16, fontweight='bold', y=1.02)
plt.show()