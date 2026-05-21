import pandas as pd

def process_data(file_path):
    print("Загрузка данных...")
    df = pd.read_csv(file_path)
    
    # 1. Обработка пропусков в возрасте
    df['age'] = df['age'].fillna(df['age'].median())
    
    # 2. Очистка дохода
    # УЯЗВИМОСТЬ: errors='coerce' тихо превратит все строки со знаком $ в NaN
    df['income'] = pd.to_numeric(df['income'], errors='coerce')
    
    # 3. Фильтрация статуса
    valid_statuses = ['active', 'inactive', 'banned']
    df = df[df['account_status'].isin(valid_statuses)]
    
    # 4. Удаление оставшегося мусора
    # УЯЗВИМОСТЬ: Мы удаляем строки вслепую, теряя данные и не зная причины
    initial_rows = len(df)
    df = df.dropna()
    final_rows = len(df)
    
    print(f"Очистка завершена. Потеряно строк: {initial_rows - final_rows}")
    return df
cleaned_df = process_data('dirty_dataset.csv')
