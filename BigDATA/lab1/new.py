import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')

# Установка стиля для лучшего отображения
plt.style.use('default')
sns.set_style("whitegrid")

# Загрузка данных
df = pd.read_csv('filtered_sbdb_data.csv')

# Преобразование типов данных
df['pdes'] = df['pdes'].astype(str)
df['diameter'] = pd.to_numeric(df['diameter'], errors='coerce')

# Создание категорий по диаметру (точно по заданию)
df['diameter_category'] = pd.cut(df['diameter'], 
                                bins=[0, 2, 20, np.inf],
                                labels=['<2 км', '2-20 км', '>20 км'],
                                right=False)

# Определение родительского тела и указанных астероидов
parent_body_id = '24'  # Themis
specified_asteroids = ['62', '90', '171', '222']  # Замените на указанные преподавателем

df['special'] = 'Обычный'
df.loc[df['pdes'] == parent_body_id, 'special'] = 'Родительское тело'
df.loc[df['pdes'].isin(specified_asteroids), 'special'] = 'Указанный астероид'

# Цветовая схема для особых астероидов
special_colors = {'Обычный': 'lightgray', 'Родительское тело': 'red', 'Указанный астероид': 'blue'}

# 1. Гистограммы для всех параметров с выделением особых астероидов И ИНФОРМАЦИЕЙ О ПРОПУСКАХ
parameters = ['spec_B', 'spec_T', 'a', 'e', 'i', 'q', 'H', 'rot_per']
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()

for i, param in enumerate(parameters):
    if param in df.columns:
        # Считаем статистику по пропускам
        total_count = len(df)
        available_count = df[param].notna().sum()
        missing_count = total_count - available_count
        missing_percent = (missing_count / total_count) * 100
        
        if available_count > 0:
            # Основная гистограмма для всех астероидов (только доступные данные)
            data = df[param].dropna()
            axes[i].hist(data, bins=20, alpha=0.5, edgecolor='black', 
                        color='purple', linewidth=0.5, label=f'Все астероиды ({available_count}/{total_count})')
            
            # Выделение родительского тела
            parent_data = df[df['special'] == 'Родительское тело'][param].dropna()
            if len(parent_data) > 0:
                axes[i].axvline(x=parent_data.iloc[0], color='red', linestyle='-', 
                              linewidth=3, alpha=0.8, label='Родительское тело')
            
            # Выделение указанных астероидов
            specified_data = df[df['special'] == 'Указанный астероид'][param].dropna()
            for j, value in enumerate(specified_data):
                axes[i].axvline(x=value, color='blue', linestyle='--', 
                              linewidth=2, alpha=0.8, label='Указанный астероид' if j == 0 else "")
            
            axes[i].set_xlabel("", fontsize=10)
            axes[i].set_ylabel('Частота', fontsize=10)
            axes[i].set_title(f'Распределение {param} (пропуски: {missing_percent:.1f}%)', fontsize=8)
            axes[i].grid(True, alpha=0.3)
            
            # Добавляем легенду только если есть особые астероиды
            if len(parent_data) > 0 or len(specified_data) > 0:
                axes[i].legend(fontsize=8)
            else:
                axes[i].legend(fontsize=8)  # Всегда показываем легенду с информацией о данных
        else:
            # Если вообще нет данных для параметра
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
        
        # Считаем общее количество и количество с данными
        total_counts = {}
        available_counts = {}
        
        for category in colors.keys():
            category_data = df[df['diameter_category'] == category]
            total_counts[category] = len(category_data)
            available_counts[category] = category_data[param].notna().sum()
        
        # Гистограммы по категориям диаметра
        for category, color in colors.items():
            category_data = df[df['diameter_category'] == category][param].dropna()
            if len(category_data) > 0:
                axes[i].hist(category_data, bins=15, alpha=0.6, 
                           label=f'{category} ({available_counts[category]}/{total_counts[category]})', 
                           color=color, edgecolor='white', linewidth=0.5)
                valid_data = True
        
        # Выделение особых астероидов (остается как было)
        parent_data = df[df['special'] == 'Родительское тело'][param].dropna()
        if len(parent_data) > 0:
            axes[i].axvline(x=parent_data.iloc[0], color='red', linestyle='-', 
                          linewidth=3, alpha=0.9, label='Родительское тело')
        
        specified_data = df[df['special'] == 'Указанный астероид'][param].dropna()
        for j, value in enumerate(specified_data):
            axes[i].axvline(x=value, color='blue', linestyle='--', 
                          linewidth=2, alpha=0.9, label='Указанный астероид' if j == 0 else "")
        
        if valid_data:
            axes[i].set_xlabel("", fontsize=10)
            axes[i].set_ylabel('Частота', fontsize=10)
            
            # Добавляем информацию о пропусках в заголовок
            total_with_data = df[param].notna().sum()
            total_all = len(df)
            axes[i].set_title(f'{param} (данные: {total_with_data}/{total_all})', fontsize=11)
            
            axes[i].legend(fontsize=8)
            axes[i].grid(True, alpha=0.3)
        else:
            # Если вообще нет данных для параметра
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

