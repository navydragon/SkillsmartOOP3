"""Главный файл игры Три-в-ряд."""

from board.board_factory import BoardFactory
from random_generator.random_provider_default import RandomProviderDefault
from rules.swap_validator import SwapValidator
from rules.match_finder import MatchFinder
from rules.move_generator import MoveGenerator
from mechanics.match_resolver import MatchResolver
from mechanics.gravity_engine import GravityEngine
from scoring.score_manager import ScoreManager
from scoring.combo_tracker import ComboTracker
from control.game_state_builder import GameStateBuilder
from control.service_container import ServiceContainer
from control.game_controller import GameController
from console_interface.console_io import ConsoleIO


def create_game_services() -> ServiceContainer:
    """Создать контейнер с игровыми сервисами.
    
    Returns:
        ServiceContainer: Контейнер с зарегистрированными сервисами
    """
    container = ServiceContainer()
    
    # Регистрируем все сервисы
    container.register_swap_validator(SwapValidator())
    container.register_match_finder(MatchFinder())
    container.register_match_resolver(MatchResolver())
    container.register_gravity_engine(GravityEngine())
    container.register_score_manager(ScoreManager())
    container.register_combo_tracker(ComboTracker())
    container.register_random_provider(RandomProviderDefault())
    container.register_move_generator(MoveGenerator())
    
    return container


def initialize_game(services: ServiceContainer):
    """Инициализировать новую игру.
    
    Args:
        services: Контейнер с сервисами
        
    Returns:
        GameState: Начальное состояние игры
    """
    random_provider = services.get_random_provider()
    match_finder = services.get_match_finder()
    
    # Создаём доску без начальных совпадений
    board = BoardFactory.create_board_without_matches(random_provider, match_finder)
    
    # Создаём начальное состояние игры
    game_state = (GameStateBuilder()
                 .with_board(board)
                 .with_score(0)
                 .with_moves_available(True)
                 .build())
    
    return game_state


def play_game():
    """Основная функция игры."""
    console_io = ConsoleIO()
    console_io.print_welcome()
    
    while True:
        # Создаём сервисы и инициализируем игру
        services = create_game_services()
        game_state = initialize_game(services)
        game_controller = GameController(services)
        
        # Главный игровой цикл
        while not game_controller.is_game_over(game_state):
            # Выводим текущее состояние
            console_io.print_board(game_state.board)
            console_io.print_score(game_state.get_score())
            
            # Читаем ход игрока
            try:
                cell1, cell2 = console_io.read_move()
                
                # Выполняем ход
                success = game_controller.perform_move(game_state, cell1, cell2)
                
                if success:
                    console_io.print_move_result(True)
                else:
                    console_io.print_move_result(False)
                
                # Обновляем доступность ходов
                game_controller.update_moves_available(game_state)
                
            except KeyboardInterrupt:
                print("\n\nИгра прервана пользователем.")
                return
            except Exception as e:
                console_io.print_error(str(e))
        
        # Игра завершена
        console_io.print_board(game_state.board)
        console_io.print_score(game_state.get_score())
        console_io.print_game_over()
        
        # Спрашиваем, хочет ли игрок играть снова
        if not console_io.ask_play_again():
            break
    
    print("\nСпасибо за игру! До свидания!")


if __name__ == "__main__":
    try:
        play_game()
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        print("Игра завершена.")
