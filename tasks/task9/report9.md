# Задание 9 — Шаг 6: Архитектура и принципы поведения системы Match-3

## Контекст

Шаг 6 фокусируется на **архитектурных решениях** и **принципах поведения** системы. Это переход от формальных спецификаций АТД (шаги 4–5) к конкретной схеме их взаимодействия и реализации.

## 1. Схемы создания объектов

### 1.1 Основные фабрики и билдеры

#### BoardFactory
```python
class BoardFactory:
    """Фабрика для создания различных типов досок.
    
    Ответственность:
    - Создание пустых досок
    - Генерация начальных досок с фишками
    - Создание досок без начальных совпадений
    """
    
    @staticmethod
    def create_empty_board() -> MutableBoard:
        """Создать пустую доску 8x8.
        
        Returns:
            MutableBoard: Пустая доска с None во всех ячейках
        """
        
    @staticmethod
    def create_initial_board(random: RandomProvider) -> MutableBoard:
        """Создать доску с случайными фишками.
        
        Args:
            random: Источник случайных значений
            
        Returns:
            MutableBoard: Доска, заполненная случайными фишками A-E
        """
        
    @staticmethod
    def create_board_without_matches(random: RandomProvider) -> MutableBoard:
        """Создать доску без начальных совпадений.
        
        Args:
            random: Источник случайных значений
            
        Returns:
            MutableBoard: Доска без совпадений ≥3 в ряд
            
        Note:
            Может потребовать несколько попыток генерации
        """
```

**Lifecycle MutableBoard:**
1. Создание через `BoardFactory.create_empty_board()`
2. Заполнение через `fill_empty(random)` 
3. Операции свопа через `swap(a, b)`
4. Модификации через `set_tile(cell, tile)`
5. Клонирование через `clone()` для неизменяемых операций

#### GameStateBuilder
```python
class GameStateBuilder:
    """Builder для создания GameState с гибкой конфигурацией.
    
    Ответственность:
    - Пошаговое конструирование GameState
    - Валидация параметров при создании
    - Предоставление значений по умолчанию
    """
    
    def __init__(self):
        """Инициализировать builder с значениями по умолчанию."""
        self._board: Optional[Board] = None
        self._score: int = 0
        self._moves_available: bool = True
    
    def with_board(self, board: Board) -> 'GameStateBuilder':
        """Установить доску.
        
        Args:
            board: Игровая доска
            
        Returns:
            GameStateBuilder: self для цепочки вызовов
        """
        
    def with_score(self, score: int) -> 'GameStateBuilder':
        """Установить счёт.
        
        Args:
            score: Начальный счёт (≥0)
            
        Returns:
            GameStateBuilder: self для цепочки вызовов
        """
        
    def with_moves_available(self, available: bool) -> 'GameStateBuilder':
        """Установить доступность ходов.
        
        Args:
            available: Есть ли доступные ходы
            
        Returns:
            GameStateBuilder: self для цепочки вызовов
        """
        
    def build(self) -> GameState:
        """Создать GameState.
        
        Returns:
            GameState: Сконфигурированное состояние игры
            
        Raises:
            ValueError: Если не установлена доска
        """
```

**Lifecycle GameState:**
1. Создание через `GameStateBuilder`
2. Обновление через `GameController.perform_move()`
3. Проверка статуса через `update_moves_available()`

