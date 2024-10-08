Горчаков Роман Владимирович. Вариант 2
# Лабораторная работа 2.22. Тестирование в Python [unittest]

Трудно представить какой-то современный программный проект без тестирования. При этом тестирование осуществляется практических на всех этапах разработки продукта: начиная, непосредственно, с процесса создания функций, методов и классов и т. д., когда пишутся unit-тесты (а иногда и раньше, в случае, если используется TDD), и заканчивая функциональным и нагрузочным тестированием уже готового, развернутого продукта.
 
В качестве определения понятия автономного теста воспользуемся тем, что дает Рой Ошероув в своей книге "Искусство автономного тестирования с примерами на C#": автономный тест – это автоматизированная часть кода, которая вызывает тестируемую единицу работы и затем проверяет некоторые предположения о единственном конечном результате этой единицы. В качестве тестируемый единицы может выступать как отдельный метод (функция), так и совокупность классов (или функций). Идея автономной единицы в том, что она представляет собой некоторую логически законченную сущность вашей программы. Автономное тестирование ещё называют модульным или unit-тестированием (unit-testing).

Важной характеристикой unit-теста является его повторяемость, т.е. результат его работы не зависит от окружения (внешнего мира), если же приходится обращаться к внешнему миру в процессе выполнения теста, то необходимо предусмотреть возможность подмены "мира" какой-то статичной сущностью. Unit-тесты могут быть написаны собственноручно, без использования сторонних библиотек, а можно использовать специализированные framework’и. На сегодняшний день практически всегда используется второй вариант.

В мире Python существуют три framework’а, которые получили наибольшее распространение: unittest, nose и pytest.

Unittest – это framework для тестирования, входящий в стандартную библиотеку языка Python. Его архитектура выполнена в стиле xUnit. xUnit представляет собой семейство framework’ов для тестирования в разных языках программирования, в Java – это JUnit, C# – NUnit и т.д.

Девизом nose является фраза "nose extends unittest to make testing easier", что можно перевести как "nose расширяет unittest, делая тестирование проще". nose идеален, когда нужно сделать тесты "по-быстрому", без предварительного планирования и выстраивания архитектуры приложения с тестами. Функционал nose можно расширять и настраивать с помощью плагинов.

Pytest довольно мощный инструмент для тестирования, и многие разработчики оставляют свой выбор на нем. Unittest в своей базе – xUnit, что накладывает определенные обязательства при разработке тестов (создание классов-наследников от unittest.TestCase, выполнение определенной процедуры запуска тестов и т.п.). При разработке на pytest ничего этого делать не нужно, вы просто пишете функции, которые должны начинаться с “test_” и используете assert`ы, встроенные в Python (unittest использует свои).

Unittest – это framework для тестирования в Python, который позволяет разрабатывать автономные тесты, собирать тесты в коллекции, обеспечивает независимость тестов от framework`а отчетов и т.д. Основными структурными элемента каркаса unittest являются:

1) Test fixture – обеспечивает подготовку окружения для выполнения тестов, а также организацию мероприятий по их корректному завершению (например, очистка ресурсов). Подготовка окружения может включать в себя создание баз данных, запуск необходим серверов и т.п.;
2) Test case – элементарная единица тестирования, в рамках которой проверяется работа компонента тестируемой программы (метод, класс, поведение и т. п.). Для реализации этой сущности используется класс TestCase;
3) Test suite – коллекция тестов, которая может в себя включать как отдельные test case`ы, так и целые коллекции. Коллекции используются с целью объединения тестов для совместного запуска;
4) Test runner – компонент, который оркестрирует (координирует взаимодействие) запуск тестов и предоставляет пользователю результат их выполнения. Test runner может иметь графический интерфейс, текстовый интерфейс или возвращать какое-то заранее заданное значение, которое будет описывать результат прохождения тестов. Вся работа по написанию тестов заключается в разработке отдельных тестов в рамках test case`ов, сборе их в модули и запуске, если нужно объединить несколько test case`ов, для их совместного запуска, они помещаются в test suite`ы, которые помимо test case`ов могут содержать другие test suite’ы.

Запуск тестов можно сделать как из командной строки, так и с помощью графического интерфейса пользователя (GUI). CLI позволяет запускать тесты из целого модуля, класса или даже обращаться к конкретному тесту. Запуск всех тестов в модуле: python -m unittest <имя модуля>. Если осуществить запуск без указания модуля с тестами, будет запущен Test Discovery.

Для запуска и анализа результатов работы тестов можно использовать GUI. Для установки Cricket можно воспользоваться менеджером pip: pip install cricket. После этого на ваш компьютер будет установлен cricket-unittest. Для запуска тестов в данном приложении, перейдите в каталог с вашим тестирующим кодом и в командной строке запустите cricket-unittest, для этого просто наберите это название и нажмите Enter. Приложение при запуске автоматически загрузит тесты. Для запуска тестов нажмите "Run all".

Основным строительным элементом при написании тестов с использованием unittest является TestCase. Он представляет собой класс, который долженявляться базовым для всех остальных классов, методы которых будут тестировать те или иные автономные единицы исходной программы. Для того, чтобы была возможность использовать компоненты unittest (в том числе и TestCase), в самом начале программы нужно импортировать модуль unittest стандартным образом. При выборе имени класса наследника от TestCase можете руководствоваться следующим правилом: [ИмяТестируемойСущности]Tests. [ИмяТестируемойСущности] – некоторая логическая единица, тесты для которой нужно написать. При написании программ на Python старайтесь придерживаться PEP 8 — Style Guide for Python Code – это рекомендации по стилевому оформлению кода.

Для того, чтобы метод класса выполнялся как тест, необходимо, чтобы он начинался со слова test. Несмотря на то, что методы framework`а unittest написаны не в соответствии с PEP 8 (ввиду того, что идейно он наследник xUnit), имена тестов нужно начинать с префикса test_. Все методы класса TestCase можно разделить на три группы:

