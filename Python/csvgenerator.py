import pandas as pd
import numpy as np
import random

# Настройки
NUM_ROWS = 1000
random.seed(42)
np.random.seed(42)

# Генерация базовых правильных данных
data = {
    'user_id': range(1, NUM_ROWS + 1),
    'age': np.random.randint(18, 80, size=NUM_ROWS),
    'income': np.random.randint(30000, 150000, size=NUM_ROWS),
    'account_status': np.random.choice(['active', 'inactive', 'banned'], size=NUM_ROWS)
}

df = pd.DataFrame(data)

# --- ВНЕДРЕНИЕ "ЛОВУШЕК" ---

# 1. Ловушка с Null в возрасте (спровоцирует мутацию int -> float)
# В Pandas это все еще происходит автоматически для NaN
null_age_indices = random.sample(range(NUM_ROWS), 50)
df.loc[null_age_indices, 'age'] = np.nan

# --- ИСПРАВЛЕНИЕ ДЛЯ СОВРЕМЕННОГО PANDAS ---
# Явно переводим колонку income в тип object, чтобы иметь возможность вставить туда строки
df['income'] = df['income'].astype(object) 
# -------------------------------------------

# 2. Ловушка с типами в доходе
string_income_indices = random.sample(range(NUM_ROWS), 30)
for idx in string_income_indices:
    df.loc[idx, 'income'] = f"{df.loc[idx, 'income']}$"
df.loc[random.sample(range(NUM_ROWS), 10), 'income'] = "N/A"

# 3. Ловушка с опечатками в категориях
typo_indices = random.sample(range(NUM_ROWS), 20)
typos = ['activ', 'in_active', 'UNKNOWN', '']
for idx in typo_indices:
    df.loc[idx, 'account_status'] = random.choice(typos)

# 4. Ловушка с отрицательными числами (нарушение бизнес-логики)
negative_income_indices = random.sample(range(NUM_ROWS), 5)
df.loc[negative_income_indices, 'income'] = -500

# Перемешаем строки
df = df.sample(frac=1).reset_index(drop=True)

# Сохраняем в CSV
df.to_csv('dirty_dataset.csv', index=False)
print("Файл dirty_dataset.csv успешно сгенерирован!")
