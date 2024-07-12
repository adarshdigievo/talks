class SingletonClass:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


obj1 = SingletonClass()
obj2 = SingletonClass()

print(obj1 is obj2)  # True
print(id(obj1))  # 2402721138768
print(id(obj2))  # 2402721138768
