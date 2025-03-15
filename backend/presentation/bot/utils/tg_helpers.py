from aiogram.types import Message


def get_file_id_by_content_type(content_type: str, message: Message):
    if content_type == 'photo':
        return message.photo[0].file_id
    if content_type == 'animation':
        return message.animation.file_id
    if content_type == 'video':
        return message.video.file_id
    if content_type == 'document':
        return message.document.file_id
