from dataclasses import dataclass, asdict, fields
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

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
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M = 100
    MIN_IN_H = 60
    KMH_IN_MSEC = round(CM_IN_M * 10 / (MIN_IN_H ** 2), 3)

    height: float

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                / (self.height / self.CM_IN_M)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight
            )
            * self.duration * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    count_pool: int
    length_pool: float

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (
                self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


# TRAIN_CLASS_COUNT_TYPES = {
#    'RUN': (Running, len(fields(Running))),
#    'WLK': (SportsWalking, len(fields(SportsWalking))),
#    'SWM': (Swimming, len(fields(Swimming)))
# }
# я не стал так соединять словари, потому что
# не знаю как потом обратиться только к len(fields(...)),
# а не всему кортежу


COUNT_TYPES: dict = {
    'RUN': len(fields(Running)),
    'WLK': len(fields(SportsWalking)),
    'SWM': len(fields(Swimming))
}

TRAIN_CLASS: dict = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}

error_message_1 = 'В словаре {} нет такого значения'
error_message_2 = (
    'Количество входных параметров ({}) в тренировке {} не совпадает'
    ' с известным количеством полей в классе ({})'
)

values_count_types = COUNT_TYPES.values()


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAIN_CLASS:
        raise KeyError(
            error_message_1.format(TRAIN_CLASS)
        )
    return (
        TRAIN_CLASS[workout_type](*data)
    )
    if len(*data) != values_count_types:
        raise ValueError(
            error_message_2.format(COUNT_TYPES[Training], data, len(data))
        )


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(
            read_package
            (
                workout_type,
                data
            )
        )