1) методы, используемые при запуске тестов;
2) методы, используемые при непосредственном написании тестов (проверка условий, сообщение об ошибках);
3) методы, позволяющие собирать информацию о самом тесте.

К первой группе относятся:

1) setUp(). Метод вызывается перед запуском теста. Как правило, используется для подготовки окружения для теста;
2) tearDown(). Метод вызывается после завершения работы теста. Используется для "приборки" за тестом;
3) setUpClass(). Метод действует на уровне класса, т.е. выполняется перед запуском тестов класса. При этом синтаксис требует наличие декоратора @classmethod;
4) tearDownClass(). Запускается после выполнения всех методов класса, требует наличия декоратора @classmethod;
5) skipTest(reason). Данный метод может быть использован для пропуска теста, если это необходимо.

Ко второй группе относятся:

1) assertEqual(a, b) - a == b
2) assertNotEqual(a, b) - a != b
3) assertTrue(x) - bool(x) is True
4) assertFalse(x) - bool(x) is False
5) assertIs(a, b) - a is b
6) assertIsNot(a, b) - a is not b
7) assertIsNone(x) - x is None
8) assertIsNotNone(x) - x is not None
9) assertIn(a, b) - a in b
10) assertNotIn(a, b) - a not in b
11) assertIsInstance(a, b) - isinstance(a, b)
12) assertNotIsInstance(a, b) - not isinstance(a, b)
13) assertRaises(exc, fun, *args,**kwds) - Функция fun(*args, **kwds) вызывает исключение exc
14) assertRaisesRegex(exc, r, fun,*args, **kwds) - Функция fun(*args, **kwds) вызывает исключение exc, сообщение которого совпадает с регулярным выражением r
15) assertWarns(warn, fun, *args,**kwds) - Функция fun(*args, **kwds) выдает сообщение warn
16) assertWarnsRegex(warn, r, fun,*args, **kwds) - Функция fun(*args, **kwds) выдает сообщение warn и оно совпадает с регулярным выражением r
17) assertAlmostEqual(a, b) - round(a-b, 7) == 0
18) assertNotAlmostEqual(a, b) - round(a-b, 7) != 0
19) assertGreater(a, b) - a > b
20) assertGreaterEqual(a, b) - a >= b
21) assertLess(a, b) - a < b
22) assertLessEqual(a, b) - a <= b
23) assertRegex(s, r) - r.search(s)
24) assertNotRegex(s, r) - not r.search(s)
25) assertCountEqual(a, b) - a и b имеют одинаковые элементы (порядок неважен)
26) assertMultiLineEqual(a, b) - строки (strings)
27) assertSequenceEqual(a, b) - последовательности (sequences)
28) assertListEqual(a, b) - списки (lists)
29) assertTupleEqual(a, b) - кортежи (tuplse)
30) assertSetEqual(a, b) - множества или неизменяемые множества (frozensets)
31) assertDictEqual(a, b) - словари (dicts)
32) fail(msg=None) - ошибка в тесте.

К третьей группе относятся:

1) countTestCases(). Возвращает количество тестов в объекте класса-наследника от TestCase;
2) d(). Возвращает строковый идентификатор теста. Как правило, это полное имя метода, включающее имя модуля и имя класса;
3) shortDescription(). Возвращает описание теста, которое представляет собой первую строку docstring’а метода, если его нет, то возвращает None.

Класс TestSuite используется для объединения тестов в группы, которые могут включать в себя как отдельные тесты так и заранее созданные группы. Помимо этого, TestSuite предоставляет интерфейс, позволяющий TestRunner`у, запускать тесты. Класс TestSuite использует следующие методы:

1) addTest(test). Добавляет TestCase или TestSuite в группу;
2) addTests(tests). Добавляет все TestCase и TestSuite объекты в группу, итеративно проходя по элементам переменной tests;
3) *run(result)*. Запускает тесты из данной группы;
4) countTestCases(). Возвращает количество тестов в данной группе (включает в себя как отдельные тесты, так и подгруппы).

Рассмотрим более подробно вопросы загрузки и запуска тестов. Начнем с класса TestLoader. Этот класс используется для создания групп из классов и модулей. Среди методов TestLoader можно выделить:

1) loadTestsFromTestCase(testCaseClass). Возвращает группу со всеми тестами из класса testCaseClass. Напоминаем, что под тестом понимается модуль, начинающийся со слова "test". Используя этот метод, можно создать список групп тестов, где каждая группа создается на базе классов-наследников от TestCase, объединенных предварительно в список;
2) loadTestsFromModule(module, pattern=None). Загружает все тесты из модуля module. Если модуль поддерживает load_tests протокол, то будет вызвана соответствующая функция модуля и ей будет передан в качестве аргумента (третьим по счету) параметр pattern;
3) loadTestsFromName(name, module=None). Загружает тесты в соответствии с параметром name. Параметр name – имя, разделенное точками. С помощью этого имени указывается уровень, начиная с которого будут добавляться тесты;
4) getTestCaseNames(testCaseClass). Возвращает список имен методов-тестов из класса testCaseClass.

Класс TestResult используется для сбора информации о результатах прохождения тестов. Объекты класса TextTestRunner используются для запуска тестов. Среди параметров, которые передаются конструктору класса, можно выделить verbosity, по умолчанию он равен 1, если создать объект с verbosity=2, то будем получать расширенную информацию о результатах прохождения тестов. Для запуска тестов используется метод run(), которому в качестве аргумента передается класс-наследник от TestCase или группа (TestSuite).
