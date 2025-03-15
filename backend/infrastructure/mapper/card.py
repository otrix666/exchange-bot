from backend.domain.entities.card import Card
from backend.domain.vo.requisites import CardRequisites


class CardMapper:
    @staticmethod
    def result_to_entity(result: dict) -> Card:
        return Card(
            id=result['id'],
            number=CardRequisites(card_number=result['number']),
            user_id=result['user_id'],
            is_deleted=result['is_deleted'],
        )
