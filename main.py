from data import db_session
from data.users import User


def main():
    db_session.global_init("db/blogs.db")

    users = [
        ["Scott", "Riddley", 21, 'captain', 'research engineer', 'module_1', "scott_chief@mars.org"],
        ["Scott2", "Riddley", 22, 'not captain', 'research engineer', 'module_2', "scott2_chief@mars.org"],
        ["Scott3", "Riddley", 23, 'not captain', 'research engineer', 'module_3', "scott3_chief@mars.org"],
        ["Scott4", "Riddley", 24, 'not captain', 'research engineer', 'module_4', "scott4_chief@mars.org"],
    ]

    db_sess = db_session.create_session()

    for surname, name, age, position, speciality, address, email in users:
        new_user = User()
        new_user.surname = surname
        new_user.name = name
        new_user.age = age
        new_user.position = position
        new_user.speciality = speciality
        new_user.address = address
        new_user.email = email
        db_sess.add(new_user)

    db_sess.commit()


if __name__ == '__main__':
    main()
