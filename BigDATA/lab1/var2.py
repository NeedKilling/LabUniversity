# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from matplotlib.patches import Patch
# import warnings
# warnings.filterwarnings('ignore')

# # Установка стиля для лучшего отображения
# plt.style.use('seaborn-v0_8')
# sns.set_palette("husl")

# # Загрузка данных
# df = pd.read_csv('filtered_sbdb_data.csv')

# # Преобразование типов данных
# df['pdes'] = df['pdes'].astype(str)
# df['diameter'] = pd.to_numeric(df['diameter'], errors='coerce')

# # Создание категорий по диаметру
# df['diameter_category'] = pd.cut(df['diameter'], 
#                                 bins=[0, 2, 20, np.inf],
#                                 labels=['<2 км', '2-20 км', '>20 км'],
#                                 right=False)

# # Определение родительского тела и указанных астероидов
# parent_body_id = '24'  # Themis
# specified_asteroids = ['62', '90', '171', '222']  # Пример, замените на указанные преподавателем

# df['special'] = 'Обычный'
# df.loc[df['pdes'] == parent_body_id, 'special'] = 'Родительское тело'
# df.loc[df['pdes'].isin(specified_asteroids), 'special'] = 'Указанный астероид'

# # Цветовая схема для особых астероидов
# special_colors = {'Обычный': 'gray', 'Родительское тело': 'red', 'Указанный астероид': 'blue'}

# # 1. Построение гистограмм для всех параметров
# parameters = ['spec_B', 'spec_T', 'a', 'e', 'i', 'q', 'H', 'rot_per']
# fig, axes = plt.subplots(4, 2, figsize=(16, 20))
# axes = axes.flatten()

# for i, param in enumerate(parameters):
#     if param in df.columns and not df[param].isna().all():
#         # Фильтруем NaN значения
#         data = df[param].dropna()
        
#         if len(data) > 0:
#             axes[i].hist(data, bins=20, alpha=0.7, edgecolor='black', color='skyblue')
#             axes[i].set_xlabel(param)
#             axes[i].set_ylabel('Частота')
#             axes[i].set_title(f'Распределение {param}')
#             axes[i].grid(True, alpha=0.3)

# plt.tight_layout()
# plt.suptitle('Гистограммы параметров для всего семейства Themis', fontsize=16, y=1.02)
# plt.show()

# # 2. Гистограммы по категориям диаметра
# fig, axes = plt.subplots(4, 2, figsize=(16, 20))
# axes = axes.flatten()

# colors = {'<2 км': 'lightblue', '2-20 км': 'lightgreen', '>20 км': 'salmon'}

# for i, param in enumerate(parameters):
#     if param in df.columns:
#         for category, color in colors.items():
#             category_data = df[df['diameter_category'] == category][param].dropna()
#             if len(category_data) > 0:
#                 axes[i].hist(category_data, bins=15, alpha=0.7, 
#                            label=category, color=color, edgecolor='black')
        
#         axes[i].set_xlabel(param)
#         axes[i].set_ylabel('Частота')
#         axes[i].set_title(f' {param} по категориям диаметра')
#         axes[i].legend()
#         axes[i].grid(True, alpha=0.3)

# plt.tight_layout()
# plt.suptitle(' по категориям диаметра', fontsize=16, y=1.02)
# plt.show()

# # 3. Графики параметров семейства через seaborn (B-V, U-B, I-R, Albedo)
# fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# # Список параметров для построения
# color_params = ['BV', 'UB', 'IR', 'albedo']
# titles = ['BV', 'UB', 'IR', 'Albedo']

# for i, (param, title) in enumerate(zip(color_params, titles)):
#     ax = axes[i//2, i%2]
    
#     if param in df.columns:
#         # Фильтруем данные без NaN
#         plot_data = df.dropna(subset=[param])
        
#         if len(plot_data) > 0:
#             # Создаем гистограмму с KDE через seaborn
#             sns.histplot(data=plot_data, x=param, hue='special', 
#                         palette=special_colors, alpha=0.7, 
#                         kde=True, element='step', ax=ax)
            
#             ax.set_xlabel(f'{title}', fontsize=12)
#             ax.set_ylabel('Частота', fontsize=12)
#             ax.set_title(f'Распределение {title}', fontsize=14)
#             ax.grid(True, alpha=0.3)
            
#             # Улучшаем легенду
#             ax.legend(title='Тип астероида', title_fontsize=10, fontsize=9)
#         else:
#             ax.text(0.5, 0.5, f'Нет данных по {title}', 
#                    ha='center', va='center', transform=ax.transAxes, fontsize=12)
#             ax.set_title(f'Распределение {title}', fontsize=14)
#     else:
#         ax.text(0.5, 0.5, f'Параметр {title} отсутствует', 
#                ha='center', va='center', transform=ax.transAxes, fontsize=12)
#         ax.set_title(f'Распределение {title}', fontsize=14)

