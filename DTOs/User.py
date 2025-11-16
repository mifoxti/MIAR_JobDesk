class User:
    def __init__(self, id: int, first_name: str,
     last_name: str, middle_name: str, email: str, phone: str, order_count: int,
     balance: float, registration_date: str, last_login: str,
     is_active: bool, password: str, rating: float = 0.0):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._middle_name = middle_name
        self._email = email
        self._phone = phone
        self._password = password
        self._order_count = order_count
        self._balance = balance
        self._registration_date = registration_date
        self._last_login = last_login
        self._is_active = is_active
        self._rating = rating
    

    def to_dict(self):
        return {
            "id": self._id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "middle_name": self._middle_name,
            "email": self._email,
            "phone": self._phone,
            "order_count": self._order_count,
            "balance": self._balance,
            "registration_date": self._registration_date,
            "last_login": self._last_login,
            "is_active": self._is_active,
            "rating": self._rating
        }
