# Information system

### Information system "Insurance companies" uses roles, row-level protection, triggers, domains, indexes, functions, views and partitioning.
Screen forms for multiple user roles. On the server side, row-level protection is provided, roles and protection policies are used. Indexes and domains were created, triggers were developed, partitioning of one of the main tables was performed.
SQL queries to the database are implemented in the form of views and functions, a modified view is created using the trigger mechanism, and the query result is visualized in Excel.
Python was chosen as the programming language for writing the information system. This language was chosen for a number of advantages, including compatibility with a huge number of databases, high performance, dynamic data typing, high readability of the final codification and the presence of many libraries.
To develop a custom graphical interface, a set of extensions to the Qt graphical framework for Python was chosen – PyQt5. To interact with the DBMS, the most popular adapter for PostgreSQL, Navicat, is used; it provides access to many DBMS functions. To generate Excel files with diagrams, the xlsxwriter Python module was chosen.

### Информационная система «Страховые компании», использующая роли, защиту на уровне строк, триггеры, домены, индексы, функции, представления и партицирование.
Экранные формы для нескольких ролей пользователей. На стороне сервера предусмотрена защиту на уровне строк, используются роли и политики защиты. Созданы индексы, домены, разработаны триггеры, выполнено партицирование одной из основных таблиц. 
SQL запросы к базе данных реализованы в виде представлений и функций, создано модифицируемое представление, используя механизм триггеров, и визуализирован результат запроса в Excel.
В качестве языка программирования для написания информационной системы был выбран Python. Данный язык был выбран по ряду преимуществ, среди которых следует выделить совместимость с огромным количеством БД, высокую производительность, наличие динамической типизации данных, высокую читаемость итоговой кодификации и наличие множества библиотек.
Для разработки пользовательского графического интерфейса был выбран набор расширений графического фреймворка Qt для Python – PyQt5. Для взаимодействия с СУБД используется самый популярный адаптер для  PostgreSQL – Navicat, он обеспечивает доступ ко многим функциям СУБД. Чтобы генерировать Excel файлы с диаграммами был выбран Python модуль xlsxwriter.
