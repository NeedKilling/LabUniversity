import pandas as pd
import numpy as np

themis_data = pd.read_csv('602_themis.tab', delim_whitespace=True, 
                         names=['ID', 'a', 'e', 'sin_i', 'H', 'C_PARAM', 'family_num', 'parent_num', 'parent_name'])

themis_ids = themis_data['ID'].astype(str).tolist()
print(f"Найдено {len(themis_ids)} ID в файле themis.tab")
sbdb_data = pd.read_csv('sbdb_query_results.csv')

sbdb_data['pdes'] = sbdb_data['pdes'].astype(str)

filtered_data = sbdb_data[sbdb_data['pdes'].isin(themis_ids)]

print(f"Найдено {len(filtered_data)} совпадений из {len(themis_ids)} возможных")
print("\nОтфильтрованные данные:")
print(filtered_data)
# Сохраняем в новый CSV файл 
# filtered_data.to_csv('filtered_sbdb_data.csv', index=False)
# print("\nРезультат сохранен в filtered_sbdb_data.csv")
missing_ids = set(themis_ids) - set(filtered_data['pdes'].astype(str).tolist())
if missing_ids:
    print(f"\nНе найдены следующие ID: {missing_ids}")
else:
    print("\nВсе ID найдены успешно!")

