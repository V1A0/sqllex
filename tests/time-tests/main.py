import cProfile
import pstats
from sqllex import *
from sqllex.debug import debug_mode

LIM = 10000


def init_db():
    db = SQLite3x('time_test.db')


def crete_table(db: SQLite3x):
    db.create_table(
        'main',
        {
            'id': [INTEGER, PRIMARY_KEY, UNIQUE],
            'name': [TEXT],
            'age': [INTEGER, DEFAULT, 33]
        }
    )


def insert_fats(db: SQLite3x):
    for _ in range(LIM):
        db.insert('main', (None, f'Alex', 33))


def insert_slow(db: SQLite3x):
    for _ in range(LIM):
        db.insert('main', (None, 'Alex'))


def insert_many_fast(db: SQLite3x):
    data = [(None, 'Alex', 33) for _ in range(LIM)]

    db.insertmany('main', data)


def insert_many_slow(db: SQLite3x):
    data = [(None, 'Alex') for _ in range(LIM)]

    db.insertmany('main', data)


def select_all(db: SQLite3x):
    db.select_all('main', LIMIT=LIM)


def select_where_1(db: SQLite3x):
    db.select(
        'main', 'id',
        WHERE={
            'name': 'Alex'
        },
        LIMIT=LIM
    )


def select_where_2(db: SQLite3x):
    """
    Modern new way to
    """
    main_tab = db['main']
    id_col = main_tab['id']
    name_col = main_tab['name']

    db.select(
        main_tab, id_col,
        WHERE=(name_col == 'Alex'),
        LIMIT=LIM
    )


if __name__ == '__main__':
    db = SQLite3x('time_test.db')

    db.connect()

    with cProfile.Profile() as pr:
        #                       # total runtime/(records), speedup 0.1.10.4 vs 0.1.10.5c (pre 0.2)
        # crete_table(db)       # 0.00327 sec/(1    table), 1.01x
        # insert_fats(db)       # 0.20000 sec/(10_000 rec), 1.10x
        # insert_slow(db)       # 0.69250 sec/(10_000 rec), 1.34x
        # insert_many_fast(db)  # 0.03473 sec/(10_000 rec), 1.22x
        # insert_many_slow(db)  # 0.04269 sec/(10_000 rec), 1.13x
        # select_all(db)        # 0.01155 sec/(10_000 rec), 3.00x
        # select_where_1(db)    # 0.00691 sec/(10_000 rec), 4.18x
        # select_where_2(db)    # 0.00856 sec/(10_000 rec), 3.00x
        pass

    db.disconnect()

    stat = pstats.Stats(pr)
    stat.sort_stats(pstats.SortKey.TIME)
    stat.dump_stats(filename='time_tst.prof')

