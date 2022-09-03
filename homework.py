from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает строку сообщения о выполненной тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: { self.duration:.3f} ч.; '
                f'Дистанция: { self.distance:.3f} км; '
                f'Ср. скорость: { self.speed:.3f} км/ч; '
                f'Потрачено ккал: { self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите формулу расчета калорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    COEF_RUN_1: int = 18
    COEF_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.COEF_RUN_1 * self.get_mean_speed() - self.COEF_RUN_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_SPRT_WLK_1: float = 0.035
    COEF_SPRT_WLK_2: int = 2
    COEF_SPRT_WLK_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        return ((self.COEF_SPRT_WLK_1 * self.weight
                + (self.get_mean_speed() ** self.COEF_SPRT_WLK_2
                 // self.height) * self.COEF_SPRT_WLK_3 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_SWM_1: float = 1.1
    COEF_SWM_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.COEF_SWM_1)
                * self.COEF_SWM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings_dict = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking
                      }
    if workout_type not in trainings_dict:
        raise ValueError(f'Неизвестный тип тренировки {workout_type}')
    return trainings_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
