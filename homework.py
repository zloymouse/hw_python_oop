from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message_template: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.message_template.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    SEC_IN_MINUT: int = 60
    CM_IN_M: int = 100

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
        total_distance: float = (self.action
                                 * self.LEN_STEP
                                 / self.M_IN_KM)
        return total_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training: InfoMessage = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return training


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    CONST: int = 20

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                 + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight
                                 / self.M_IN_KM
                                 * self.duration
                                 * self.MIN_IN_H)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_WEIGHT_MULTIPLIER
                          * self.weight + ((self.get_mean_speed()
                                           * self.KMH_IN_MSEC)
                                           ** 2 / (self.height
                                           / self.CM_IN_M))
                          * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                          * self.weight)
                          * self.duration
                          * self.MIN_IN_H)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        mean_speed_swim = (self.length_pool
                           * self.count_pool
                           / self.M_IN_KM
                           / self.duration)
        return mean_speed_swim

    def get_spent_calories(self) -> float:
        spent_calories_swim = ((Swimming.get_mean_speed(self)
                               + self.CALORIES_MEAN_SPEED_SHIFT)
                               * self.CALORIES_WEIGHT_MULTIPLIER
                               * self.weight
                               * self.duration)
        return spent_calories_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    class_types: Training = train_class[workout_type](*data)
    return class_types


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
