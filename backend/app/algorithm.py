from typing import List

from sqids import Sqids


class HashingAlgorithm:
    def __init__(self, salt: str = "", min_length: int = 6,
                 alphabet: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'):
        self.salt = salt
        self.alphabet = self.__reorder_alphabet(alphabet, salt)
        self.min_length = min_length
        self.hashing_func = Sqids(alphabet=self.alphabet, min_length=self.min_length)

    @staticmethod
    def __reorder_alphabet(alphabet: str, salt: str) -> str:
        """
        Reorders 'input_alphabet' according to given 'input_salt'.
        :param alphabet: string
        :param salt: string
        :return: string
        """
        salt_length: int = len(salt)
        alphabet_list: List[str] = list(alphabet)

        if salt_length == 0:
            return alphabet

        current_index: int = 0
        sum_of_integers: int = 0

        for i in range(len(alphabet_list) - 1, 0, -1):
            current_integer: int = ord(salt[current_index])
            sum_of_integers += current_integer
            j: int = (current_integer + current_index + sum_of_integers) % i
            alphabet_list[i], alphabet_list[j] = alphabet_list[j], alphabet_list[i]
            current_index = (current_index + 1) % salt_length

        reordered_alphabet = ''.join(alphabet_list)
        return reordered_alphabet

    def encode(self, number: int) -> str:
        """
        :param number: int - ID of a record corresponding to URL.
        :return: str - Obfuscated short string corresponding to the integer (ID of a record).
        """
        if not isinstance(number, int):
            raise TypeError("Input must be an integer.")
        return self.hashing_func.encode([number])

    def decode(self, text: str) -> int:
        """
        :param text: str - Encoded string.
        :return: int - ID of a record corresponding to URL.
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")
        number = self.hashing_func.decode(text)
        return int(number[0]) if len(number) > 0 else None
