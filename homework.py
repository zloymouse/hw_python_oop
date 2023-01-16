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

    MESSAGE_TEMPLATE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


M_IN_KM = 1000
MIN_IN_H = 60


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = M_IN_KM
    MIN_IN_H = MIN_IN_H

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

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


@dataclass
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
            * self.weight / M_IN_KM * self.duration * MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M = 100
    KMH_IN_MSEC = round(M_IN_KM / (MIN_IN_H ** 2), 3)

    height: float

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                / (self.height / self.CM_IN_M)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight
            )
            * self.duration * MIN_IN_H
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
            / M_IN_KM
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


TRAIN_CLASSES_COUNT_TYPES = {
    'RUN': [Running, len(fields(Running))],
    'WLK': [SportsWalking, len(fields(SportsWalking))],
    'SWM': [Swimming, len(fields(Swimming))]
}


ERROR_MESSAGE_MISS = 'Тренировка {} оказалась неожиданной'
ERROR_WRONG_NUMBER = (
    'Количество входных параметров ({}) в тренировке {} не совпадает'
    ' с известным количеством полей в этой тренировке'
)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAIN_CLASSES_COUNT_TYPES.keys():
        raise ValueError(
            ERROR_MESSAGE_MISS.format(workout_type)
        )
    if len(data) != TRAIN_CLASSES_COUNT_TYPES[workout_type][1]:
        raise ValueError(
            ERROR_WRONG_NUMBER.format(
                len(data),
                TRAIN_CLASSES_COUNT_TYPES[workout_type][0]
            )
        )
    return (
        TRAIN_CLASSES_COUNT_TYPES[workout_type][0](*data)
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
