import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    all=[]
    
    def __init__(self, name, breed):
        self.id= None
        self.name=name
        self.breed=breed


    @classmethod
    def create_table(cls):
        sql="""
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
      
          """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql="""
            DROP TABLE IF EXISTS dogs
        """
        # Execute the SQL statement
        CURSOR.execute(sql)
        # Commit the changes
        CONN.commit()

    def save(self):
        sql="""
            INSERT INTO dogs (name, breed)
            VALUES (?,?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        # Commit the changes
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog= Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog= cls(row[1],row[2])
        dog.id=row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql="""SELECT * FROM dogs"""

        all_dogs= CURSOR.execute(sql).fetchall()
        cls.all=[cls.new_from_db(row) for row in all_dogs]

    @classmethod
    def find_by_name(cls, name):
        sql="""
            SELECT * FROM dogs WHERE name=? LIMIT 1
        """
        dog= CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, dog_id):
        sql="""SELECT * FROM dogs WHERE id=? LIMIT 1"""
        dog_data= CURSOR.execute(sql, (dog_id,)).fetchone()
        return cls.new_from_db(dog_data)
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name=?, breed=?
            WHERE id=?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

