from backend.domain.entities.admin import FullBuyOrder
from backend.domain.entities.card import Card
from backend.domain.entities.order import BuyOrder
from backend.domain.entities.user import User
from backend.domain.vo.requisites import CardRequisites, UsdtRequisites


class BuyOrderMapper:
    @staticmethod
    def result_to_entity(result: dict) -> BuyOrder:
        return BuyOrder(
            id=result['id'],
            crypto_amount=result['crypto_amount'],
            fiat_amount=result['fiat_amount'],
            ticker=result['ticker'],
            status=result['status'],
            created_at=result['created_at'],
            completed_at=result['completed_at'],
            note=result['note'],
            user_requisites=UsdtRequisites(address=result['user_requisites']),
            card_id=result['card_id'],
            user_id=result['user_id'],
            cheque_id=result['cheque_id'],
        )


class FullBuyOrderMapper:
    @staticmethod
    def result_to_entity(result: dict) -> FullBuyOrder:
        return FullBuyOrder(
            order=BuyOrder(
                id=result['order_id'],
                crypto_amount=result['crypto_amount'],
                fiat_amount=result['fiat_amount'],
                ticker=result['ticker'],
                status=result['status'],
                created_at=result['order_created_at'],
                completed_at=result['completed_at'],
                note=result['note'],
                user_requisites=UsdtRequisites(address=result['user_requisites']),
                card_id=result['order_card_id'],
                user_id=result['order_user_id'],
                cheque_id=result['cheque_id'],
            ),
            user=User(
                id=result['user_id'],
                username=result['username'],
                full_name=result['full_name'],
                is_banned=result['is_banned'],
                created_at=result['user_created_at'],
            ),
            card=Card(
                id=result['card_id'],
                number=CardRequisites(card_number=result['number']),
                user_id=result['operator_id'],
                is_deleted=result['is_deleted'],
            ),
        )