# plt.tight_layout()
# plt.suptitle('Распределение фотометрических параметров семейства Themis', fontsize=16, y=1.02)
# plt.show()

# # 4. АЛЬТЕРНАТИВА BOXPLOT: Violin plot и swarm plot для тех же параметров
# fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# for i, (param, title) in enumerate(zip(color_params, titles)):
#     ax = axes[i//2, i%2]
    
#     if param in df.columns:
#         # Фильтруем данные без NaN
#         plot_data = df.dropna(subset=[param])
        
#         if len(plot_data) > 0:
#             # Создаем violin plot через seaborn
#             sns.violinplot(data=plot_data, x='special', y=param, 
#                           palette=special_colors, ax=ax, inner='quartile')
            
#             # Добавляем точки поверх violin plot
#             sns.stripplot(data=plot_data, x='special', y=param, 
#                          color='black', alpha=0.6, size=2, jitter=True, ax=ax)
            
#             ax.set_xlabel('Тип астероида', fontsize=12)
#             ax.set_ylabel(f'{title}', fontsize=12)
#             ax.set_title(f'Violin plot {title}', fontsize=14)
#             ax.grid(True, alpha=0.3)
            
#             # Поворачиваем подписи по оси X для лучшей читаемости
#             ax.tick_params(axis='x', rotation=45)
#         else:
#             ax.text(0.5, 0.5, f'Нет данных по {title}', 
#                    ha='center', va='center', transform=ax.transAxes, fontsize=12)
#             ax.set_title(f'Violin plot {title}', fontsize=14)
#     else:
#         ax.text(0.5, 0.5, f'Параметр {title} отсутствует', 
#                ha='center', va='center', transform=ax.transAxes, fontsize=12)
#         ax.set_title(f'Violin plot {title}', fontsize=14)

# plt.tight_layout()
# plt.suptitle('Violin plot фотометрических параметров семейства Themis', fontsize=16, y=1.02)
# plt.show()

# # 4.1 ДОПОЛНИТЕЛЬНАЯ АЛЬТЕРНАТИВА: Статистические summary plot
# fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# for i, (param, title) in enumerate(zip(color_params, titles)):
#     ax = axes[i//2, i%2]
    
#     if param in df.columns:
#         # Фильтруем данные без NaN
#         plot_data = df.dropna(subset=[param])
        
#         if len(plot_data) > 0:
#             # Создаем pointplot с отображением доверительных интервалов
#             sns.pointplot(data=plot_data, x='special', y=param, 
#                          palette=special_colors, ax=ax, capsize=0.1, errwidth=1.5)
            
#             # Добавляем точки данных
#             sns.stripplot(data=plot_data, x='special', y=param, 
#                          color='black', alpha=0.5, size=3, jitter=True, ax=ax)
            
#             ax.set_xlabel('Тип астероида', fontsize=12)
#             ax.set_ylabel(f'{title}', fontsize=12)
#             ax.set_title(f'Сравнение средних {title}', fontsize=14)
#             ax.grid(True, alpha=0.3)
            
#             # Поворачиваем подписи по оси X для лучшей читаемости
#             ax.tick_params(axis='x', rotation=45)
#         else:
#             ax.text(0.5, 0.5, f'Нет данных по {title}', 
#                    ha='center', va='center', transform=ax.transAxes, fontsize=12)
#             ax.set_title(f'Сравнение средних {title}', fontsize=14)
#     else:
#         ax.text(0.5, 0.5, f'Параметр {title} отсутствует', 
#                ha='center', va='center', transform=ax.transAxes, fontsize=12)
#         ax.set_title(f'Сравнение средних {title}', fontsize=14)

# plt.tight_layout()
# plt.suptitle('Сравнение средних значений фотометрических параметров', fontsize=16, y=1.02)
# plt.show()

# # 5. Поиск резонансов с Юпитером
# jupiter_a = 5.2

# # Основные резонансы с Юпитером (отношение периодов)
# resonances = {
#     '1:1': 1.0,
#     '2:1': 2.0,
#     '3:1': 3.0,
#     '3:2': 3/2,
#     '4:1': 4.0,
#     '4:3': 4/3,
#     '5:2': 5/2,
#     '5:3': 5/3
# }

# # Вычисление резонансных больших полуосей
# resonance_positions = {}
# for name, ratio in resonances.items():
#     resonance_a = jupiter_a / (ratio**(2/3))
#     resonance_positions[name] = resonance_a

# # Визуализация резонансов
# plt.figure(figsize=(14, 7))
# a_data = df['a'].dropna()

# # Гистограмма большой полуоси
# n, bins, patches = plt.hist(a_data, bins=30, alpha=0.7, edgecolor='black', color='lightsteelblue')
# plt.xlabel('Большая полуось (а.е.)', fontsize=12)
# plt.ylabel('Частота', fontsize=12)
# plt.title('Распределение большой полуоси с резонансами Юпитера', fontsize=14)

