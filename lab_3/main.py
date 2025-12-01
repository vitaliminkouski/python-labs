import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# Загрузка данных
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"

# Стандартные имена столбцов согласно документации UCI German Credit Data
column_names = [
    "checking_account", "duration", "credit_history", "purpose", "credit_amount",
    "savings_account", "employment", "installment_rate", "personal_status", "debtors",
    "residence_since", "property", "age", "other_installments", "housing",
    "existing_credits", "job", "liable_people", "telephone", "foreign_worker", "risk"
]

try:
    # Загружаем данные
    df = pd.read_csv(url, sep=' ', header=None, names=column_names)
    print("✅ Данные успешно загружены!")
except Exception as e:
    print(f"❌ Ошибка при загрузке данных: {e}")

# Обработка пропущенных значений
missing_values = df.isnull().sum()
print("\n--- Проверка пропущенных значений ---")
if missing_values.sum() == 0:
    print("Пропущенных значений (NaN) не обнаружено.")
else:
    print("Найдены пропущенные значения:")
    print(missing_values[missing_values > 0])

# Обзор данных
print("\n--- Информация о датасете ---")
print(df.info())

print("\n--- Первые 5 строк данных ---")
pd.set_option('display.max_columns', None)
print(df.head())

df['risk'] = df['risk'].map({1: 1, 2: 0})
print("\nПримечание: Целевая переменная 'risk' преобразована: 1 = Good (кредит вернут), 0 = Bad (проблемы).")

# Анализ числовых признаков
print("\n=== Статистика по числовым признакам ===")
numeric_cols = ['duration', 'credit_amount', 'installment_rate', 'residence_since', 'age', 'existing_credits', 'liable_people']
print(df[numeric_cols].describe().round(2))

# Анализ категориальных признаков
print("\n=== Распределение ключевых категорий ===")
for col in ['purpose', 'credit_history', 'housing']:
    print(f"\n--- {col} (Топ-5 значений) ---")
    print(df[col].value_counts().head(5))

# Кодирование категориальных признаков
df_encoded = df.copy()
categorical_columns = df.select_dtypes(include=['object']).columns
label_encoders = {}

print("\n=== Кодирование категорий (Label Encoding) ===")
for col in categorical_columns:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"Столбец '{col}' закодирован. Пример: {le.classes_[:3]} -> [0, 1, 2]")

print("\n--- Проверка результата кодирования (первые 3 строки) ---")
print(df_encoded.head(3))


# Визуализация
# Настройка стиля
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("\n=== Генерация и сохранение графиков ===")

# Создание папки charts
output_folder = "charts"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"📁 Папка '{output_folder}' создана.")
else:
    print(f"📁 Папка '{output_folder}' уже существует.")

# Тепловая карта
plt.figure(figsize=(12, 8))
corr_matrix = df_encoded.corr()
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
plt.title('Матрица корреляции')
plt.tight_layout()

# Сохраняем в папку charts
save_path_1 = os.path.join(output_folder, 'plot_1_heatmap.png')
plt.savefig(save_path_1)
print(f" График сохранен: {save_path_1}")
plt.close()

# Гистограммы
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.histplot(df['age'], bins=20, kde=True, ax=axes[0], color='skyblue')
axes[0].set_title('Распределение возраста')
sns.histplot(df['credit_amount'], bins=20, kde=True, ax=axes[1], color='salmon')
axes[1].set_title('Распределение суммы кредита')
plt.tight_layout()

# Сохраняем в папку charts
save_path_2 = os.path.join(output_folder, 'plot_2_histograms.png')
plt.savefig(save_path_2)
print(f"✅ График сохранен: {save_path_2}")
plt.close()

# Boxplot
plt.figure(figsize=(14, 7))
sns.boxplot(x='purpose', y='credit_amount', data=df, hue='purpose', palette='Set3', legend=False)
plt.title('Разброс суммы кредита по целям')
plt.xticks(rotation=45)
plt.tight_layout()

# Сохраняем в папку charts
save_path_3 = os.path.join(output_folder, 'plot_3_boxplot.png')
plt.savefig(save_path_3)
print(f"✅ График сохранен: {save_path_3}")
plt.close()

print(f"Визуализация завершена. Проверьте папку '{output_folder}' в проекте.")

# Работа с БД
db_name = "german_credit.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

print(f" База данных '{db_name}' создана и подключение установлено.")

try:
    df.to_sql('credits', conn, if_exists='replace', index=False)
    print(" Данные успешно загружены в таблицу 'credits'.")
except Exception as e:
    print(f" Ошибка при записи в БД: {e}")


def run_query(query, title):
    print(f"\n--- {title} ---")
    print(f"SQL: {query}")
    result = pd.read_sql(query, conn)
    print(result)
    return result


# Запрос 1
query_1 = """
SELECT purpose, duration, credit_amount, age
FROM credits
WHERE risk = 0 AND duration > 24
ORDER BY credit_amount DESC
LIMIT 5;
"""
run_query(query_1, "Топ-5 крупных 'плохих' кредитов (>24 мес)")

# Запрос 2
query_2 = """
SELECT 
    purpose, 
    COUNT(*) as count_loans,
    ROUND(AVG(credit_amount), 2) as avg_amount,
    MAX(age) as max_age
FROM credits
GROUP BY purpose
ORDER BY avg_amount DESC;
"""
run_query(query_2, "Статистика по целям кредита (Средняя сумма и Макс. возраст)")

# Запрос 3
query_3 = """
SELECT 
    housing,
    COUNT(*) as total_clients,
    SUM(CASE WHEN risk = 0 THEN 1 ELSE 0 END) as bad_loans,
    ROUND(AVG(risk) * 100, 1) as good_loans_percent
FROM credits
GROUP BY housing
ORDER BY good_loans_percent DESC;
"""
run_query(query_3, "Процент возврата кредитов в зависимости от типа жилья")

conn.close()
print("\n Работа с базой данных завершена, соединение закрыто.")