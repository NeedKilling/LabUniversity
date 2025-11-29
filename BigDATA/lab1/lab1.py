import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('filtered_sbdb_data.csv')
df500 = pd.read_csv('sbdb_query_500.csv')


def createCountsObj(data):
    obj = {}
    for item in data:
        if item in obj:
            obj[item] += 1
        else:
            obj[item] = 1

    x = [item[0] for item in obj.items()]
    y = [item[1] for item in obj.items()]
    plt.bar(x,y, edgecolor='black', alpha=0.7)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

plt.figure(figsize=(17, 8))

# График 1: spec_B
plt.subplot(2, 4, 1)
createCountsObj(df.dropna(subset=['spec_B'])['spec_B'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Спектральные классы (spec_B)')
plt.grid(True, alpha=0.3)

# График 2: spec_T
plt.subplot(2, 4, 2)
createCountsObj(df.dropna(subset=['spec_T'])['spec_T'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Спектральные классы (spec_T)')
plt.grid(True, alpha=0.3)

# График 3: большая полуось (a)
plt.subplot(2, 4, 3)
plt.hist(df["a"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Большая полуось орбиты (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('Распределение большой полуоси (a)')

# График 4: эксцентриситет (e)
plt.subplot(2, 4, 4)
plt.hist(df["e"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Эксцентриситет орбиты')
plt.ylabel('Количество астероидов')
plt.title('Распределение эксцентриситета (e)')

# График 5: наклонение (i)
plt.subplot(2, 4, 5)
plt.hist(df["i"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Наклонение орбиты (градусы)')
plt.ylabel('Количество астероидов')
plt.title('Распределение наклонения (i)')

# График 6: Перигелий
plt.subplot(2, 4, 6)
plt.hist(df["q"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Перигелий (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('Распределение перигелия (q)')

# График 7: Абсолютная величина
plt.subplot(2, 4, 7)
plt.hist(df["H"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Абсолютная величина')
plt.ylabel('Количество астероидов')
plt.title('Распределение абсолютной величины (H)')

# График 8: Период вращения
plt.subplot(2, 4, 8)
plt.hist(df["rot_per"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Период вращения (часы)')
plt.ylabel('Количество астероидов')
plt.title('Распределение периодов вращения (rot_per)')

plt.tight_layout()
plt.show()

rot_per_data = df['rot_per'].dropna()
asteroids500 = rot_per_data[(rot_per_data >= 0) & (rot_per_data <= 500)]
asteroids_outside = rot_per_data[rot_per_data > 500]
print(f"Всего астероидов с данными о вращении: {len(rot_per_data)}")
print(f"Астероидов от 0 до 500 часов: {len(asteroids500)}")
print(f"Астероидов более 500 часов: {len(asteroids_outside)}")


large_asteroids = df[df['diameter'] > 20]
medium_asteroids = df[(df['diameter'] >= 2) & (df['diameter'] <= 20)]
small_asteroids = df[df['diameter'] < 2]

# def createObj(data):
#     obj = {}
#     for item in data:
#         if item in obj:
#             obj[item] += 1
#         else:
#             obj[item] = 1

#     x = [item[0] for item in obj.items()]
#     y = [item[1] for item in obj.items()]
#     return obj
# print(createObj(df["rot_per"].dropna()))





print("Анализ данных по группам:")
for col in ['spec_B', 'spec_T', 'a', 'e', 'i', 'q', 'H', 'rot_per']:
    print(f"\n{col}: {len(df[col].dropna())}")
    for size_group, label in zip([large_asteroids, medium_asteroids,small_asteroids], 
                                ['>20 км', '2-20 км', '2 км']):
        available_data = size_group[col].dropna()
        print(f"  {label}: {len(available_data)} записей")




























plt.figure(figsize=(17, 8))

# График 1: spec_B
plt.subplot(2, 4, 1)
createCountsObj(df.dropna(subset=['spec_B'])['spec_B'])

createCountsObj(large_asteroids.dropna(subset=['spec_B'])['spec_B'])
createCountsObj(medium_asteroids.dropna(subset=['spec_B'])['spec_B'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Spec_B (оранжевый>20км, синий=2-20км)')
plt.grid(True, alpha=0.3)

# График 2: spec_T
plt.subplot(2, 4, 2)
createCountsObj(df.dropna(subset=['spec_T'])['spec_T'])
createCountsObj(large_asteroids.dropna(subset=['spec_T'])['spec_T'])
createCountsObj(medium_asteroids.dropna(subset=['spec_T'])['spec_T'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Spec_T (оранжевый>20км, синий=2-20км)')
plt.grid(True, alpha=0.3)

# График 3: большая полуось (a)
plt.subplot(2, 4, 3)
plt.hist(df["a"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["a"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["a"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Большая полуось орбиты (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('a (красный>20км, синий=2-20км)')

# График 4: эксцентриситет (e)
plt.subplot(2, 4, 4)
plt.hist(df["e"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["e"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["e"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Эксцентриситет орбиты')
plt.ylabel('Количество астероидов')
plt.title('e (красный>20км, синий=2-20км)')

# График 5: наклонение (i)
plt.subplot(2, 4, 5)
plt.hist(df["i"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["i"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["i"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Наклонение орбиты (градусы)')
plt.ylabel('Количество астероидов')
plt.title('i (красный>20км, синий=2-20км)')

# График 6: Перигелий (q)
plt.subplot(2, 4, 6)
plt.hist(df["q"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["q"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["q"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Перигелий (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('q (красный>20км, синий=2-20км)')

# График 7: Абсолютная величина (H)
plt.subplot(2, 4, 7)
plt.hist(df["H"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["H"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["H"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Абсолютная величина')
plt.ylabel('Количество астероидов')
plt.title('H (красный>20км, синий=2-20км)')

#График 8: Период вращения (rot_per)
plt.subplot(2, 4, 8)
plt.hist(df["rot_per"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["rot_per"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["rot_per"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Период вращения (часы)')
plt.ylabel('Количество астероидов')
plt.title('rot_per (красный>20км, синий=2-20км)')


parent_body = 24 
special_asteroids = [62, 90, 171, 222] 

parent_data = df[df['pdes'] == parent_body]
special_data = df[df['pdes'].isin(special_asteroids)]

columns_for_plots = ['spec_B','spec_T','a', 'e', 'i', 'q', 'H', 'rot_per']
plot_numbers = [1, 2, 3, 4, 5, 6, 7, 8]

for plot_num, col in zip(plot_numbers, columns_for_plots):
    plt.subplot(2, 4, plot_num)
    parent_added = False
    if len(parent_data) > 0 and not pd.isna(parent_data[col].iloc[0]):
        plt.axvline(x=parent_data[col].iloc[0], color='green', linewidth=2, label='Родительское тело', alpha = 0.6)
        parent_added = True
    special_added = False
    for i, asteroid in special_data.iterrows():
        if not pd.isna(asteroid[col]):
            if not special_added:
                plt.axvline(x=asteroid[col], color='orange', linewidth=2, linestyle='--', label='Особые астероиды', alpha = 0.6)
                special_added = True
            else:
                plt.axvline(x=asteroid[col], color='orange', linewidth=2, linestyle='--', alpha = 0.6)


plt.legend()
plt.tight_layout()
plt.show()











































plt.figure(figsize=(10, 6))
plt.hist(df["a"].dropna(), bins="auto", edgecolor='black', alpha=0.7)

jupiter = 5.204
themis_resonances = {
    '2:1': jupiter / (2/1)**(2/3),  
    '7:4': jupiter / (7/4)**(2/3),  
    '5:3': jupiter / (5/3)**(2/3),  
}

for resonance, a_value in themis_resonances.items():
    plt.axvline(x=a_value, color='red', linestyle='--', linewidth=2, 
               label=f'Резонанс {resonance}')
    plt.text(a_value, plt.ylim()[1]*0.9, f'{resonance}\n          ', 
            rotation=90, verticalalignment='top', ha='center', fontweight='bold')

plt.xlabel('Большая полуось орбиты (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('Семейство Themis: резонансы с Юпитером')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


























# plt.figure(figsize=(12, 8))

# parameters = ['a', 'e', 'i', 'albedo']
# titles = ['Большая полуось (a)', 'Эксцентриситет (e)', 'Наклонение (i)', 'Альбедо']

# for i, (param, title) in enumerate(zip(parameters, titles), 1):
#     plt.subplot(2, 2, i)
    
#     # Гистограммы
#     plt.hist(df[param].dropna(), bins=30, alpha=0.6, color='blue', 
#              label='Семейство Themis', edgecolor='black')
#     plt.hist(df500[param].dropna(), bins=30, alpha=0.6, color='red', 
#              label='Первые 500', edgecolor='black')
    
#     # Логарифмическая шкала
#     plt.yscale('log')
    
#     # Просто линии без легенды (чтобы не загромождать)
#     if len(parent_data) > 0 and not pd.isna(parent_data[param].iloc[0]):
#         plt.axvline(x=parent_data[param].iloc[0], color='green', linewidth=3)
    
#     for _, asteroid in special_data.iterrows():
#         if not pd.isna(asteroid[param]):
#             plt.axvline(x=asteroid[param], color='orange', linewidth=2, linestyle='--')
    
#     plt.xlabel(param)
#     plt.ylabel('Количество (лог. шкала)')
#     plt.title(title)
#     plt.grid(True, alpha=0.3)
    
#     # Общая легенда только на первом графике
#     if i == 1:
#         plt.legend()

# plt.tight_layout()
# plt.show()






















plt.figure(figsize=(17, 8))

# График 1: большая полуось (a)
plt.subplot(2, 2, 1)
plt.hist(df["a"].dropna(),  alpha=0.7, bins="auto", color='gray')
plt.hist(df500["a"].dropna(),  alpha=0.3, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Большая полуось (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('a (серый=Themis, красный=500)')
plt.yscale('log')

# График 2: эксцентриситет (e)
plt.subplot(2, 2, 2)
plt.hist(df["e"].dropna(),  alpha=0.7, bins="auto", color='gray')
plt.hist(df500["e"].dropna(),  alpha=0.3, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Эксцентриситет')
plt.ylabel('Количество астероидов')
plt.title('e (серый=Themis, красный=500)')
plt.yscale('log')

# График 3: наклонение (i)
plt.subplot(2, 2, 3)
plt.hist(df["i"].dropna(),  alpha=0.7, bins="auto", color='gray')
plt.hist(df500["i"].dropna(),  alpha=0.3, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Наклонение (градусы)')
plt.ylabel('Количество астероидов')
plt.title('i (серый=Themis, красный=500)')
plt.yscale('log')

# График 4: альбедо
plt.subplot(2, 2, 4)
plt.hist(df["albedo"].dropna(),  alpha=0.7, bins="auto", color='gray')
plt.hist(df500["albedo"].dropna(),  alpha=0.3, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Альбедо')
plt.ylabel('Количество астероидов')
plt.title('albedo (серый=Themis, красный=500)')
plt.yscale('log')

# БЛОК ВЫДЕЛЕНИЯ ОСОБЫХ АСТЕРОИДОВ
parent_body = 24 
special_asteroids = [62, 90, 171, 222] 

parent_data = df[df['pdes'] == parent_body]
special_data = df[df['pdes'].isin(special_asteroids)]

columns_for_plots = ['a', 'e', 'i', 'albedo']
plot_numbers = [1, 2, 3, 4]

for plot_num, col in zip(plot_numbers, columns_for_plots):
    plt.subplot(2, 2, plot_num)
    
    parent_added = False
    if len(parent_data) > 0 and not pd.isna(parent_data[col].iloc[0]):
        plt.axvline(x=parent_data[col].iloc[0], color='green', linewidth=2, label='Родительское тело', alpha=0.6)
        parent_added = True
    
    special_added = False
    for i, asteroid in special_data.iterrows():
        if not pd.isna(asteroid[col]):
            if not special_added:
                plt.axvline(x=asteroid[col], color='orange', linewidth=2, linestyle='--', label='Особые астероиды', alpha=0.6)
                special_added = True
            else:
                plt.axvline(x=asteroid[col], color='orange', linewidth=2, linestyle='--', alpha=0.6)
        
plt.legend()
plt.tight_layout()
plt.show()