# # Добавление линий резонансов
# y_max = max(n) * 1.1
# for name, position in resonance_positions.items():
#     if position >= a_data.min() and position <= a_data.max():
#         plt.axvline(x=position, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
#         # Размещаем подписи с проверкой на перекрытие
#         plt.text(position, y_max * 0.85, f'{name}\n{position:.2f}', 
#                 ha='center', va='top', fontsize=9, 
#                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()

# # 6. Сравнение с первыми 500 астероидами по логарифмической шкале
# # Загрузка данных первых 500 астероидов
# first_500 = pd.read_csv('sbdb_query_500.csv')
# first_500 = first_500.head(500)

# # Создаем объединенный DataFrame для сравнения
# comparison_params = ['a', 'e', 'i', 'albedo']

# fig, axes = plt.subplots(2, 2, figsize=(16, 12))
# axes = axes.flatten()

# for i, param in enumerate(comparison_params):
#     if param in df.columns and param in first_500.columns:
#         # Данные семейства
#         family_data = df[param].dropna()
        
#         # Данные первых 500 астероидов
#         first_500_data = first_500[param].dropna()
        
#         if len(family_data) > 0 and len(first_500_data) > 0:
#             # Используем логарифмическую шкалу если семейство большое
#             log_scale = len(family_data) >= 500
            
#             # Определяем общие границы для гистограмм
#             all_data = pd.concat([family_data, first_500_data])
#             bins = np.linspace(all_data.min(), all_data.max(), 21)
            
#             axes[i].hist(family_data, bins=bins, alpha=0.7, 
#                        label=f'Семейство Themis (n={len(family_data)})', 
#                        color='blue', edgecolor='black', log=log_scale)
#             axes[i].hist(first_500_data, bins=bins, alpha=0.7, 
#                        label=f'Первые 500 астероидов (n={len(first_500_data)})', 
#                        color='orange', edgecolor='black', log=log_scale)
            
#             axes[i].set_xlabel(param, fontsize=11)
#             ylabel = 'Частота (лог масштаб)' if log_scale else 'Частота'
#             axes[i].set_ylabel(ylabel, fontsize=11)
#             axes[i].set_title(f'Сравнение распределения {param}', fontsize=12)
#             axes[i].legend(fontsize=10)
#             axes[i].grid(True, alpha=0.3)

# plt.tight_layout()
# plt.suptitle('Сравнение семейства Themis с первыми 500 астероидами', fontsize=16, y=1.02)
# plt.show()

# # 7. Дополнительные визуализации с выделением особых астероидов
# fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# # a vs e
# scatter1 = axes[0, 0].scatter(df['a'], df['e'], 
#                              c=df['special'].map(special_colors), 
#                              alpha=0.7, s=40, edgecolors='black', linewidth=0.5)
# axes[0, 0].set_xlabel('Большая полуось (a)', fontsize=11)
# axes[0, 0].set_ylabel('Эксцентриситет (e)', fontsize=11)
# axes[0, 0].set_title('a vs e с выделением особых астероидов', fontsize=12)
# axes[0, 0].grid(True, alpha=0.3)

# # i vs albedo
# if 'albedo' in df.columns:
#     scatter2 = axes[0, 1].scatter(df['i'], df['albedo'], 
#                                  c=df['special'].map(special_colors), 
#                                  alpha=0.7, s=40, edgecolors='black', linewidth=0.5)
#     axes[0, 1].set_xlabel('Наклонение (i)', fontsize=11)
#     axes[0, 1].set_ylabel('Альбедо', fontsize=11)
#     axes[0, 1].set_title('i vs albedo', fontsize=12)
#     axes[0, 1].grid(True, alpha=0.3)

# # H vs diameter
# scatter3 = axes[1, 0].scatter(df['H'], df['diameter'], 
#                              c=df['special'].map(special_colors), 
#                              alpha=0.7, s=40, edgecolors='black', linewidth=0.5)
# axes[1, 0].set_xlabel('Абсолютная магнитуда (H)', fontsize=11)
# axes[1, 0].set_ylabel('Диаметр', fontsize=11)
# axes[1, 0].set_title('H vs diameter', fontsize=12)
# axes[1, 0].grid(True, alpha=0.3)

# # Создаем легенду для особых астероидов
# legend_elements = [Patch(facecolor=color, label=label, alpha=0.7) 
#                   for label, color in special_colors.items()]
# axes[1, 1].legend(handles=legend_elements, loc='center', fontsize=11)
# axes[1, 1].axis('off')
# axes[1, 1].set_title('Легенда: особые астероиды', fontsize=12)

# plt.tight_layout()
# plt.show()

# # 8. Статистика по резонансам
# print("Анализ резонансов с Юпитером:")
# print("=" * 50)