# Визуализация резонансов с выделением особых астероидов
plt.figure(figsize=(14, 8))
a_data = df['a'].dropna()

# Гистограмма большой полуоси
n, bins, patches = plt.hist(a_data, bins=30, alpha=0.7, edgecolor='white', 
                           color='lightsteelblue', linewidth=0.5, label='Все астероиды')

# Добавление линий резонансов
y_max = max(n) * 1.1
resonance_lines = []  # Для легенды

for name, position in resonance_positions.items():
    if position >= a_data.min() and position <= a_data.max():
        line = plt.axvline(x=position, color='orange', linestyle='--', alpha=0.7, linewidth=1.5)
        resonance_lines.append(line)
        plt.text(position, y_max * 0.9, f'{name}\n{position:.2f}', 
                ha='center', va='top', fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="yellow", alpha=0.7))

# Выделение родительского тела
parent_a = df[df['special'] == 'Родительское тело']['a'].dropna()
if len(parent_a) > 0:
    plt.axvline(x=parent_a.iloc[0], color='red', linestyle='-', 
                linewidth=4, alpha=0.9, label='Родительское тело')

# Выделение указанных астероидов
specified_a = df[df['special'] == 'Указанный астероид']['a'].dropna()
for j, value in enumerate(specified_a):
    plt.axvline(x=value, color='blue', linestyle='--', 
                linewidth=3, alpha=0.9, label='Указанный астероид' if j == 0 else "")

# Добавляем резонансы в легенду
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
# Загрузка данных первых 500 астероидов
df_500 = pd.read_csv('sbdb_query_500.csv')

# Преобразование типов данных для df_500
df_500['pdes'] = df_500['pdes'].astype(str)
df_500['diameter'] = pd.to_numeric(df_500['diameter'], errors='coerce')
if 'albedo' in df_500.columns:
    df_500['albedo'] = pd.to_numeric(df_500['albedo'], errors='coerce')

# Определение особых астероидов в df_500
df_500['special'] = 'Обычный'
df_500.loc[df_500['pdes'] == parent_body_id, 'special'] = 'Родительское тело'
df_500.loc[df_500['pdes'].isin(specified_asteroids), 'special'] = 'Указанный астероид'

# Параметры для сравнения
comparison_params = ['a', 'e', 'i']
if 'albedo' in df.columns and 'albedo' in df_500.columns:
    comparison_params.append('albedo')

# Определяем использовать ли логарифмическую шкалу
use_log_scale = len(df) >= 500  # Логарифмическая если семейство >= 500 астероидов

print(f"Размер семейства Themis: {len(df)} астероидов")
print(f"Использовать логарифмическую шкалу: {use_log_scale}")

# Создаем графики сравнения
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()