#### ServiceContainer (Dependency Injection)
```python
class ServiceContainer:
    """Контейнер для управления зависимостями сервисов.
    
    Ответственность:
    - Регистрация сервисов
    - Предоставление сервисов по запросу
    - Управление жизненным циклом сервисов
    - Обеспечение слабых связей между компонентами
    """
    
    def __init__(self):
        """Инициализировать пустой контейнер."""
        self._services: Dict[str, Any] = {}
    
    def register_swap_validator(self, validator: SwapValidator) -> None:
        """Зарегистрировать валидатор свопов.
        
        Args:
            validator: Валидатор для проверки свопов
        """
        
    def register_match_finder(self, finder: MatchFinder) -> None:
        """Зарегистрировать поисковик совпадений.
        
        Args:
            finder: Поисковик совпадений на доске
        """
        
    def register_match_resolver(self, resolver: MatchResolver) -> None:
        """Зарегистрировать резолвер совпадений.
        
        Args:
            resolver: Резолвер для удаления совпадений
        """
        
    def register_gravity_engine(self, engine: GravityEngine) -> None:
        """Зарегистрировать движок гравитации.
        
        Args:
            engine: Движок для падения и заполнения фишек
        """
        
    def register_score_manager(self, manager: ScoreManager) -> None:
        """Зарегистрировать менеджер счёта.
        
        Args:
            manager: Менеджер для расчёта и начисления очков
        """
        
    def register_combo_tracker(self, tracker: ComboTracker) -> None:
        """Зарегистрировать трекер комбо.
        
        Args:
            tracker: Трекер для отслеживания каскадов
        """
        
    def register_random_provider(self, provider: RandomProvider) -> None:
        """Зарегистрировать поставщика случайностей.
        
        Args:
            provider: Поставщик случайных значений
        """
        
    def get_swap_validator(self) -> SwapValidator:
        """Получить валидатор свопов.
        
        Returns:
            SwapValidator: Зарегистрированный валидатор
            
        Raises:
            KeyError: Если валидатор не зарегистрирован
        """
        
    def get_services(self) -> Dict[str, Any]:
        """Получить все зарегистрированные сервисы.
        
        Returns:
            Dict[str, Any]: Словарь всех сервисов
        """
```

### 1.2 Специализированные билдеры

#### ComboTrackerBuilder
```python
class ComboTrackerBuilder:
    """Builder для создания и настройки ComboTracker.
    
    Ответственность:
    - Создание трекеров комбо с начальными значениями
    - Сброс существующих трекеров
    - Конфигурация параметров трекинга
    """
    
    @staticmethod
    def create() -> ComboTracker:
        """Создать новый трекер комбо.
        
        Returns:
            ComboTracker: Трекер с индексом каскада = 0
        """
        
    @staticmethod
    def reset(tracker: ComboTracker) -> None:
        """Сбросить трекер комбо к начальному состоянию.
        
        Args:
            tracker: Трекер для сброса
        """
        
    @staticmethod
    def create_with_initial_index(index: int) -> ComboTracker:
        """Создать трекер с заданным начальным индексом.
        
        Args:
            index: Начальный индекс каскада (≥0)
            
        Returns:
            ComboTracker: Трекер с заданным индексом
        """
```

#### RandomProviderBuilder
```python
class RandomProviderBuilder:
    """Builder для создания различных RandomProvider.
    
    Ответственность:
    - Создание стандартных поставщиков случайностей
    - Создание тестовых поставщиков с предопределёнными последовательностями
    - Конфигурация параметров генерации
    """
    
    @staticmethod
    def create_default() -> RandomProviderDefault:
        """Создать стандартный поставщик случайностей.
        
        Returns:
            RandomProviderDefault: Поставщик с системным seed
        """
        
    @staticmethod
    def create_with_seed(seed: int) -> RandomProviderDefault:
        """Создать поставщик с фиксированным seed.
        
        Args:
            seed: Начальное значение для генератора
            
        Returns:
            RandomProviderDefault: Поставщик с заданным seed
        """
        
    @staticmethod
    def create_mock(sequence: List[TileKind]) -> MockRandomProvider:
        """Создать тестовый поставщик с предопределённой последовательностью.
        
        Args:
            sequence: Последовательность фишек для возврата
            
        Returns:
            MockRandomProvider: Поставщик для тестирования
        """
        
    @staticmethod
    def create_weighted(weights: Dict[TileKind, float]) -> WeightedRandomProvider:
        """Создать поставщик с весовым распределением.
        
        Args:
            weights: Словарь весов для каждого типа фишки
            
        Returns:
            WeightedRandomProvider: Поставщик с заданными весами
        """
```

### 1.3 Детальные описания ключевых классов

