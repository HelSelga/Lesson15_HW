from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


DATABASE_PATH = 'animal.db'


def serialize_row(row: sqlite3.Row):
    return {key: row[key] for key in row.keys()}


@app.route('/<animal_id>')
def get_info(animal_id):
    query = (""
             "SELECT * "
             "FROM new_animals "
             "WHERE animal_id = :1 "
        )

    connection: sqlite3.Connection = app.config['db']
    cursor = connection.cursor()
    cursor.execute(query, (animal_id, ))
    row = cursor.fetchone()
    cursor.close()

    return jsonify(serialize_row(row))


@app.route('/<animal_id>/full')
def get_info_full(animal_id):
    query = ("""
        SELECT
            new_animals.id 
            age_upon_outcome,
            animal_id,
            new_animals.name,
            date_of_birth,
            outcome_month,
            outcome_year,
            animal_type.name as 'type',
            animal_breed.name as 'breed',
            animal_color1.name as 'color1',
            animal_color2.name as 'color2',
            outcome_subtype.name as 'outcome_subtype',
            outcome_subtype.name as 'outcome_subtype' 
        FROM new_animals 
        LEFT JOIN animal_type ON animal_type.id = new_animals.type_id
        LEFT JOIN animal_breed ON animal_breed.id = new_animals.breed_id
        LEFT JOIN animal_color as animal_color1 ON animal_color1.id = new_animals.color1_id
        LEFT JOIN animal_color as animal_color2 ON animal_color2.id = new_animals.color2_id
        LEFT JOIN outcome_subtype ON outcome_subtype.id = new_animals.outcome_subtype_id
        LEFT JOIN outcome_type ON outcome_type.id = new_animals.outcome_type_id
        WHERE new_animals.animal_id = :1
    """)

    connection: sqlite3.Connection = app.config['db']
    cursor = connection.cursor()
    cursor.execute(query, (animal_id,))
    row = cursor.fetchone()
    cursor.close()

    return jsonify(serialize_row(row))


if __name__ == "__main__":
    con = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    app.config['db'] = con
    try:
        app.run()
    except KeyboardInterrupt:
        con.close()
