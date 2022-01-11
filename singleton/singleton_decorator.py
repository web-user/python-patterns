def singleton(class_):
    instance = {}

    def get_instance(*args, **kwargs):
        if class_ not in instance:
            instance[class_] = class_(*args, **kwargs)
        return instance[class_]

    return get_instance


@singleton
class Database:

    def __init__(self):
        print('Loading database from file')


if __name__ == '__main__':
    d1 = Database()
    d2 = Database()

    print(d1 == d2)