#### GameController
```python
class GameController:
    """Основной контроллер игровой логики.
    
    Ответственность:
    - Координация выполнения ходов
    - Управление каскадными эффектами
    - Обновление состояния игры
    - Валидация игровых действий
    """
    
    def __init__(self, services: ServiceContainer):
        """Инициализировать контроллер с сервисами.
        
        Args:
            services: Контейнер с игровыми сервисами
        """
        self._services = services
        self._swap_validator = services.get_swap_validator()
        self._match_finder = services.get_match_finder()
        self._match_resolver = services.get_match_resolver()
        self._gravity_engine = services.get_gravity_engine()
        self._score_manager = services.get_score_manager()
        self._combo_tracker = services.get_combo_tracker()
        self._random_provider = services.get_random_provider()
    
    def perform_move(self, state: GameState, a: Cell, b: Cell) -> bool:
        """Выполнить ход игрока.
        
        Args:
            state: Текущее состояние игры
            a: Первая ячейка для свопа
            b: Вторая ячейка для свопа
            
        Returns:
            bool: True если ход выполнен успешно, False если невалидный
            
        Raises:
            ValueError: Если ячейки не соседние или вне доски
        """
        
    def update_moves_available(self, state: GameState) -> None:
        """Обновить флаг доступности ходов.
        
        Args:
            state: Состояние для обновления
        """
        
    def is_game_over(self, state: GameState) -> bool:
        """Проверить, завершена ли игра.
        
        Args:
            state: Состояние для проверки
            
        Returns:
            bool: True если игра завершена
        """
        
    def _execute_cascade(self, board: MutableBoard, state: GameState) -> int:
        """Выполнить каскадное разрешение совпадений.
        
        Args:
            board: Доска для обработки
            state: Состояние для обновления счёта
            
        Returns:
            int: Общее количество очков за каскад
        """
```

#### MutableBoard
```python
class MutableBoard(Board):
    """Изменяемая реализация игровой доски.
    
    Ответственность:
    - Хранение состояния доски 8x8
    - Выполнение операций изменения (своп, установка фишек)
    - Заполнение пустых ячеек новыми фишками
    - Поддержание инвариантов доски
    """
    
    def __init__(self):
        """Создать пустую доску 8x8."""
        self._tiles: List[List[Optional[Tile]]] = [[None for _ in range(8)] for _ in range(8)]
    
    def width(self) -> int:
        """Получить ширину доски.
        
        Returns:
            int: Ширина доски (всегда 8)
        """
        
    def height(self) -> int:
        """Получить высоту доски.
        
        Returns:
            int: Высота доски (всегда 8)
        """
        
    def tile_at(self, cell: Cell) -> Optional[Tile]:
        """Получить фишку в указанной ячейке.
        
        Args:
            cell: Ячейка для проверки
            
        Returns:
            Optional[Tile]: Фишка в ячейке или None
        """
        
    def is_inside(self, cell: Cell) -> bool:
        """Проверить, находится ли ячейка в пределах доски.
        
        Args:
            cell: Ячейка для проверки
            
        Returns:
            bool: True если ячейка внутри доски
        """
        
    def enumerate_cells(self) -> Iterable[Cell]:
        """Перечислить все ячейки доски.
        
        Returns:
            Iterable[Cell]: Все ячейки доски
        """
        
    def clone(self) -> 'MutableBoard':
        """Создать копию доски.
        
        Returns:
            MutableBoard: Независимая копия доски
        """
        
    def set_tile(self, cell: Cell, tile: Optional[Tile]) -> None:
        """Установить фишку в ячейку.
        
        Args:
            cell: Ячейка для установки
            tile: Фишка для установки (None для очистки)
            
        Raises:
            ValueError: Если ячейка вне доски
        """
        
    def swap(self, a: Cell, b: Cell) -> None:
        """Обменять содержимое двух ячеек.
        
        Args:
            a: Первая ячейка
            b: Вторая ячейка
            
        Raises:
            ValueError: Если ячейки не соседние или вне доски
        """
        
    def fill_empty(self, random: RandomProvider) -> None:
        """Заполнить пустые ячейки новыми фишками.
        
        Args:
            random: Поставщик случайных фишек
        """
        
    def _is_adjacent(self, a: Cell, b: Cell) -> bool:
        """Проверить, являются ли ячейки соседними.
        
        Args:
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            bool: True если ячейки соседние по стороне
        """
```

#### GameState
```python
@dataclass
class GameState:
    """Состояние игры.
    
    Ответственность:
    - Хранение текущего состояния доски
    - Отслеживание счёта игрока
    - Управление флагом доступности ходов
    """
    
    board: Board
    score: int
    moves_available: bool
    
    def __post_init__(self):
        """Валидация после инициализации."""
        if self.score < 0:
            raise ValueError("Счёт не может быть отрицательным")
        if self.board is None:
            raise ValueError("Доска обязательна")
    
    def get_score(self) -> int:
        """Получить текущий счёт.
        
        Returns:
            int: Текущий счёт игрока
        """
        
    def add_score(self, points: int) -> None:
        """Добавить очки к счёту.
        
        Args:
            points: Количество очков для добавления (≥0)
        """
        
    def has_moves(self) -> bool:
        """Проверить, есть ли доступные ходы.
        
        Returns:
            bool: True если есть доступные ходы
        """
        
    def set_moves_available(self, available: bool) -> None:
        """Установить флаг доступности ходов.
        
        Args:
            available: Доступны ли ходы
        """
```

