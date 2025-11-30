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
plt.subplot(2, 4, 1)
createCountsObj(df.dropna(subset=['spec_B'])['spec_B'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Спектральные классы (spec_B)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 4, 2)
createCountsObj(df.dropna(subset=['spec_T'])['spec_T'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Спектральные классы (spec_T)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 4, 3)
plt.hist(df["a"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Большая полуось орбиты (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('Распределение большой полуоси (a)')

plt.subplot(2, 4, 4)
plt.hist(df["e"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Эксцентриситет орбиты')
plt.ylabel('Количество астероидов')
plt.title('Распределение эксцентриситета (e)')

plt.subplot(2, 4, 5)
plt.hist(df["i"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Наклонение орбиты (градусы)')
plt.ylabel('Количество астероидов')
plt.title('Распределение наклонения (i)')

plt.subplot(2, 4, 6)
plt.hist(df["q"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Перигелий (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('Распределение перигелия (q)')

plt.subplot(2, 4, 7)
plt.hist(df["H"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Абсолютная величина')
plt.ylabel('Количество астероидов')
plt.title('Распределение абсолютной величины (H)')

plt.subplot(2, 4, 8)
plt.hist(df["rot_per"].dropna(), edgecolor='black', alpha=0.7, bins="auto")
plt.grid(True, alpha=0.3)
plt.xlabel('Период вращения (часы)')
plt.ylabel('Количество астероидов')
plt.title('Распределение периодов вращения (rot_per)')

plt.tight_layout()
plt.show()


large_asteroids = df[df['diameter'] > 20]
medium_asteroids = df[(df['diameter'] >= 2) & (df['diameter'] <= 20)]

plt.figure(figsize=(17, 8))

plt.subplot(2, 4, 1)
createCountsObj(df.dropna(subset=['spec_B'])['spec_B'])

createCountsObj(large_asteroids.dropna(subset=['spec_B'])['spec_B'])
createCountsObj(medium_asteroids.dropna(subset=['spec_B'])['spec_B'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Spec_B (оранжевый>20км, синий=2-20км)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 4, 2)
createCountsObj(df.dropna(subset=['spec_T'])['spec_T'])
createCountsObj(large_asteroids.dropna(subset=['spec_T'])['spec_T'])
createCountsObj(medium_asteroids.dropna(subset=['spec_T'])['spec_T'])
plt.xlabel('Спектральный класс')
plt.ylabel('Количество астероидов')
plt.title('Spec_T (оранжевый>20км, синий=2-20км)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 4, 3)
plt.hist(df["a"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["a"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["a"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Большая полуось орбиты (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('a')

plt.subplot(2, 4, 4)
plt.hist(df["e"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["e"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["e"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Эксцентриситет орбиты')
plt.ylabel('Количество астероидов')
plt.title('e')

plt.subplot(2, 4, 5)
plt.hist(df["i"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["i"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["i"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Наклонение орбиты (градусы)')
plt.ylabel('Количество астероидов')
plt.title('i')

plt.subplot(2, 4, 6)
plt.hist(df["q"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["q"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["q"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Перигелий (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('q')

plt.subplot(2, 4, 7)
plt.hist(df["H"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray')
plt.hist(medium_asteroids["H"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue')
plt.hist(large_asteroids["H"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Абсолютная величина')
plt.ylabel('Количество астероидов')
plt.title('H')

plt.subplot(2, 4, 8)
plt.hist(df["rot_per"].dropna(), edgecolor='black', alpha=0.3, bins="auto", color='gray',label='Themis')
plt.hist(medium_asteroids["rot_per"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='blue',label='2-20km')
plt.hist(large_asteroids["rot_per"].dropna(), edgecolor='black', alpha=0.7, bins="auto", color='red',label='>20km')
plt.grid(True, alpha=0.3)
plt.xlabel('Период вращения (часы)')
plt.ylabel('Количество астероидов')
plt.title('rot_per')

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





plt.figure(figsize=(17, 8))
plt.subplot(2, 2, 1)
plt.hist(df["a"].dropna(),  alpha=0.7, bins="auto", color='gray')
plt.hist(df500["a"].dropna(),  alpha=0.3, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Большая полуось (а.е.)')
plt.ylabel('Количество астероидов')
plt.title('a')
plt.yscale('log')

plt.subplot(2, 2, 2)
plt.hist(df["e"].dropna(),  alpha=0.7, bins="auto", color='gray')
plt.hist(df500["e"].dropna(),  alpha=0.3, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Эксцентриситет')
plt.ylabel('Количество астероидов')
plt.title('e')
plt.yscale('log')

plt.subplot(2, 2, 3)
plt.hist(df["i"].dropna(),  alpha=0.7, bins="auto", color='gray')
plt.hist(df500["i"].dropna(),  alpha=0.3, bins="auto", color='red')
plt.grid(True, alpha=0.3)
plt.xlabel('Наклонение (градусы)')
plt.ylabel('Количество астероидов')
plt.title('i')
plt.yscale('log')

plt.subplot(2, 2, 4)
plt.hist(df["albedo"].dropna(),  alpha=0.7, bins="auto", color='gray',label='Themis')
plt.hist(df500["albedo"].dropna(),  alpha=0.3, bins="auto", color='red',label='500')
plt.grid(True, alpha=0.3)
plt.xlabel('Альбедо')
plt.ylabel('Количество астероидов')
plt.title('albedo')
plt.yscale('log')

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



df['group'] = 'Остальные'
df.loc[df['pdes'] == 24, 'group'] = 'Родительское тело'
df.loc[df['pdes'].isin(special_asteroids), 'group'] = 'Особые астероиды'
params_for_plot = ['BV', 'UB', 'albedo']
sns.pairplot(df[params_for_plot + ['group']].dropna(), hue='group')
plt.show()

