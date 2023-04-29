# Как создаётся модуль?

- В файле нужно объявить класс который наследуется от `loader.Module`

```python
from .. import loader, utils


class Example(loader.Module):
    pass

```

# Когда мы объявили класс, можно начинать писать сам модуль

- Класс должен иметь словарь `strings` с ключом `name`
- В этом ключе должно находиться название модуля
- Также **Netfoll** поддерживает динамические переводы, однако:
    - `name` должен быть только в `strings`, его не нужно переводить на другие языки 

- Пример:

```python
from .. import loader, utils

class ExampleMod(loader.Module):
    """Module doc"""

    strings = {
        "name": "Example",
        "text": "Example text",
    }

    strings_ru = {
        "text": "Пример текста",
    }

    strings_uk = {
        "text": "Приклад тексту",
    }

```

# Создаём команды

- Есть 2 способа создать команду:

    - Через декоратор `loader.command`
    - Добавить `cmd` в конец названия метода

- Я буду использовать декоратор

```python

class ExampleMod(loader.Module):
    """Module doc"""

    strings = {
        "name": "Example",
        "text": "Example text",
    }

    strings_ru = {
        "text": "Пример текста",
    }

    strings_uk = {
        "text": "Приклад тексту",
    }

    @loader.command()
    async def example(self, message):
        """Command doc"""

        await utils.answer(message, self.strings["text"])

```

- `utils.answer` это функция, аналогичная `message.edit` но:

    - Если в сообщении больше 4096 сивмолов, то будет создан инлайн список
    - Юзербот ответит на сообщение, если его отправил другой человек, а не владелец аккаунта

- Юзербот заменяет словарь `strings` на словарь с нужным языком, поэтому мы всегда обращаемся к `strings`