#### SwapValidator
```python
class SwapValidator:
    """Валидатор для проверки допустимости свопов.
    
    Ответственность:
    - Проверка соседства ячеек
    - Валидация создания совпадений при свопе
    - Проверка границ доски
    """
    
    def is_adjacent(self, a: Cell, b: Cell) -> bool:
        """Проверить, являются ли ячейки соседними.
        
        Args:
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            bool: True если ячейки соседние по стороне
        """
        
    def is_swap_creating_match(self, board: Board, a: Cell, b: Cell) -> bool:
        """Проверить, создаёт ли своп совпадения.
        
        Args:
            board: Доска для проверки
            a: Первая ячейка свопа
            b: Вторая ячейка свопа
            
        Returns:
            bool: True если своп создаст ≥1 совпадение
            
        Raises:
            ValueError: Если ячейки не соседние или вне доски
        """
        
    def is_valid_swap(self, board: Board, a: Cell, b: Cell) -> bool:
        """Проверить валидность свопа.
        
        Args:
            board: Доска для проверки
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            bool: True если своп валиден
        """
        
    def _are_cells_adjacent(self, a: Cell, b: Cell) -> bool:
        """Проверить соседство ячеек по координатам.
        
        Args:
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            bool: True если ячейки соседние
        """
        
    def _simulate_swap(self, board: Board, a: Cell, b: Cell) -> Board:
        """Симулировать своп на копии доски.
        
        Args:
            board: Исходная доска
            a: Первая ячейка
            b: Вторая ячейка
            
        Returns:
            Board: Доска после симуляции свопа
        """
```

## 2. Обработка событий и поведение системы

### 2.1 Основной игровой цикл

```
1. Инициализация
   ├── Создание ServiceContainer
   ├── Регистрация всех сервисов
   ├── Создание GameState через GameStateBuilder
   └── Генерация начальной доски без совпадений

2. Главный цикл игры
   ├── Вывод текущего состояния (ConsoleIO.print_board)
   ├── Ввод хода игрока (ConsoleIO.read_move)
   ├── Валидация ввода (проверка координат, соседства)
   ├── Выполнение хода (GameController.perform_move)
   │   ├── Проверка валидности свопа
   │   ├── Выполнение свопа
   │   ├── Каскадное разрешение совпадений
   │   └── Обновление счёта
   ├── Обновление статуса игры (update_moves_available)
   └── Проверка завершения (moves_available == false)

3. Завершение
   ├── Вывод финального счёта
   └── Предложение перезапуска
```

### 2.2 Схема каскадного разрешения совпадений

```
perform_move(state, a, b, services):
├── 1. Валидация
│   ├── SwapValidator.is_adjacent(a, b)
│   └── SwapValidator.is_swap_creating_match(board, a, b)
├── 2. Выполнение свопа
│   └── MutableBoard.swap(a, b)
├── 3. Каскадный цикл
│   ├── ComboTracker.reset()
│   └── Пока есть совпадения:
│       ├── MatchFinder.find_matches(board)
│       ├── MatchResolver.remove_matches(board, matches)
│       ├── ScoreManager.add_points(state, score_for_removed)
│       ├── GravityEngine.apply_gravity(board)
│       ├── GravityEngine.refill(board, random)
│       └── ComboTracker.increment()
└── 4. Обновление состояния
    ├── state.board = board
    └── state.score += total_points
```

### 2.3 Обработка ошибок

#### Ошибки ввода
- **Неверные координаты**: `ValueError` с сообщением "Координаты вне диапазона [0-7]"
- **Несоседние ячейки**: `ValueError` с сообщением "Ячейки не являются соседними"
- **Недопустимый формат**: `ValueError` с сообщением "Неверный формат ввода. Используйте: row1 col1 row2 col2"

#### Ошибки игровой логики
- **Своп не создаёт совпадения**: `perform_move` возвращает `false`, состояние не изменяется
- **Нарушение предусловий**: `AssertionError` с описанием нарушенного условия
- **Нет доступных ходов**: игра завершается, выводится финальный счёт