# for name, position in resonance_positions.items():
#     if position >= df['a'].min() and position <= df['a'].max():
#         # Астероиды вблизи резонанса (±0.1 а.е.)
#         near_resonance = df[(df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)]
#         print(f"Резонанс {name} ({position:.3f} а.е.): {len(near_resonance)} астероидов")
        
#         if len(near_resonance) > 0:
#             # Выделяем особые астероиды
#             special_in_resonance = near_resonance[near_resonance['special'] != 'Обычный']
#             if len(special_in_resonance) > 0:
#                 special_ids = ', '.join(special_in_resonance['pdes'].astype(str).tolist())
#                 print(f"  Особые астероиды: {special_ids}")

# # 9. Сохранение результатов анализа
# df['resonance'] = 'Нет'
# for name, position in resonance_positions.items():
#     mask = (df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)
#     df.loc[mask, 'resonance'] = name

# # Сохраняем обогащенные данные
# df.to_csv('themis_family_analysis.csv', index=False)
# print(f"\nРезультаты анализа сохранены в themis_family_analysis.csv")

# # Вывод основной статистики
# print(f"\nОбщая статистика семейства Themis:")
# print(f"Всего астероидов: {len(df)}")
# print(f"С диаметром >20 км: {len(df[df['diameter_category'] == '>20 км'])}")
# print(f"С диаметром 2-20 км: {len(df[df['diameter_category'] == '2-20 км'])}")
# print(f"С диаметром <2 км: {len(df[df['diameter_category'] == '<2 км'])}")
# print(f"Астероидов в резонансе: {len(df[df['resonance'] != 'Нет'])}")
# print(f"Родительское тело: {parent_body_id}")
# print(f"Указанные астероиды: {', '.join(specified_asteroids)}")



# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from matplotlib.patches import Patch
# import warnings
# warnings.filterwarnings('ignore')

# # Установка стиля для лучшего отображения
# plt.style.use('default')
# sns.set_style("whitegrid")

# # Загрузка данных
# df = pd.read_csv('filtered_sbdb_data.csv')

# # Преобразование типов данных
# df['pdes'] = df['pdes'].astype(str)
# df['diameter'] = pd.to_numeric(df['diameter'], errors='coerce')

# # Создание категорий по диаметру (точно по заданию)
# df['diameter_category'] = pd.cut(df['diameter'], 
#                                 bins=[0, 2, 20, np.inf],
#                                 labels=['<2 км', '2-20 км', '>20 км'],
#                                 right=False)

# # Определение родительского тела и указанных астероидов
# parent_body_id = '24'  # Themis
# specified_asteroids = ['62', '90', '171', '222']  # Замените на указанные преподавателем

# df['special'] = 'Обычный'
# df.loc[df['pdes'] == parent_body_id, 'special'] = 'Родительское тело'
# df.loc[df['pdes'].isin(specified_asteroids), 'special'] = 'Указанный астероид'

# # Цветовая схема для особых астероидов
# special_colors = {'Обычный': 'lightgray', 'Родительское тело': 'red', 'Указанный астероид': 'blue'}

# # 1. Гистограммы для всех параметров (точно как в задании)
# parameters = ['spec_B', 'spec_T', 'a', 'e', 'i', 'q', 'H', 'rot_per']
# fig, axes = plt.subplots(4, 2, figsize=(14, 16))
# axes = axes.flatten()

# for i, param in enumerate(parameters):
#     if param in df.columns and not df[param].isna().all():
#         data = df[param].dropna()
        
#         if len(data) > 0:
#             axes[i].hist(data, bins=20, alpha=0.7, edgecolor='white', 
#                         color='skyblue', linewidth=0.5)
#             axes[i].set_xlabel(param, fontsize=10)
#             axes[i].set_ylabel('Частота', fontsize=10)
#             axes[i].set_title(f'Распределение {param}', fontsize=11)
#             axes[i].grid(True, alpha=0.3)

# # Убираем пустые subplots
# for i in range(len(parameters), len(axes)):
#     axes[i].set_visible(False)

# plt.tight_layout()
# plt.suptitle('Гистограммы параметров для всего семейства Themis', fontsize=14, y=1.02)
# plt.show()

# # 2. Гистограммы по категориям диаметра (точно по заданию)
# fig, axes = plt.subplots(4, 2, figsize=(14, 16))
# axes = axes.flatten()

# colors = {'<2 км': 'lightblue', '2-20 км': 'lightgreen', '>20 км': 'salmon'}

# for i, param in enumerate(parameters):
#     if param in df.columns:
#         valid_data = False
#         for category, color in colors.items():
#             category_data = df[df['diameter_category'] == category][param].dropna()
#             if len(category_data) > 0:
#                 axes[i].hist(category_data, bins=15, alpha=0.7, 
#                            label=category, color=color, edgecolor='white', linewidth=0.5)
#                 valid_data = True
        
