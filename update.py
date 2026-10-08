def update_app_db(headers, conn, cursor):
    new_header_names = headers

    if "building" not in new_header_names:
        cursor.execute("ALTER TABLE items ADD building TEXT DEFAULT 'home'")
        conn.commit()

    if "room" not in new_header_names:
        cursor.execute("ALTER TABLE items ADD room TEXT DEFAULT 'unknown'")
        conn.commit()

    if "placement" not in new_header_names:
        cursor.execute("ALTER TABLE items ADD placement TEXT DEFAULT 'unknown'")
        conn.commit()

    if "quantity" not in new_header_names:
        cursor.execute("ALTER TABLE items RENAME COLUMN quanity to quantity")
        conn.commit()

    cursor.execute("SELECT * FROM items LIMIT 0")
    new_header_names = [description[0] for description in cursor.description]

    return new_header_names