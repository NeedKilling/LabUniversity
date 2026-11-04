# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ (основа для студента).

Перепишите клиента блокчейн-сети на ООП. Нужно реализовать два класса —
Block и StudentClient — и дописать методы, помеченные «# TODO».
Обязательные условия:
  1) вся логика оформлена через классы и методы (ООП);
  2) при создании объектов используйте и ИМЕНОВАННЫЕ (keyword), и
     НЕИМЕНОВАННЫЕ (позиционные) аргументы;
  3) в блоке должны быть ваши ФАМИЛИЯ и ГРУППА;
  4) сервер teacher_server.py менять НЕЛЬЗЯ.

Запуск:
    pip install requests
    python student_client_task.py
"""
import hashlib
import time
import requests


class Block:
    """Один блок цепочки. Хранит данные и умеет считать свой хэш и майнить."""
    NUM_ZEROS = 4   # сложность Proof-of-Work (должно совпадать с сервером)

    def __init__(self, index, surname, group, prev_hash,
                 message="Привет, блокчейн!", timestamp=None, nonce=0):
        self.index = index
        self.surname = surname
        self.group = group
        self.message = message
        self.prev_hash = prev_hash
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.nonce = nonce
        self.hash = None

    @property
    def data(self):
        """Данные блока одной строкой (фамилия, группа, сообщение). НЕ менять формат!"""
        return f"{self.surname}, группа {self.group} — {self.message}"

    def header(self):
        """Заголовок для хэширования. Формат ДОЛЖЕН совпадать с сервером — не менять."""
        return f"{self.index}|{self.prev_hash}|{self.data}|{self.timestamp}|{self.nonce}"

    def calc_hash(self):
        """Возвращает SHA-256 (hexdigest) от self.header(), закодированного в utf-8."""
        return hashlib.sha256(self.header().encode('utf-8')).hexdigest()

    def mine(self):
        """Proof-of-Work"""
        target = '0' * Block.NUM_ZEROS
        while True:
            h = self.calc_hash()
            if h.startswith(target):
                self.hash = h
                return self.nonce, self.hash
            self.nonce += 1

    def to_dict(self):
        """Возвращает словарь блока со всеми полями, которые ждёт сервер."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "surname": self.surname,
            "group": self.group,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class StudentClient:
    """Клиент студента: общается с сервером преподавателя и присоединяет блок."""

    def __init__(self, server_url, surname, group):
        url = server_url.strip().rstrip("/")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.server = url
        self.surname = surname
        self.group = group

    def get_last_block(self):
        """GET /last_block — последний блок цепочки (готовый метод)."""
        return requests.get(f"{self.server}/last_block", timeout=10).json()

    def create_block(self, last, message):
        """Создаёт и возвращает объект Block, идущий за блоком last.
        Используются позиционные аргументы (index, surname, group, prev_hash)
        и именованный (message)."""
        index = last["index"] + 1
        prev_hash = last["hash"]
        return Block(index, self.surname, self.group, prev_hash, message=message)

    def submit(self, block):
        """Отправляет блок на сервер методом POST /add_block.
        Возвращает (status_code, ответ-JSON)."""
        r = requests.post(f"{self.server}/add_block", json=block.to_dict(), timeout=10)
        return r.status_code, r.json()

    def show_chain(self):
        """Показать текущую цепочку преподавателя (готовый метод)."""
        chain = requests.get(f"{self.server}/chain", timeout=10).json()["chain"]
        print("\nТекущая цепочка преподавателя:")
        for b in chain:
            who = "ГЕНЕЗИС" if b["index"] == 0 else f"{b['surname']} (гр. {b['group']})"
            print(f"  #{b['index']:>2}  {who:<30} hash={b['hash'][:12]}…  prev={b['prev_hash'][:12]}…")

    def run(self, message="Привет, блокчейн!"):
        """Главный сценарий (готов). Вызывает create_block/mine/submit."""
        print(f"Подключаюсь к {self.server}  как  {self.surname} (гр. {self.group})")
        for attempt in range(1, 6):
            last = self.get_last_block()
            block = self.create_block(last, message)
            print(f"[Попытка {attempt}] Майнинг блока #{block.index} … "
                  f"(ищем хэш с {Block.NUM_ZEROS} нулями)")
            nonce, h = block.mine()
            print(f"  Найден nonce={nonce}, hash={h[:20]}…  отправляем преподавателю…")
            status, res = self.submit(block)
            if res.get("accepted"):
                print(f"\n✔ БЛОК ПРИНЯТ! Ваш блок #{res['index']} добавлен в цепочку. "
                      f"Длина цепочки: {res['chain_length']}.")
                break
            print(f"✖ Блок отклонён: {res.get('reason')}")
            if status == 409 and "last_block" in res:
                print("  Цепочка изменилась — перемайниваем…")
                continue
            break
        self.show_chain()


if __name__ == "__main__":
    client = StudentClient(server_url="http://10.39.120.52:5000",
                           surname="Камардин", group="ОКБП-401ИТМП")
    client.run("Мой блок на ООП")