#         if valid_data:
#             axes[i].set_xlabel(param, fontsize=10)
#             axes[i].set_ylabel('Частота', fontsize=10)
#             axes[i].set_title(f'{param} по категориям диаметра', fontsize=11)
#             axes[i].legend(fontsize=9)
#             axes[i].grid(True, alpha=0.3)

# # Убираем пустые subplots
# for i in range(len(parameters), len(axes)):
#     axes[i].set_visible(False)

# plt.tight_layout()
# plt.suptitle('Распределение параметров по категориям диаметра', fontsize=14, y=1.02)
# plt.show()

# # 3. Поиск резонансов с Юпитером (точно по заданию)
# jupiter_a = 5.2

# # Основные резонансы с Юпитером
# resonances = {
#     '1:1': 1.0,
#     '2:1': 2.0,
#     '3:1': 3.0,
#     '3:2': 3/2,
#     '4:1': 4.0,
#     '4:3': 4/3,
#     '5:2': 5/2,
#     '5:3': 5/3
# }

# # Вычисление резонансных больших полуосей
# resonance_positions = {}
# for name, ratio in resonances.items():
#     resonance_a = jupiter_a / (ratio**(2/3))
#     resonance_positions[name] = resonance_a

# # Визуализация резонансов
# plt.figure(figsize=(12, 6))
# a_data = df['a'].dropna()

# # Гистограмма большой полуоси
# n, bins, patches = plt.hist(a_data, bins=30, alpha=0.7, edgecolor='white', 
#                            color='lightsteelblue', linewidth=0.5)
# plt.xlabel('Большая полуось (а.е.)', fontsize=12)
# plt.ylabel('Количество астероидов', fontsize=12)
# plt.title('Распределение большой полуоси с резонансами Юпитера', fontsize=13)

# # Добавление линий резонансов
# y_max = max(n) * 1.1
# for name, position in resonance_positions.items():
#     if position >= a_data.min() and position <= a_data.max():
#         plt.axvline(x=position, color='red', linestyle='--', alpha=0.8, linewidth=1.5)
#         plt.text(position, y_max * 0.9, f'{name}\n{position:.2f}', 
#                 ha='center', va='top', fontsize=8,
#                 bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))

# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()

# # 4. Сравнение с первыми 500 астероидами (точно по заданию)
# try:
#     first_500 = pd.read_csv('sbdb_query_500.csv')  # Исправлено название файла
#     first_500 = first_500.head(500)
    
#     comparison_params = ['a', 'e', 'i', 'albedo']
    
#     fig, axes = plt.subplots(2, 2, figsize=(12, 10))
#     axes = axes.flatten()

#     for i, param in enumerate(comparison_params):
#         if param in df.columns and param in first_500.columns:
#             family_data = df[param].dropna()
#             first_500_data = first_500[param].dropna()
            
#             if len(family_data) > 0 and len(first_500_data) > 0:
#                 # Логарифмическая шкала если семейство большое (>500)
#                 log_scale = len(df) >= 500
                
#                 # Общие границы для сравнения
#                 all_data = pd.concat([family_data, first_500_data])
#                 bins = np.linspace(all_data.min(), all_data.max(), 20)
                
#                 axes[i].hist(family_data, bins=bins, alpha=0.7, 
#                            label=f'Семейство Themis (n={len(family_data)})', 
#                            color='blue', edgecolor='white', linewidth=0.5, log=log_scale)
#                 axes[i].hist(first_500_data, bins=bins, alpha=0.7, 
#                            label=f'Первые 500 астероидов (n={len(first_500_data)})', 
#                            color='orange', edgecolor='white', linewidth=0.5, log=log_scale)
                
#                 axes[i].set_xlabel(param, fontsize=11)
#                 ylabel = 'Частота (лог)' if log_scale else 'Частота'
#                 axes[i].set_ylabel(ylabel, fontsize=11)
#                 axes[i].set_title(f'Сравнение {param}', fontsize=12)
#                 axes[i].legend(fontsize=9)
#                 axes[i].grid(True, alpha=0.3)

#     plt.tight_layout()
#     plt.suptitle('Сравнение семейства Themis с первыми 500 астероидами', fontsize=14, y=1.02)
#     plt.show()
    
# except FileNotFoundError:
#     print("Файл с первыми 500 астероидами не найден. Пропускаем сравнение.")

# # 5. Графики через seaborn (B-V, U-B, I-R, Albedo) - как в задании
# fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# # Проверяем доступные параметры
# available_params = []
# param_mapping = {
#     'B-V': ['BV', 'B-V', 'b_v', 'color_bv'],
#     'U-B': ['UB', 'U-B', 'u_b', 'color_ub'], 
#     'I-R': ['IR', 'I-R', 'i_r', 'color_ir'],
#     'Albedo': ['albedo', 'A', 'pV', 'pv']
# }

