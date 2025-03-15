import csv
import io
from collections.abc import Sequence

from backend.application import interfaces
from backend.domain.entities.admin import FullBuyOrder
from backend.domain.entities.order import SellOrder


class CsvCreator(
    interfaces.CsvCreator,
):
    @staticmethod
    def _generate_order_row(order: [SellOrder, FullBuyOrder]) -> list:
        if isinstance(order, SellOrder):
            return [
                order.id,
                order.fiat_amount,
                order.crypto_amount,
                order.ticker,
                order.status,
                order.created_at,
                order.completed_at,
                order.note,
                order.user_requisites.card_number,
                order.service_requisites.address,
            ]
        if isinstance(order, FullBuyOrder):
            return [
                order.order.id,
                order.order.fiat_amount,
                order.order.crypto_amount,
                order.order.ticker,
                order.order.status,
                order.order.created_at,
                order.order.completed_at,
                order.order.note,
                order.order.user_requisites.address,
                order.card.number.card_number,
            ]

    def create_report(self, orders: Sequence[SellOrder | FullBuyOrder]) -> bytes:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            [
                'ID',
                'Сумма(RUB)',
                'Сумма(USDT)',
                'Пара',
                'Статус',
                'Создан в',
                'Выполнен в',
                'Примечание',
                'Реквизиты пользователя',
                'Реквизиты сервиса',
            ],
        )

        for order in orders:
            writer.writerow(self._generate_order_row(order))

        return output.getvalue().encode('utf-8')
