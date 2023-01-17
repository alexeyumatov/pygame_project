import sqlite3


conn = sqlite3.connect('database/gameconfig.db')
cursor = conn.cursor()


def coins_select(player_id):
    res = cursor.execute("""SELECT coins_amount FROM player_stats WHERE id = ?""",
                         (player_id, )).fetchall()
    return res[0][0]


def bullets_amount_select(player_id):
    res = cursor.execute("""SELECT bullets_amount FROM player_stats WHERE id = ?""",
                         (player_id, )).fetchall()
    return res[0][0]


def bullets_damage_select(player_id):
    res = cursor.execute("""SELECT bullet_damage FROM player_stats WHERE id = ?""",
                         (player_id, )).fetchall()
    return res[0][0]


def levels_amount_select(player_id):
    res = cursor.execute("""SELECT levels_passed FROM player_stats WHERE id = ?""",
                         (player_id, )).fetchall()
    return res[0][0]


def coins_update(player_id):
    cursor.execute("""UPDATE player_stats
                    SET coins_amount = coins_amount + 1
                    WHERE id = ?""", (player_id, ))
    conn.commit()


def bullets_amount_update(player_id):
    cursor.execute("""UPDATE player_stats
                    SET bullets_amount = bullets_amount + 1
                    WHERE id = ?""", (player_id, ))
    conn.commit()


def levels_amount_update(player_id):
    cursor.execute("""UPDATE player_stats
                    SET levels_passed = levels_passed + 1
                    WHERE id = ?""", (player_id, ))
    conn.commit()
