# Информационная система
### Информационная система «Страховые компании», использующая роли, защиту на уровне строк, триггеры, домены, индексы, функции, представления и партицирование.
  Экранные формы для нескольких ролей пользователей. На стороне сервера предусмотрена защиту на уровне строк, используются роли и политики защиты. Созданы индексы, домены, разработаны триггеры, выполнено партицирование одной из основных таблиц. 
  SQL запросы к базе данных реализованы в виде представлений и функций, создано модифицируемое представление, используя механизм триггеров, и визуализирован результат запроса в Excel.

  В качестве языка программирования для написания информационной системы был выбран Python. Данный язык был выбран по ряду преимуществ, среди которых следует выделить совместимость с огромным количеством БД, высокую производительность, наличие динамической типизации данных, высокую читаемость итоговой кодификации и наличие множества библиотек.
  Для разработки пользовательского графического интерфейса был выбран набор расширений графического фреймворка Qt для Python – PyQt5. Для взаимодействия с СУБД используется самый популярный адаптер для  PostgreSQL – Navicat, он обеспечивает доступ ко многим функциям СУБД. Чтобы генерировать Excel файлы с диаграммами был выбран Python модуль xlsxwriter.