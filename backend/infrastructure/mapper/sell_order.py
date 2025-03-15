from backend.domain.entities.admin import FullSellOrder
from backend.domain.entities.order import SellOrder
from backend.domain.entities.user import User
from backend.domain.vo.requisites import CardRequisites, UsdtRequisites


class SellOrderMapper:
    @staticmethod
    def result_to_entity(result: dict) -> SellOrder:
        return SellOrder(
            id=result['id'],
            crypto_amount=result['crypto_amount'],
            fiat_amount=result['fiat_amount'],
            ticker=result['ticker'],
            status=result['status'],
            created_at=result['created_at'],
            completed_at=result['completed_at'],
            note=result['note'],
            user_requisites=CardRequisites(card_number=result['user_requisites']),
            service_requisites=UsdtRequisites(address=result['service_requisites']),
            user_id=result['user_id'],
            cheque_id=result['cheque_id'],
        )


class FullSellOrderMapper:
    @staticmethod
    def result_to_entity(result: dict) -> FullSellOrder:
        return FullSellOrder(
            order=SellOrder(
                id=result['order_id'],
                crypto_amount=result['crypto_amount'],
                fiat_amount=result['fiat_amount'],
                ticker=result['ticker'],
                status=result['status'],
                created_at=result['order_created_at'],
                completed_at=result['completed_at'],
                note=result['note'],
                user_requisites=CardRequisites(card_number=result['user_requisites']),
                service_requisites=UsdtRequisites(address=result['service_requisites']),
                user_id=result['order_user_id'],
                cheque_id=result['cheque_id'],
            ),
            user=User(
                id=result['user_id'],
                username=result['username'],
                full_name=result['full_name'],
                role=result['role'],
                is_banned=result['is_banned'],
                created_at=result['user_created_at'],
            ),
        )
