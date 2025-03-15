from backend.application import interfaces


class AccessManager(
    interfaces.AccessManager,
):
    @staticmethod
    def is_admin(user_id: int, admin_ids: list[int]) -> bool:
        return user_id in admin_ids

    @staticmethod
    def is_operator(user_id: int, operator_ids: list[int]) -> bool:
        return user_id in operator_ids