for i, param in enumerate(comparison_params):
    if i < len(axes):
        if param in df.columns and param in df_500.columns:
            # Данные семейства Themis
            themis_data = df[param].dropna()
            # Данные первых 500 астероидов
            first_500_data = df_500[param].dropna()
            
            if len(themis_data) > 0 and len(first_500_data) > 0:
                # Определяем общие границы для бинов
                all_data = pd.concat([themis_data, first_500_data])
                data_min = all_data.min()
                data_max = all_data.max()
                bins = 30
                
                # Строим гистограммы
                if use_log_scale:
                    # Гистограммы с логарифмической шкалой Y
                    counts_themis, bins_themis = np.histogram(themis_data, bins=bins, range=(data_min, data_max))
                    counts_500, bins_500 = np.histogram(first_500_data, bins=bins, range=(data_min, data_max))
                    
                    # Логарифмируем counts (избегая log(0))
                    log_counts_themis = np.log10(counts_themis + 1)
                    log_counts_500 = np.log10(counts_500 + 1)
                    
                    # Строим ступенчатые графики
                    axes[i].step(bins_themis[:-1], log_counts_themis, where='post', 
                               color='red', linewidth=2, label=f'Семейство Themis ({len(themis_data)})')
                    axes[i].step(bins_500[:-1], log_counts_500, where='post', 
                               color='blue', linewidth=2, alpha=0.7, label=f'Первые 500 ({len(first_500_data)})')
                    axes[i].set_ylabel('log₁₀(Частота + 1)')
                else:
                    # Обычные гистограммы
                    axes[i].hist(themis_data, bins=bins, alpha=0.7, color='red', 
                               edgecolor='white', linewidth=0.5, label=f'Семейство Themis ({len(themis_data)})')
                    axes[i].hist(first_500_data, bins=bins, alpha=0.5, color='blue', 
                               edgecolor='white', linewidth=0.5, label=f'Первые 500 ({len(first_500_data)})')
                    axes[i].set_ylabel('Частота')
                
                # Выделение особых астероидов в семействе Themis
                # Родительское тело
                parent_data = df[df['special'] == 'Родительское тело'][param].dropna()
                if len(parent_data) > 0:
                    axes[i].axvline(x=parent_data.iloc[0], color='darkred', linestyle='-', 
                                  linewidth=3, alpha=0.9, label='Родительское тело (Themis)')
                
                # Указанные астероиды в семействе Themis
                specified_data = df[df['special'] == 'Указанный астероид'][param].dropna()
                for j, value in enumerate(specified_data):
                    axes[i].axvline(x=value, color='purple', linestyle='--', 
                                  linewidth=2, alpha=0.9, label='Указанный астероид (Themis)' if j == 0 else "")
                
                # Выделение особых астероидов в первых 500 (если есть)
                parent_in_500 = df_500[df_500['special'] == 'Родительское тело'][param].dropna()
                if len(parent_in_500) > 0:
                    axes[i].axvline(x=parent_in_500.iloc[0], color='darkred', linestyle=':', 
                                  linewidth=2, alpha=0.7, label='Родительское тело (500)')
                
                specified_in_500 = df_500[df_500['special'] == 'Указанный астероид'][param].dropna()
                for j, value in enumerate(specified_in_500):
                    axes[i].axvline(x=value, color='purple', linestyle=':', 
                                  linewidth=1.5, alpha=0.7, label='Указанный астероид (500)' if j == 0 else "")
                
                axes[i].set_xlabel(param)
                axes[i].set_title(f'Сравнение {param}: Themis vs Первые 500')
                axes[i].legend(fontsize=8)
                axes[i].grid(True, alpha=0.3)
        
        # Если параметр отсутствует в одном из наборов данных
        else:
            axes[i].text(0.5, 0.5, f'Нет данных\nдля {param}', 
                        ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
            axes[i].set_title(f'Сравнение {param}')
            axes[i].set_xlabel(param)
            axes[i].set_ylabel('Частота')

# Убираем лишние subplots
for i in range(len(comparison_params), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
scale_type = "логарифмической" if use_log_scale else "обычной"
plt.suptitle(f'Сравнение распределений параметров ({scale_type} шкала)', fontsize=16, y=1.02)
plt.show()

# Дополнительная статистика сравнения
print("\nСТАТИСТИКА СРАВНЕНИЯ:")
print("=" * 50)
print(f"Семейство Themis: {len(df)} астероидов")
print(f"Первые 500 астероидов: {len(df_500)} астероидов")

# Функция для вычисления перекрытия распределений
def calculate_overlap(data1, data2, bins=30):
    """Вычисляет процент перекрытия двух распределений"""
    all_data = pd.concat([data1, data2])
    hist1, edges = np.histogram(data1, bins=bins, range=(all_data.min(), all_data.max()))
    hist2, _ = np.histogram(data2, bins=bins, range=(all_data.min(), all_data.max()))
    
    overlap = np.minimum(hist1, hist2).sum()
    total = hist1.sum() + hist2.sum()
    
    return (overlap / total) * 100

for param in comparison_params:
    if param in df.columns and param in df_500.columns:
        themis_data = df[param].dropna()
        first_500_data = df_500[param].dropna()
        
        if len(themis_data) > 0 and len(first_500_data) > 0:
            print(f"\n--- {param} ---")
            print(f"Themis:     среднее = {themis_data.mean():.3f}, std = {themis_data.std():.3f}, n = {len(themis_data)}")
            print(f"Первые 500: среднее = {first_500_data.mean():.3f}, std = {first_500_data.std():.3f}, n = {len(first_500_data)}")
            
            # Вычисляем перекрытие распределений
            overlap_percent = calculate_overlap(themis_data, first_500_data)
            print(f"Перекрытие распределений: {overlap_percent:.1f}%")
            
            # Простой анализ различий
            mean_diff = abs(themis_data.mean() - first_500_data.mean())
            std_ratio = themis_data.std() / first_500_data.std() if first_500_data.std() > 0 else 0
            
            print(f"Разница средних: {mean_diff:.3f}")
            if mean_diff > themis_data.std() * 0.5:
                print("  → Заметная разница в средних значениях")
            
            if std_ratio < 0.7 or std_ratio > 1.3:
                print("  → Заметная разница в разбросе данных")

# Дополнительный график: сравнение альбедо (если есть данные)
if 'albedo' in df.columns and 'albedo' in df_500.columns:
    plt.figure(figsize=(10, 6))
    
    themis_albedo = df['albedo'].dropna()
    first_500_albedo = df_500['albedo'].dropna()
    
    if len(themis_albedo) > 0 and len(first_500_albedo) > 0:
        if use_log_scale:
            counts_t, bins_t = np.histogram(themis_albedo, bins=30)
            counts_500, bins_500 = np.histogram(first_500_albedo, bins=30)
            
            log_counts_t = np.log10(counts_t + 1)
            log_counts_500 = np.log10(counts_500 + 1)
            
            plt.step(bins_t[:-1], log_counts_t, where='post', 
                   color='red', linewidth=2, label=f'Семейство Themis ({len(themis_albedo)})')
            plt.step(bins_500[:-1], log_counts_500, where='post', 
                   color='blue', linewidth=2, alpha=0.7, label=f'Первые 500 ({len(first_500_albedo)})')
            plt.ylabel('log₁₀(Частота + 1)')
        else:
            plt.hist(themis_albedo, bins=30, alpha=0.7, color='red', 
                   edgecolor='white', linewidth=0.5, label=f'Семейство Themis ({len(themis_albedo)})')
            plt.hist(first_500_albedo, bins=30, alpha=0.5, color='blue', 
                   edgecolor='white', linewidth=0.5, label=f'Первые 500 ({len(first_500_albedo)})')
            plt.ylabel('Частота')
        
        # Выделение особых астероидов
        parent_albedo = df[df['special'] == 'Родительское тело']['albedo'].dropna()
        if len(parent_albedo) > 0:
            plt.axvline(x=parent_albedo.iloc[0], color='darkred', linestyle='-', 
                      linewidth=3, alpha=0.9, label='Родительское тело (Themis)')
        
        specified_albedo = df[df['special'] == 'Указанный астероид']['albedo'].dropna()
        for j, value in enumerate(specified_albedo):
            plt.axvline(x=value, color='purple', linestyle='--', 
                      linewidth=2, alpha=0.9, label='Указанный астероид (Themis)' if j == 0 else "")
        
        plt.xlabel('Альбедо')
        plt.title('Сравнение распределения альбедо')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

# Проверка наличия особых астероидов в обоих наборах
print("\nОСОБЫЕ АСТЕРОИДЫ В НАБОРАХ ДАННЫХ:")
print("=" * 50)
print("В семействе Themis:")
special_in_themis = df[df['special'].isin(['Родительское тело', 'Указанный астероид'])]
for _, asteroid in special_in_themis.iterrows():
    print(f"  {asteroid['special']}: ID {asteroid['pdes']}")

print("\nВ первых 500 астероидах:")
special_in_500 = df_500[df_500['special'].isin(['Родительское тело', 'Указанный астероид'])]
for _, asteroid in special_in_500.iterrows():
    print(f"  {asteroid['special']}: ID {asteroid['pdes']}")



# 6. Графики цветовых параметров и альбедо через Seaborn
# Создаем фигуру с такой же компоновкой как на фото
fig = plt.figure(figsize=(15, 12))

# Создаем сетку графиков 2x2 с разными размерами
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

# 1. Верхний левый график: BV
ax1 = fig.add_subplot(gs[0, 0])
if 'BV' in df.columns:
    bv_data = df['BV'].dropna()
    if len(bv_data) > 0:
        # Основное распределение
        sns.histplot(data=df, x='BV', ax=ax1, color='skyblue', alpha=0.7, 
                    edgecolor='white', linewidth=0.5, bins=20)
        
        # Выделение особых астероидов
        # Родительское тело
        parent_bv = df[df['special'] == 'Родительское тело']['BV'].dropna()
        if len(parent_bv) > 0:
            ax1.axvline(x=parent_bv.iloc[0], color='red', linestyle='-', 
                       linewidth=3, alpha=0.9, label='Родительское тело')
        
        # Указанные астероиды
        specified_bv = df[df['special'] == 'Указанный астероид']['BV'].dropna()
        for j, value in enumerate(specified_bv):
            ax1.axvline(x=value, color='blue', linestyle='--', 
                       linewidth=2, alpha=0.9, label='Указанный астероид' if j == 0 else "")
        
        ax1.set_xlabel('BV')
        ax1.set_ylabel('Частота')
        ax1.set_title('Распределение BV')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)
    else:
        ax1.text(0.5, 0.5, 'Нет данных BV', ha='center', va='center', 
                transform=ax1.transAxes, fontsize=12)
        ax1.set_title('Распределение BV')
else:
    ax1.text(0.5, 0.5, 'Нет данных BV', ha='center', va='center', 
            transform=ax1.transAxes, fontsize=12)
    ax1.set_title('Распределение BV')

# 2. Верхний правый график: UB
ax2 = fig.add_subplot(gs[0, 1])
if 'UB' in df.columns:
    ub_data = df['UB'].dropna()
    if len(ub_data) > 0:
        # Основное распределение
        sns.histplot(data=df, x='UB', ax=ax2, color='lightgreen', alpha=0.7, 
                    edgecolor='white', linewidth=0.5, bins=20)
        
        # Выделение особых астероидов
        # Родительское тело
        parent_ub = df[df['special'] == 'Родительское тело']['UB'].dropna()
        if len(parent_ub) > 0:
            ax2.axvline(x=parent_ub.iloc[0], color='red', linestyle='-', 
                       linewidth=3, alpha=0.9, label='Родительское тело')
        
        # Указанные астероиды
        specified_ub = df[df['special'] == 'Указанный астероид']['UB'].dropna()
        for j, value in enumerate(specified_ub):
            ax2.axvline(x=value, color='blue', linestyle='--', 
                       linewidth=2, alpha=0.9, label='Указанный астероид' if j == 0 else "")
        
        ax2.set_xlabel('UB')
        ax2.set_ylabel('Частота')
        ax2.set_title('Распределение UB')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'Нет данных UB', ha='center', va='center', 
                transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Распределение UB')
else:
    ax2.text(0.5, 0.5, 'Нет данных UB', ha='center', va='center', 
            transform=ax2.transAxes, fontsize=12)
    ax2.set_title('Распределение UB')

# 3. Нижний левый график: IR
ax3 = fig.add_subplot(gs[1, 0])
if 'IR' in df.columns:
    ir_data = df['IR'].dropna()
    if len(ir_data) > 0:
        # Основное распределение
        sns.histplot(data=df, x='IR', ax=ax3, color='salmon', alpha=0.7, 
                    edgecolor='white', linewidth=0.5, bins=20)
        
        # Выделение особых астероидов
        # Родительское тело
        parent_ir = df[df['special'] == 'Родительское тело']['IR'].dropna()
        if len(parent_ir) > 0:
            ax3.axvline(x=parent_ir.iloc[0], color='red', linestyle='-', 
                       linewidth=3, alpha=0.9, label='Родительское тело')
        
        # Указанные астероиды
        specified_ir = df[df['special'] == 'Указанный астероид']['IR'].dropna()
        for j, value in enumerate(specified_ir):
            ax3.axvline(x=value, color='blue', linestyle='--', 
                       linewidth=2, alpha=0.9, label='Указанный астероид' if j == 0 else "")
        
        ax3.set_xlabel('IR')
        ax3.set_ylabel('Частота')
        ax3.set_title('Распределение IR')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
    else:
        ax3.text(0.5, 0.5, 'Нет данных IR', ha='center', va='center', 
                transform=ax3.transAxes, fontsize=12)
        ax3.set_title('Распределение IR')
else:
    ax3.text(0.5, 0.5, 'Нет данных IR', ha='center', va='center', 
            transform=ax3.transAxes, fontsize=12)
    ax3.set_title('Распределение IR')

# 4. Нижний правый график: Albedo
ax4 = fig.add_subplot(gs[1, 1])
if 'albedo' in df.columns:
    albedo_data = df['albedo'].dropna()
    if len(albedo_data) > 0:
        # Основное распределение
        sns.histplot(data=df, x='albedo', ax=ax4, color='gold', alpha=0.7, 
                    edgecolor='white', linewidth=0.5, bins=20)
        
        # Выделение особых астероидов
        # Родительское тело
        parent_albedo = df[df['special'] == 'Родительское тело']['albedo'].dropna()
        if len(parent_albedo) > 0:
            ax4.axvline(x=parent_albedo.iloc[0], color='red', linestyle='-', 
                       linewidth=3, alpha=0.9, label='Родительское тело')
        
        # Указанные астероиды
        specified_albedo = df[df['special'] == 'Указанный астероид']['albedo'].dropna()
        for j, value in enumerate(specified_albedo):
            ax4.axvline(x=value, color='blue', linestyle='--', 
                       linewidth=2, alpha=0.9, label='Указанный астероид' if j == 0 else "")
        
        ax4.set_xlabel('Albedo')
        ax4.set_ylabel('Частота')
        ax4.set_title('Распределение Albedo')
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3)
    else:
        ax4.text(0.5, 0.5, 'Нет данных Albedo', ha='center', va='center', 
                transform=ax4.transAxes, fontsize=12)
        ax4.set_title('Распределение Albedo')
