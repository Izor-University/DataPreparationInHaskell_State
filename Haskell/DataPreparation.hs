import Text.Read (readMaybe)

-- 1. Наши строгие типы данных
data AccountStatus = Active | Inactive | Banned deriving (Show, Eq)

data UserProfile = UserProfile
  { userId :: Int
  , age    :: Maybe Int -- Пустые ячейки (NaN) легально станут Nothing
  , income :: Int       -- Строго целое число
  , status :: AccountStatus
  } deriving (Show)

-- 2. Логика строгого парсинга (сердце нашего конвейера)
-- Возвращает либо текст ошибки (Left), либо чистый профиль (Right)
parseRow :: String -> Either String UserProfile
parseRow line = case splitByComma line of
    [uidStr, ageStr, incStr, statStr] -> do
        uid  <- parseStrictInt "user_id" uidStr
        -- readMaybe превратит "25" в Just 25, а пустую строку или "NaN" в Nothing
        let parsedAge = readMaybe ageStr 
        inc  <- parseStrictInt "income" incStr
        stat <- parseStatus statStr
        return $ UserProfile uid parsedAge inc stat
    _ -> Left "Критическая ошибка: неверное количество колонок в строке"

-- Вспомогательная функция для безопасного чтения чисел
parseStrictInt :: String -> String -> Either String Int
parseStrictInt fieldName val = case readMaybe val of
    Just n  -> Right n
    Nothing -> Left $ "Ошибка типизации (ожидалось число) в поле " ++ fieldName ++ ": '" ++ val ++ "'"

-- Вспомогательная функция для валидации статуса (ADT)
parseStatus :: String -> Either String AccountStatus
parseStatus "active"   = Right Active
parseStatus "inactive" = Right Inactive
parseStatus "banned"   = Right Banned
parseStatus err        = Left $ "Неизвестный или сломанный статус аккаунта: '" ++ err ++ "'"

-- Простейший разделитель строк по запятым
splitByComma :: String -> [String]
splitByComma "" = [""]
splitByComma s =
  let (word, rest) = break (== ',') s
  in word : case rest of
              []     -> []
              (_:xs) -> splitByComma xs

-- 3. Запуск конвейера
main :: IO ()
main = do
    csvData <- readFile "../Python/dirty_dataset.csv"
    let (header:rows) = lines csvData -- Пропускаем строку с заголовками
    let results = map parseRow rows

    -- Разделяем результаты на успешные и ошибочные
    let successes = [profile | Right profile <- results]
    let errors    = [err     | Left err      <- results]

    putStrLn "=== Отчет о типобезопасной обработке (Haskell) ==="
    putStrLn $ "Успешно распарсено абсолютно чистых строк: " ++ show (length successes)
    putStrLn $ "Отловлено ошибок структуры на этапе парсинга: " ++ show (length errors)
    
    putStrLn "\n--- Пример лога отловленных ошибок (первые 5) ---"
    mapM_ putStrLn (take 5 errors)
