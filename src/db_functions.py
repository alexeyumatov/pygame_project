import sqlite3


conn = sqlite3.connect('database/gameconfig.db')
cursor = conn.cursor()


def coins_select(player_id):
    res = cursor.execute("""SELECT coins_amount FROM player_stats WHERE id = ?""", (player_id, )).fetchall()
    print(res)
    return res[0]


def coins_update(player_id):
    cursor.execute("""UPDATE player_stats
                    SET coins_amount = coins_amount + 1
                    WHERE id = ?""", (player_id, ))
    conn.commit()