else:
    ax4.text(0.5, 0.5, 'Нет данных Albedo', ha='center', va='center', 
            transform=ax4.transAxes, fontsize=12)
    ax4.set_title('Распределение Albedo')

plt.tight_layout()
plt.suptitle('Цветовые параметры и альбедо семейства Themis', fontsize=16, y=1.02)
plt.show()

# Дополнительно: scatter plot цветовых параметров
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.flatten()

color_combinations = [
    ('BV', 'UB', 'Цветовая диаграмма BV vs UB'),
    ('BV', 'IR', 'Цветовая диаграмма BV vs IR'), 
    ('UB', 'IR', 'Цветовая диаграмма UB vs IR'),
    ('BV', 'albedo', 'BV vs Albedo')
]

for i, (x_param, y_param, title) in enumerate(color_combinations):
    if i < len(axes):
        if x_param in df.columns and y_param in df.columns:
            # Фильтруем данные где оба параметра присутствуют
            valid_data = df.dropna(subset=[x_param, y_param])
            
            if len(valid_data) > 0:
                # Обычные астероиды
                normal_data = valid_data[valid_data['special'] == 'Обычный']
                if len(normal_data) > 0:
                    axes[i].scatter(normal_data[x_param], normal_data[y_param], 
                                   alpha=0.6, c='gray', s=30, label='Обычные астероиды')
                
                # Родительское тело
                parent_data = valid_data[valid_data['special'] == 'Родительское тело']
                if len(parent_data) > 0:
                    axes[i].scatter(parent_data[x_param], parent_data[y_param], 
                                   c='red', s=200, marker='*', edgecolors='black', 
                                   linewidth=2, label='Родительское тело')
                
                # Указанные астероиды
                specified_data = valid_data[valid_data['special'] == 'Указанный астероид']
                if len(specified_data) > 0:
                    axes[i].scatter(specified_data[x_param], specified_data[y_param], 
                                   c='blue', s=100, marker='D', edgecolors='black', 
                                   linewidth=1.5, label='Указанные астероиды')
                
                axes[i].set_xlabel(x_param)
                axes[i].set_ylabel(y_param)
                axes[i].set_title(title)
                axes[i].legend(fontsize=8)
                axes[i].grid(True, alpha=0.3)
            else:
                axes[i].text(0.5, 0.5, f'Нет данных\nдля {x_param} и {y_param}', 
                           ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
                axes[i].set_title(title)
        else:
            axes[i].text(0.5, 0.5, f'Нет данных\nдля {x_param} и/или {y_param}', 
                       ha='center', va='center', transform=axes[i].transAxes, fontsize=12)
            axes[i].set_title(title)

# Убираем лишние subplots
for i in range(len(color_combinations), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.suptitle('Диаграммы рассеяния цветовых параметров', fontsize=16, y=1.02)
plt.show()

# Статистика по цветовым параметрам
print("СТАТИСТИКА ЦВЕТОВЫХ ПАРАМЕТРОВ:")
print("=" * 50)
color_params = ['BV', 'UB', 'IR', 'albedo']

for param in color_params:
    if param in df.columns:
        data = df[param].dropna()
        special_data = df[df['special'].isin(['Родительское тело', 'Указанный астероид'])][param].dropna()
        
        if len(data) > 0:
            print(f"\n{param}:")
            print(f"  Всего данных: {len(data)}/{len(df)} ({len(data)/len(df)*100:.1f}%)")
            print(f"  Среднее: {data.mean():.3f} ± {data.std():.3f}")
            print(f"  Диапазон: [{data.min():.3f}, {data.max():.3f}]")
            
            if len(special_data) > 0:
                print(f"  Особые астероиды:")
                for _, asteroid in df[df['special'].isin(['Родительское тело', 'Указанный астероид'])].iterrows():
                    if pd.notna(asteroid[param]):
                        print(f"    - {asteroid['special']} ID {asteroid['pdes']}: {asteroid[param]:.3f}")