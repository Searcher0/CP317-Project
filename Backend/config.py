
class Config:
    DB_HOST = 'srv1207.hstgr.io'
    DB_USER = 'u593794933_grocery_guru'
    DB_PASSWORD = 'Grocery_guru1'
    DB_NAME = 'u593794933_grocery_guru'  # Specify the name of the database to use

    # Construct the full database URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False