#### Ошибки системы
- **Ошибка генерации случайных значений**: `RuntimeError` с сообщением "Ошибка генерации фишек"
- **Ошибка I/O**: `IOError` с сообщением "Ошибка ввода/вывода"

## 3. Увязка с выбранными технологиями

### 3.1 Технологический стек
- **Язык**: Python 3.11+
- **Стандартная библиотека**: `random`, `typing`, `abc`, `dataclasses`
- **I/O**: `input()`, `print()`, `sys.stdout`
- **Тестирование**: `unittest` (встроенный модуль)

### 3.2 Структура модулей в `project/`

```
project/
├── __init__.py
├── main.py                    # Точка входа в приложение
├── board/
│   ├── __init__.py
│   ├── tile_kind.py          # TileKind (enum)
│   ├── tile.py               # Tile
│   ├── cell.py               # Cell
│   ├── board.py              # Board (абстрактный)
│   ├── mutable_board.py      # MutableBoard
│   └── board_factory.py      # BoardFactory
├── rules/
│   ├── __init__.py
│   ├── swap_validator.py     # SwapValidator
│   ├── move_generator.py     # MoveGenerator
│   └── match_finder.py       # MatchFinder
├── mechanics/
│   ├── __init__.py
│   ├── match_resolver.py     # MatchResolver
│   └── gravity_engine.py     # GravityEngine
├── scoring/
│   ├── __init__.py
│   ├── score_manager.py      # ScoreManager
│   └── combo_tracker.py      # ComboTracker
├── random/
│   ├── __init__.py
│   ├── random_provider.py    # RandomProvider (интерфейс)
│   └── random_provider_default.py  # RandomProviderDefault
├── control/
│   ├── __init__.py
│   ├── game_state.py         # GameState
│   ├── game_controller.py    # GameController
│   ├── service_container.py  # ServiceContainer
│   └── builders.py           # GameStateBuilder, ComboTrackerBuilder
├── io/
│   ├── __init__.py
│   └── console_io.py         # ConsoleIO
└── tests/
    ├── __init__.py
    ├── test_board.py
    ├── test_rules.py
    ├── test_mechanics.py
    ├── test_scoring.py
    ├── test_control.py
    └── test_integration.py
```

### 3.3 Принцип Dependency Injection

```python
# Пример использования ServiceContainer
def create_game_services() -> ServiceContainer:
    container = ServiceContainer()
    
    # Регистрация сервисов
    container.register_swap_validator(SwapValidator())
    container.register_match_finder(MatchFinder())
    container.register_match_resolver(MatchResolver())
    container.register_gravity_engine(GravityEngine())
    container.register_score_manager(ScoreManager())
    container.register_combo_tracker(ComboTrackerBuilder.create())
    container.register_random_provider(RandomProviderBuilder.create_default())
    
    return container

# Использование в GameController
def perform_move(self, state: GameState, a: Cell, b: Cell, services: ServiceContainer):
    swap_validator = services.get_swap_validator()
    match_finder = services.get_match_finder()
    # ... остальные сервисы
```

## 4. Тесты для типовых сценариев

### 4.1 Сценарий 1: Простой валидный ход
```python
def test_simple_valid_move():
    """Тест простого валидного хода с одной группой совпадений.
    
    Проверяет:
    - Валидацию свопа
    - Выполнение свопа
    - Удаление совпадений
    - Начисление очков
    - Применение гравитации
    """
    # Arrange
    random_provider = RandomProviderBuilder.create_with_seed(42)
    board = BoardFactory.create_board_without_matches(random_provider)
    
    # Создаём конфигурацию A-B-A для горизонтального совпадения
    board.set_tile(Cell(3, 3), Tile(TileKind.A))
    board.set_tile(Cell(3, 4), Tile(TileKind.B))
    board.set_tile(Cell(3, 5), Tile(TileKind.A))
    
    state = GameStateBuilder().with_board(board).with_score(0).build()
    services = create_game_services()
    game_controller = GameController(services)
    
    # Act
    result = game_controller.perform_move(state, Cell(3, 4), Cell(3, 5), services)
    
    # Assert
    assert result == True, "Ход должен быть выполнен успешно"
    assert state.score > 0, "Счёт должен увеличиться"
    assert board.tile_at(Cell(3, 3)) is None, "Фишка A должна быть удалена"
    assert board.tile_at(Cell(3, 4)) is None, "Фишка B должна быть удалена" 
    assert board.tile_at(Cell(3, 5)) is None, "Фишка A должна быть удалена"
    
    # Проверяем, что пустые места заполнены новыми фишками
    for col in [3, 4, 5]:
        tile = board.tile_at(Cell(3, col))
        assert tile is not None, f"Ячейка (3, {col}) должна быть заполнена"
        assert tile.kind() in TileKind.all(), "Фишка должна быть допустимого типа"
```

