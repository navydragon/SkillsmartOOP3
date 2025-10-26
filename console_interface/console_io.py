"""Адаптер для консольного ввода/вывода."""

from typing import Tuple

from board.board import Board
from board.cell import Cell


class ConsoleIO:
    """Адаптер для консольного ввода/вывода."""
    
    def read_move(self) -> Tuple[Cell, Cell]:
        """Прочитать ход игрока.
        
        Returns:
            Tuple[Cell, Cell]: Пара ячеек для свопа
            
        Raises:
            ValueError: Если ввод невалиден
        """
        while True:
            try:
                input_str = input("Введите ход (row1 col1 row2 col2): ").strip()
                return self._parse_coordinates(input_str)
            except ValueError as e:
                print(f"Ошибка ввода: {e}")
                print("Используйте формат: row1 col1 row2 col2 (например: 0 1 0 2)")
    
    def print_board(self, board: Board) -> None:
        """Вывести доску в консоль.
        
        Args:
            board: Доска для вывода
        """
        print("\n" + "="*50)
        print("ИГРОВОЕ ПОЛЕ")
        print("="*50)
        
        # Выводим заголовок с номерами столбцов
        print("   ", end="")
        for col in range(board.width()):
            print(f" {col:2}", end="")
        print()
        
        # Выводим строки
        for row in range(board.height()):
            print(f"{row:2} ", end="")
            for col in range(board.width()):
                cell = Cell(row, col)
                tile = board.tile_at(cell)
                if tile is not None:
                    print(f" {tile.kind().value:2}", end="")
                else:
                    print("  .", end="")
            print()
        
        print("="*50)
    
    def print_score(self, score: int) -> None:
        """Вывести текущий счёт.
        
        Args:
            score: Счёт для вывода
        """
        print(f"\nТекущий счёт: {score}")
    
    def print_game_over(self) -> None:
        """Вывести сообщение о завершении игры."""
        print("\n" + "="*50)
        print("ИГРА ЗАВЕРШЕНА!")
        print("Нет доступных ходов.")
        print("="*50)
    
    def print_error(self, message: str) -> None:
        """Вывести сообщение об ошибке.
        
        Args:
            message: Сообщение об ошибке
        """
        print(f"\nОШИБКА: {message}")
    
    def print_welcome(self) -> None:
        """Вывести приветственное сообщение."""
        print("="*60)
        print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ТРИ-В-РЯД'!")
        print("="*60)
        print("Цель: создавайте ряды из 3+ одинаковых элементов")
        print("Ход: введите координаты двух соседних элементов для обмена")
        print("Формат: row1 col1 row2 col2 (например: 0 1 0 2)")
        print("="*60)
    
    def print_move_result(self, success: bool, points: int = 0) -> None:
        """Вывести результат хода.
        
        Args:
            success: Успешен ли ход
            points: Полученные очки
        """
        if success:
            if points > 0:
                print(f"\nОтличный ход! Получено очков: {points}")
            else:
                print("\nХод выполнен.")
        else:
            print("\nНеверный ход! Попробуйте ещё раз.")
    
    def ask_play_again(self) -> bool:
        """Спросить, хочет ли игрок играть снова.
        
        Returns:
            bool: True если игрок хочет играть снова
        """
        while True:
            answer = input("\nХотите сыграть ещё раз? (y/n): ").strip().lower()
            if answer in ['y', 'yes', 'да', 'д']:
                return True
            elif answer in ['n', 'no', 'нет', 'н']:
                return False
            else:
                print("Пожалуйста, введите 'y' или 'n'")
    
    def _parse_coordinates(self, input_str: str) -> Tuple[Cell, Cell]:
        """Распарсить координаты из строки.
        
        Args:
            input_str: Строка с координатами
            
        Returns:
            Tuple[Cell, Cell]: Пара ячеек
            
        Raises:
            ValueError: Если формат неверный
        """
        parts = input_str.split()
        
        if len(parts) != 4:
            raise ValueError("Неверный формат ввода. Используйте: row1 col1 row2 col2")
        
        try:
            row1, col1, row2, col2 = map(int, parts)
            
            # Проверяем диапазон координат
            if not (0 <= row1 < 8 and 0 <= col1 < 8 and 0 <= row2 < 8 and 0 <= col2 < 8):
                raise ValueError("Координаты должны быть в диапазоне [0-7]")
            
            cell1 = Cell(row1, col1)
            cell2 = Cell(row2, col2)
            
            # Проверяем, что ячейки соседние
            if not cell1.is_adjacent(cell2):
                raise ValueError("Ячейки должны быть соседними")
            
            return cell1, cell2
            
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Координаты должны быть числами")
            raise
