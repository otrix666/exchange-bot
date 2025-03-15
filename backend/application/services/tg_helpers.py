from backend.application import interfaces


def get_file_id_by_content_type(message: interfaces.Message):
    if message.content_type == 'photo':
        return message.photo[0].file_id
    if message.content_type == 'animation':
        return message.animation.file_id
    if message.content_type == 'video':
        return message.video.file_id
    if message.content_type == 'document':
        return message.document.file_id


def get_spam_keyboard(message_text: str, kb_builder: interfaces.AdminKeyboardBuilder) -> interfaces.Keyboard:
    if '|' not in message_text:
        return kb_builder.get_close_kb()

    parts = message_text.split('|')
    if len(parts) < 2:
        return kb_builder.get_close_kb()

    title, url = parts[0], parts[1]
    if 'http' in url:
        return kb_builder.get_custom_kb(text=title, url=url)

    return kb_builder.get_close_kb()
