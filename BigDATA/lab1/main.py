import pandas as pd
import numpy as np

# Чтение данных из файла 602_themis.tab
# Предполагаем, что файл имеет формат с пробелами в качестве разделителей
themis_data = pd.read_csv('602_themis.tab', delim_whitespace=True, 
                         names=['ID', 'a', 'e', 'sin_i', 'H', 'C_PARAM', 'family_num', 'parent_num', 'parent_name'])

# Получаем список ID астероидов из файла themis
themis_ids = themis_data['ID'].astype(str).tolist()
print(f"Найдено {len(themis_ids)} ID в файле themis.tab")

# Чтение данных из CSV файла
sbdb_data = pd.read_csv('sbdb_query_results.csv')

# Преобразуем pdes к строковому типу для сравнения
sbdb_data['pdes'] = sbdb_data['pdes'].astype(str)

# Фильтруем данные, оставляя только строки с pdes из themis_ids
filtered_data = sbdb_data[sbdb_data['pdes'].isin(themis_ids)]

print(f"Найдено {len(filtered_data)} совпадений из {len(themis_ids)} возможных")

# Выводим результат
print("\nОтфильтрованные данные:")
print(filtered_data)

# Сохраняем результат в новый CSV файл (опционально)
filtered_data.to_csv('filtered_sbdb_data.csv', index=False)
print("\nРезультат сохранен в filtered_sbdb_data.csv")

# Дополнительно: покажем, какие ID не были найдены
missing_ids = set(themis_ids) - set(filtered_data['pdes'].astype(str).tolist())
if missing_ids:
    print(f"\nНе найдены следующие ID: {missing_ids}")
else:
    print("\nВсе ID найдены успешно!")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# import pandas as pd
# import numpy as np

# # Чтение данных из файла 602_themis.tab
# themis_data = pd.read_csv('602_themis.tab', delim_whitespace=True, 
#                          names=['ID', 'a_themis', 'e_themis', 'sin_i_themis', 
#                                 'H_themis', 'C_PARAM', 'family_num', 'parent_num', 'parent_name'])

# # Чтение данных из CSV файла
# sbdb_data = pd.read_csv('sbdb_query_results.csv')

# # Преобразуем ID к строковому типу для сравнения
# themis_data['ID'] = themis_data['ID'].astype(str)
# sbdb_data['pdes'] = sbdb_data['pdes'].astype(str)

# # Объединяем данные по ID
# merged_data = pd.merge(themis_data, sbdb_data, 
#                       left_on='ID', right_on='pdes', 
#                       how='left')

# print(f"Объединено {merged_data['pdes'].notna().sum()} записей из {len(themis_data)}")

# # Выводим результат
# print("\nОбъединенные данные:")
# print(merged_data.head())

# # Сохраняем результат в новый CSV файл
# merged_data.to_csv('merged_asteroid_data.csv', index=False)
# print("\nРезультат сохранен в merged_asteroid_data.csv")

# # Покажем информацию о объединенных данных
# print("\nИнформация о данных:")
# print(merged_data.info())

# # Покажем, какие ID не были найдены в sbdb_data
# missing_ids = merged_data[merged_data['pdes'].isna()]['ID'].tolist()
# if missing_ids:
#     print(f"\nНе найдены данные для следующих ID: {missing_ids}")
# else:
#     print("\nВсе ID найдены успешно!")