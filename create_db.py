from init import Base, engine


def create_tables():
    from tables import products, category, series, user, rule
    Base.metadata.create_all(bind=engine)


def drop_tables():
    from tables import products, category, series, user, rule
    Base.metadata.drop_all(bind=engine)


if __name__ == '__main__':
    drop_tables()
    create_tables()
    print(Base.metadata.tables)