### 4.2 Сценарий 2: Каскадный ход
```python
def test_cascade_move():
    # Arrange
    board = create_cascade_test_board()  # Специальная конфигурация
    initial_score = state.score
    
    # Act
    result = game_controller.perform_move(state, Cell(2, 2), Cell(2, 3), services)
    
    # Assert
    assert result == True
    assert state.score > initial_score + 30  # Очки за каскад
    assert combo_tracker.current_index() > 1  # Было несколько волн
```

### 4.3 Сценарий 3: Невалидный ход
```python
def test_invalid_move():
    # Arrange
    board = create_no_matches_board()
    
    # Act
    result = game_controller.perform_move(state, Cell(0, 0), Cell(0, 1), services)
    
    # Assert
    assert result == False
    assert state.score == initial_score  # Счёт не изменился
    assert board.tile_at(Cell(0, 0)) == original_tile_0  # Доска не изменилась
    assert board.tile_at(Cell(0, 1)) == original_tile_1
```

### 4.4 Сценарий 4: Завершение игры
```python
def test_game_over():
    # Arrange
    board = create_no_moves_board()  # Доска без возможных ходов
    move_generator = MoveGenerator()
    
    # Act
    game_controller.update_moves_available(state, move_generator)
    
    # Assert
    assert state.moves_available == False
    assert game_controller.is_game_over(state) == True
```

### 4.5 Сценарий 5: Начальная генерация
```python
def test_initial_board_generation():
    # Arrange
    random_provider = RandomProviderBuilder.create_with_seed(42)
    
    # Act
    board = BoardFactory.create_board_without_matches(random_provider)
    matches = MatchFinder().find_matches(board)
    
    # Assert
    assert len(matches) == 0  # Нет начальных совпадений
    assert board.width() == 8
    assert board.height() == 8
    # Все ячейки заполнены допустимыми фишками
    for cell in board.enumerate_cells():
        tile = board.tile_at(cell)
        assert tile is not None
        assert tile.kind() in TileKind.all()
```

## 5. Архитектурные диаграммы

### 5.1 Схема зависимостей кластеров

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Board    │    │    Rules    │    │  Mechanics  │
│             │    │             │    │             │
│ - TileKind  │    │ - SwapVal   │    │ - MatchRes  │
│ - Tile      │    │ - MoveGen   │    │ - Gravity   │
│ - Cell      │    │ - MatchFind │    │             │
│ - Board     │    │             │    │             │
│ - MutableBd │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Scoring   │    │   Control   │    │     IO      │
│             │    │             │    │             │
│ - ScoreMgr  │    │ - GameState │    │ - ConsoleIO │
│ - ComboTrk  │    │ - GameCtrl  │    │             │
│             │    │ - ServCont  │    │             │
│             │    │ - Builders  │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                   ┌─────────────┐
                   │   Random    │
                   │             │
                   │ - RandProv  │
                   │ - RandDef   │
                   │             │
                   └─────────────┘
```

### 5.2 Последовательность вызовов в perform_move

```
GameController.perform_move()
├── SwapValidator.is_adjacent(a, b)
├── SwapValidator.is_swap_creating_match(board, a, b)
├── MutableBoard.swap(a, b)
├── ComboTracker.reset()
└── Цикл каскада:
    ├── MatchFinder.find_matches(board)
    ├── MatchResolver.remove_matches(board, matches)
    ├── ScoreManager.add_points(state, points)
    ├── GravityEngine.apply_gravity(board)
    ├── GravityEngine.refill(board, random)
    └── ComboTracker.increment()