# # Определяем реальные названия параметров
# real_params = {}
# for display_name, possible_names in param_mapping.items():
#     for name in possible_names:
#         if name in df.columns and not df[name].isna().all():
#             real_params[display_name] = name
#             available_params.append(display_name)
#             break

# print(f"Доступные для построения параметры: {real_params}")

# # Строим графики для доступных параметров
# for i, (display_name, real_name) in enumerate(real_params.items()):
#     if i < 4:  # Максимум 4 графика
#         ax = axes[i//2, i%2]
#         plot_data = df.dropna(subset=[real_name])
        
#         if len(plot_data) > 0:
#             # Гистограмма с KDE через seaborn
#             sns.histplot(data=plot_data, x=real_name, hue='special', 
#                         palette=special_colors, alpha=0.7, 
#                         kde=True, ax=ax, bins=15)
            
#             ax.set_xlabel(display_name, fontsize=11)
#             ax.set_ylabel('Частота', fontsize=11)
#             ax.set_title(f'Распределение {display_name}', fontsize=12)
#             ax.legend(title='Тип астероида', title_fontsize=9, fontsize=8)
#             ax.grid(True, alpha=0.3)

# # Скрываем пустые subplots
# for i in range(len(available_params), 4):
#     axes[i//2, i%2].set_visible(False)

# plt.tight_layout()
# plt.suptitle('Фотометрические параметры семейства Themis', fontsize=14, y=1.02)
# plt.show()

# # 6. Дополнительные scatter plots с выделением особых астероидов
# fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# # a vs e
# sc1 = axes[0].scatter(df['a'], df['e'], 
#                      c=df['special'].map(special_colors), 
#                      alpha=0.8, s=30, edgecolors='black', linewidth=0.3)
# axes[0].set_xlabel('Большая полуось (a)', fontsize=11)
# axes[0].set_ylabel('Эксцентриситет (e)', fontsize=11)
# axes[0].set_title('a vs e', fontsize=12)
# axes[0].grid(True, alpha=0.3)

# # Создаем легенду
# legend_elements = [Patch(facecolor=color, label=label, alpha=0.8) 
#                   for label, color in special_colors.items()]
# axes[1].legend(handles=legend_elements, loc='center', fontsize=10)
# axes[1].axis('off')
# axes[1].set_title('Легенда', fontsize=12)

# plt.tight_layout()
# plt.show()

# # 7. Статистика по резонансам
# print("Анализ резонансов с Юпитером:")
# print("=" * 40)

# resonance_asteroids = []
# for name, position in resonance_positions.items():
#     if position >= df['a'].min() and position <= df['a'].max():
#         near_resonance = df[(df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)]
#         print(f"Резонанс {name} ({position:.3f} а.е.): {len(near_resonance)} астероидов")
        
#         if len(near_resonance) > 0:
#             special_in_resonance = near_resonance[near_resonance['special'] != 'Обычный']
#             if len(special_in_resonance) > 0:
#                 special_ids = ', '.join(special_in_resonance['pdes'].astype(str).tolist())
#                 print(f"  Особые астероиды: {special_ids}")

# # 8. Сохранение результатов
# df['resonance'] = 'Нет'
# for name, position in resonance_positions.items():
#     mask = (df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)
#     df.loc[mask, 'resonance'] = name

# df.to_csv('themis_family_analysis.csv', index=False)
# print(f"\nРезультаты сохранены в themis_family_analysis.csv")

# # 9. Итоговая статистика
# print(f"\nОбщая статистика семейства Themis:")
# print(f"Всего астероидов: {len(df)}")
# print(f"С диаметром >20 км: {len(df[df['diameter_category'] == '>20 км'])}")
# print(f"С диаметром 2-20 км: {len(df[df['diameter_category'] == '2-20 км'])}")
# print(f"С диаметром <2 км: {len(df[df['diameter_category'] == '<2 км'])}")
# print(f"Астероидов в резонансе: {len(df[df['resonance'] != 'Нет'])}")
# print(f"Родительское тело: {parent_body_id}")
# print(f"Указанные астероиды: {', '.join(specified_asteroids)}")


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

# 1. Гистограммы для всех параметров (точно как в задании)
parameters = ['spec_B', 'spec_T', 'a', 'e', 'i', 'q', 'H', 'rot_per']
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()

for i, param in enumerate(parameters):
    if param in df.columns and not df[param].isna().all():
        data = df[param].dropna()
        
        if len(data) > 0:
            axes[i].hist(data, bins=20, alpha=0.7, edgecolor='white', 
                        color='skyblue', linewidth=0.5)
            axes[i].set_xlabel(param, fontsize=10)
            axes[i].set_ylabel('Частота', fontsize=10)
            axes[i].set_title(f'Распределение {param}', fontsize=11)
            axes[i].grid(True, alpha=0.3)

