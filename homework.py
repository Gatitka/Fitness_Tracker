class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
# Числовые значения должны округляться при выводе до тысячных долей
# (до третьего знака после запятой).

    def get_message(self) -> str:
        """Возвращает строку сообщения о выполненной тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: { round(self.duration, 3) } ч.; '
                f'Дистанция: { round(self.distance, 3)} км; '
                f'Ср. скорость: { round(self.speed, 3)} км/ч; '
                f'Потрачено ккал: {round(self.calories, 3)}.'
                )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP: float = 0.65

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
        pass

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

    def get_spent_calories(self) -> float:
        coef_1 = 18
        coef_2 = 20
        return ((coef_1 * self.get_mean_speed() - coef_2)
                * self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coef_1 = 0.035
        coef_2 = 2
        coef_3 = 0.029
        return ((coef_1 * self.weight
                + (self.get_mean_speed() ** coef_2 // self.height)
                * coef_3 * self.weight) * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

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

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coef_swim_1: float = 1.1
        coef_swim_2: int = 2
        return ((self.get_mean_speed() + coef_swim_1)
                * coef_swim_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings_dict = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking
                      }
    return trainings_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