```


## 7. Дополнительные классы с подробными описаниями

### 7.1 Классы механики игры

#### MatchFinder
```python
class MatchFinder:
    """Поисковик совпадений на доске.
    
    Ответственность:
    - Поиск всех горизонтальных совпадений ≥3 фишек
    - Поиск всех вертикальных совпадений ≥3 фишек
    - Группировка совпадений без пересечений
    - Валидация найденных групп
    """
    
    def find_matches(self, board: Board) -> Set[Set[Cell]]:
        """Найти все совпадения на доске.
        
        Args:
            board: Доска для поиска совпадений
            
        Returns:
            Set[Set[Cell]]: Множество групп ячеек с совпадениями
            
        Note:
            Каждая группа содержит ≥3 ячейки одного типа в ряд
        """
        
    def find_horizontal_matches(self, board: Board) -> Set[Set[Cell]]:
        """Найти горизонтальные совпадения.
        
        Args:
            board: Доска для поиска
            
        Returns:
            Set[Set[Cell]]: Горизонтальные группы совпадений
        """
        
    def find_vertical_matches(self, board: Board) -> Set[Set[Cell]]:
        """Найти вертикальные совпадения.
        
        Args:
            board: Доска для поиска
            
        Returns:
            Set[Set[Cell]]: Вертикальные группы совпадений
        """
        
    def _find_matches_in_line(self, board: Board, start: Cell, direction: Tuple[int, int]) -> Set[Cell]:
        """Найти совпадения в заданном направлении.
        
        Args:
            board: Доска для поиска
            start: Начальная ячейка
            direction: Направление поиска (dx, dy)
            
        Returns:
            Set[Cell]: Ячейки с совпадением в направлении
        """
```

#### MatchResolver
```python
class MatchResolver:
    """Резолвер для удаления совпадений.
    
    Ответственность:
    - Удаление фишек из найденных совпадений
    - Подсчёт количества удалённых фишек
    - Валидация групп совпадений
    - Очистка ячеек доски
    """
    
    def remove_matches(self, board: MutableBoard, matches: Set[Set[Cell]]) -> int:
        """Удалить совпадения с доски.
        
        Args:
            board: Доска для изменения
            matches: Группы ячеек для удаления
            
        Returns:
            int: Количество удалённых фишек
            
        Raises:
            ValueError: Если группы совпадений невалидны
        """
        
    def _validate_match_groups(self, board: Board, matches: Set[Set[Cell]]) -> None:
        """Валидировать группы совпадений.
        
        Args:
            board: Доска для проверки
            matches: Группы для валидации
            
        Raises:
            ValueError: Если группы невалидны
        """
        
    def _remove_group(self, board: MutableBoard, group: Set[Cell]) -> int:
        """Удалить одну группу совпадений.
        
        Args:
            board: Доска для изменения
            group: Группа ячеек для удаления
            
        Returns:
            int: Количество удалённых фишек
        """
```

#### GravityEngine
```python
class GravityEngine:
    """Движок гравитации и заполнения.
    
    Ответственность:
    - Применение гравитации (падение фишек вниз)
    - Заполнение пустых ячеек новыми фишками
    - Сохранение относительного порядка фишек
    - Поддержание инвариантов доски
    """
    
    def apply_gravity(self, board: MutableBoard) -> None:
        """Применить гравитацию ко всем столбцам.
        
        Args:
            board: Доска для обработки
            
        Note:
            Фишки падают вниз, сохраняя относительный порядок
        """
        
    def refill(self, board: MutableBoard, random: RandomProvider) -> None:
        """Заполнить пустые ячейки новыми фишками.
        
        Args:
            board: Доска для заполнения
            random: Поставщик случайных фишек
        """
        
    def _apply_gravity_to_column(self, board: MutableBoard, col: int) -> None:
        """Применить гравитацию к одному столбцу.
        
        Args:
            board: Доска для изменения
            col: Индекс столбца
        """
        
    def _compact_column(self, tiles: List[Optional[Tile]]) -> List[Optional[Tile]]:
        """Сжать столбец, убрав None между фишками.
        
        Args:
            tiles: Список фишек столбца
            
        Returns:
            List[Optional[Tile]]: Сжатый столбец
        """