# Убираем пустые subplots
for i in range(len(parameters), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.suptitle('Гистограммы параметров для всего семейства Themis', fontsize=14, y=1.02)
plt.show()

# 2. Гистограммы по категориям диаметра (точно по заданию)
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()

colors = {'<2 км': 'lightblue', '2-20 км': 'lightgreen', '>20 км': 'salmon'}

for i, param in enumerate(parameters):
    if param in df.columns:
        valid_data = False
        for category, color in colors.items():
            category_data = df[df['diameter_category'] == category][param].dropna()
            if len(category_data) > 0:
                axes[i].hist(category_data, bins=15, alpha=0.7, 
                           label=category, color=color, edgecolor='white', linewidth=0.5)
                valid_data = True
        
        if valid_data:
            axes[i].set_xlabel(param, fontsize=10)
            axes[i].set_ylabel('Частота', fontsize=10)
            axes[i].set_title(f'{param} по категориям диаметра', fontsize=11)
            axes[i].legend(fontsize=9)
            axes[i].grid(True, alpha=0.3)

# Убираем пустые subplots
for i in range(len(parameters), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.suptitle('Распределение параметров по категориям диаметра', fontsize=14, y=1.02)
plt.show()

# 3. Поиск резонансов с Юпитером (точно по заданию)
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

# Визуализация резонансов
plt.figure(figsize=(12, 6))
a_data = df['a'].dropna()

# Гистограмма большой полуоси
n, bins, patches = plt.hist(a_data, bins=30, alpha=0.7, edgecolor='white', 
                           color='lightsteelblue', linewidth=0.5)
plt.xlabel('Большая полуось (а.е.)', fontsize=12)
plt.ylabel('Количество астероидов', fontsize=12)
plt.title('Распределение большой полуоси с резонансами Юпитера', fontsize=13)

# Добавление линий резонансов
y_max = max(n) * 1.1
for name, position in resonance_positions.items():
    if position >= a_data.min() and position <= a_data.max():
        plt.axvline(x=position, color='red', linestyle='--', alpha=0.8, linewidth=1.5)
        plt.text(position, y_max * 0.9, f'{name}\n{position:.2f}', 
                ha='center', va='top', fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 4. Сравнение с первыми 500 астероидами (точно по заданию)
try:
    first_500 = pd.read_csv('sbdb_query_500.csv')  # Исправлено название файла
    first_500 = first_500.head(500)
    
    comparison_params = ['a', 'e', 'i', 'albedo']
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for i, param in enumerate(comparison_params):
        if param in df.columns and param in first_500.columns:
            family_data = df[param].dropna()
            first_500_data = first_500[param].dropna()
            
            if len(family_data) > 0 and len(first_500_data) > 0:
                # Логарифмическая шкала если семейство большое (>500)
                log_scale = len(df) >= 500
                
                # Общие границы для сравнения
                all_data = pd.concat([family_data, first_500_data])
                bins = np.linspace(all_data.min(), all_data.max(), 20)
                
                axes[i].hist(family_data, bins=bins, alpha=0.7, 
                           label=f'Семейство Themis (n={len(family_data)})', 
                           color='blue', edgecolor='white', linewidth=0.5, log=log_scale)
                axes[i].hist(first_500_data, bins=bins, alpha=0.7, 
                           label=f'Первые 500 астероидов (n={len(first_500_data)})', 
                           color='orange', edgecolor='white', linewidth=0.5, log=log_scale)
                
                axes[i].set_xlabel(param, fontsize=11)
                ylabel = 'Частота (лог)' if log_scale else 'Частота'
                axes[i].set_ylabel(ylabel, fontsize=11)
                axes[i].set_title(f'Сравнение {param}', fontsize=12)
                axes[i].legend(fontsize=9)
                axes[i].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.suptitle('Сравнение семейства Themis с первыми 500 астероидами', fontsize=14, y=1.02)
    plt.show()
    
except FileNotFoundError:
    print("Файл с первыми 500 астероидами не найден. Пропускаем сравнение.")

# 5. Графики через seaborn (B-V, U-B, I-R, Albedo) - как в задании
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Проверяем доступные параметры
available_params = []
param_mapping = {
    'B-V': ['BV', 'B-V', 'b_v', 'color_bv'],
    'U-B': ['UB', 'U-B', 'u_b', 'color_ub'], 
    'I-R': ['IR', 'I-R', 'i_r', 'color_ir'],
    'Albedo': ['albedo', 'A', 'pV', 'pv']
}

# Определяем реальные названия параметров
real_params = {}
for display_name, possible_names in param_mapping.items():
    for name in possible_names:
        if name in df.columns and not df[name].isna().all():
            real_params[display_name] = name
            available_params.append(display_name)
            break

print(f"Доступные для построения параметры: {real_params}")

# Строим графики для доступных параметров
for i, (display_name, real_name) in enumerate(real_params.items()):
    if i < 4:  # Максимум 4 графика
        ax = axes[i//2, i%2]
        plot_data = df.dropna(subset=[real_name])
        
        if len(plot_data) > 0:
            # Гистограмма с KDE через seaborn
            sns.histplot(data=plot_data, x=real_name, hue='special', 
                        palette=special_colors, alpha=0.7, 
                        kde=True, ax=ax, bins=15)
            
            ax.set_xlabel(display_name, fontsize=11)
            ax.set_ylabel('Частота', fontsize=11)
            ax.set_title(f'Распределение {display_name}', fontsize=12)
            ax.legend(title='Тип астероида', title_fontsize=9, fontsize=8)
            ax.grid(True, alpha=0.3)

# Скрываем пустые subplots
for i in range(len(available_params), 4):
    axes[i//2, i%2].set_visible(False)

plt.tight_layout()
plt.suptitle('Фотометрические параметры семейства Themis', fontsize=14, y=1.02)
plt.show()

# 6. ВОЗВРАЩЕННЫЕ SCATTER PLOTS (последние 3 графика как было)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# a vs e
scatter1 = axes[0, 0].scatter(df['a'], df['e'], 
                             c=df['special'].map(special_colors), 
                             alpha=0.7, s=40, edgecolors='black', linewidth=0.5)
axes[0, 0].set_xlabel('Большая полуось (a)', fontsize=11)
axes[0, 0].set_ylabel('Эксцентриситет (e)', fontsize=11)
axes[0, 0].set_title('a vs e с выделением особых астероидов', fontsize=12)
axes[0, 0].grid(True, alpha=0.3)

# i vs albedo
if 'albedo' in df.columns:
    scatter2 = axes[0, 1].scatter(df['i'], df['albedo'], 
                                 c=df['special'].map(special_colors), 
                                 alpha=0.7, s=40, edgecolors='black', linewidth=0.5)
    axes[0, 1].set_xlabel('Наклонение (i)', fontsize=11)
    axes[0, 1].set_ylabel('Альбедо', fontsize=11)
    axes[0, 1].set_title('i vs albedo', fontsize=12)
    axes[0, 1].grid(True, alpha=0.3)

# H vs diameter
scatter3 = axes[1, 0].scatter(df['H'], df['diameter'], 
                             c=df['special'].map(special_colors), 
                             alpha=0.7, s=40, edgecolors='black', linewidth=0.5)
axes[1, 0].set_xlabel('Абсолютная магнитуда (H)', fontsize=11)
axes[1, 0].set_ylabel('Диаметр', fontsize=11)
axes[1, 0].set_title('H vs diameter', fontsize=12)
axes[1, 0].grid(True, alpha=0.3)

# Создаем легенду для особых астероидов
legend_elements = [Patch(facecolor=color, label=label, alpha=0.7) 
                  for label, color in special_colors.items()]
axes[1, 1].legend(handles=legend_elements, loc='center', fontsize=11)
axes[1, 1].axis('off')
axes[1, 1].set_title('Легенда: особые астероиды', fontsize=12)

plt.tight_layout()
plt.show()

# 7. Статистика по резонансам
print("Анализ резонансов с Юпитером:")
print("=" * 40)

resonance_asteroids = []
for name, position in resonance_positions.items():
    if position >= df['a'].min() and position <= df['a'].max():
        near_resonance = df[(df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)]
        print(f"Резонанс {name} ({position:.3f} а.е.): {len(near_resonance)} астероидов")
        
        if len(near_resonance) > 0:
            special_in_resonance = near_resonance[near_resonance['special'] != 'Обычный']
            if len(special_in_resonance) > 0:
                special_ids = ', '.join(special_in_resonance['pdes'].astype(str).tolist())
                print(f"  Особые астероиды: {special_ids}")

# 8. Сохранение результатов
df['resonance'] = 'Нет'
for name, position in resonance_positions.items():
    mask = (df['a'] >= position - 0.1) & (df['a'] <= position + 0.1)
    df.loc[mask, 'resonance'] = name

df.to_csv('themis_family_analysis.csv', index=False)
print(f"\nРезультаты сохранены в themis_family_analysis.csv")

# 9. Итоговая статистика
print(f"\nОбщая статистика семейства Themis:")
print(f"Всего астероидов: {len(df)}")
print(f"С диаметром >20 км: {len(df[df['diameter_category'] == '>20 км'])}")
print(f"С диаметром 2-20 км: {len(df[df['diameter_category'] == '2-20 км'])}")
print(f"С диаметром <2 км: {len(df[df['diameter_category'] == '<2 км'])}")
print(f"Астероидов в резонансе: {len(df[df['resonance'] != 'Нет'])}")
print(f"Родительское тело: {parent_body_id}")
print(f"Указанные астероиды: {', '.join(specified_asteroids)}")