```

### 7.2 Классы подсчёта очков

#### ScoreManager
```python
class ScoreManager:
    """Менеджер для расчёта и начисления очков.
    
    Ответственность:
    - Расчёт очков за удалённые фишки
    - Учёт множителей каскада
    - Начисление очков к счёту
    - Валидация параметров подсчёта
    """
    
    def __init__(self, base_points: int = 10, cascade_multiplier: float = 1.5):
        """Инициализировать менеджер счёта.
        
        Args:
            base_points: Базовые очки за фишку
            cascade_multiplier: Множитель за каскад
        """
        self._base_points = base_points
        self._cascade_multiplier = cascade_multiplier
    
    def score_for_removed(self, removed_count: int, cascade_index: int) -> int:
        """Рассчитать очки за удалённые фишки.
        
        Args:
            removed_count: Количество удалённых фишек
            cascade_index: Индекс каскада (≥0)
            
        Returns:
            int: Количество очков
            
        Raises:
            ValueError: Если параметры невалидны
        """
        
    def add_points(self, state: GameState, points: int) -> None:
        """Добавить очки к счёту.
        
        Args:
            state: Состояние игры
            points: Очки для добавления (≥0)
        """
        
    def _calculate_cascade_multiplier(self, cascade_index: int) -> float:
        """Рассчитать множитель каскада.
        
        Args:
            cascade_index: Индекс каскада
            
        Returns:
            float: Множитель для очков
        """
```

#### ComboTracker
```python
class ComboTracker:
    """Трекер для отслеживания каскадов.
    
    Ответственность:
    - Отслеживание текущего индекса каскада
    - Сброс индекса при новом ходе
    - Увеличение индекса при новой волне
    - Предоставление текущего состояния
    """
    
    def __init__(self, initial_index: int = 0):
        """Инициализировать трекер.
        
        Args:
            initial_index: Начальный индекс каскада
        """
        self._current_index = initial_index
    
    def reset(self) -> None:
        """Сбросить индекс каскада к 0."""
        self._current_index = 0
    
    def increment(self) -> None:
        """Увеличить индекс каскада на 1."""
        self._current_index += 1
    
    def current_index(self) -> int:
        """Получить текущий индекс каскада.
        
        Returns:
            int: Текущий индекс каскада
        """
        
    def set_index(self, index: int) -> None:
        """Установить индекс каскада.
        
        Args:
            index: Новый индекс (≥0)
        """
```

### 7.3 Классы ввода/вывода

#### ConsoleIO
```python
class ConsoleIO:
    """Адаптер для консольного ввода/вывода.
    
    Ответственность:
    - Чтение ходов игрока из консоли
    - Вывод доски в консоль
    - Отображение счёта и сообщений
    - Обработка ошибок ввода
    """
    
    def read_move(self) -> Tuple[Cell, Cell]:
        """Прочитать ход игрока.
        
        Returns:
            Tuple[Cell, Cell]: Пара ячеек для свопа
            
        Raises:
            ValueError: Если ввод невалиден
        """
        
    def print_board(self, board: Board) -> None:
        """Вывести доску в консоль.
        
        Args:
            board: Доска для вывода
        """
        
    def print_score(self, score: int) -> None:
        """Вывести текущий счёт.
        
        Args:
            score: Счёт для вывода
        """
        
    def print_game_over(self) -> None:
        """Вывести сообщение о завершении игры."""
        
    def print_error(self, message: str) -> None:
        """Вывести сообщение об ошибке.
        
        Args:
            message: Сообщение об ошибке
        """
        
    def _parse_coordinates(self, input_str: str) -> Tuple[Cell, Cell]:
        """Распарсить координаты из строки.
        
        Args:
            input_str: Строка с координатами
            
        Returns:
            Tuple[Cell, Cell]: Пара ячеек
            
        Raises:
            ValueError: Если формат неверный
        """
        
    def _format_board(self, board: Board) -> str:
        """Форматировать доску для вывода.
        
        Args:
            board: Доска для форматирования
            
        Returns:
            str: Отформатированная строка доски
        """
```

### 7.4 Классы случайности

#### RandomProviderDefault
```python
class RandomProviderDefault(RandomProvider):
    """Стандартная реализация поставщика случайностей.
    
    Ответственность:
    - Генерация случайных фишек
    - Управление seed для воспроизводимости
    - Обеспечение равномерного распределения
    """
    
    def __init__(self, seed: Optional[int] = None):
        """Инициализировать генератор.
        
        Args:
            seed: Начальное значение (None для системного)
        """
        self._random = random.Random(seed)
        self._tile_kinds = list(TileKind.all())
    
    def next_tile_kind(self) -> TileKind:
        """Получить следующий случайный тип фишки.
        
        Returns:
            TileKind: Случайный тип фишки
        """
        
    def set_seed(self, seed: int) -> None:
        """Установить seed генератора.
        
        Args:
            seed: Новое начальное значение
        """
        
    def _generate_tile_kind(self) -> TileKind:
        """Сгенерировать случайный тип фишки.
        
        Returns:
            TileKind: Случайный тип из доступных
        """
```
