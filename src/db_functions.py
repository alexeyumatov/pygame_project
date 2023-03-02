import sqlite3


conn = sqlite3.connect('database/gameconfig.db')
cursor = conn.cursor()


def coins_select(player_id):
    res = cursor.execute("""SELECT coins_amount FROM player_stats 
    WHERE id = ?""", (player_id, )).fetchall()
    return res[0][0]


def bullets_damage_select(player_id):
    res = cursor.execute("""SELECT bullet_damage FROM bullet_stats 
    WHERE player_id = ?""", (player_id, )).fetchall()
    return res[0][0]


def bullet_is_collidable_select(player_id):
    res = cursor.execute("""SELECT bullet_is_collidable FROM bullet_stats 
    WHERE player_id = ?""", (player_id, )).fetchall()
    return res[0][0]


def levels_amount_select(player_id):
    res = cursor.execute("""SELECT levels_passed FROM player_stats 
    WHERE id = ?""", (player_id, )).fetchall()
    return res[0][0]


def shield_points_select(player_id):
    res = cursor.execute("""SELECT shield_points FROM player_stats 
    WHERE id = ?""", (player_id, )).fetchall()
    return res[0][0]


def bullet_cooldown_select(player_id):
    res = cursor.execute("""SELECT bullet_cooldown FROM bullet_stats 
    WHERE player_id = ?""", (player_id, )).fetchall()

    processed_result = 0
    if res[0][0] == 1:
        processed_result = 60
    elif res[0][0] == 2:
        processed_result = 50
    elif res[0][0] == 3:
        processed_result = 40
    elif res[0][0] == 4:
        processed_result = 35
    return [res[0][0], processed_result]


def stamina_select(player_id):
    res = cursor.execute("""SELECT stamina FROM player_stats WHERE id = ?""",
                         (player_id, )).fetchall()
    return res[0][0]


def coins_update(player_id, coins_amount):
    cursor.execute("""UPDATE player_stats
                    SET coins_amount = coins_amount + ?
                    WHERE id = ?""", (coins_amount, player_id))
    conn.commit()


def stamina_update(player_id, stamina_amount):
    cursor.execute("""UPDATE player_stats
                    SET stamina = stamina + ?
                    WHERE id = ?""", (stamina_amount, player_id))
    conn.commit()


def bullets_damage_update(player_id):
    cursor.execute("""UPDATE bullet_stats
                    SET bullet_damage = bullet_damage + 5
                    WHERE player_id = ?""", (player_id, ))
    conn.commit()


def bullet_is_collided_update(player_id):
    cursor.execute("""UPDATE bullet_stats
                    SET bullet_is_collidable = TRUE
                    WHERE player_id = ?""", (player_id, ))
    conn.commit()


def levels_amount_update(player_id):
    cursor.execute("""UPDATE player_stats
                    SET levels_passed = levels_passed + 1
                    WHERE id = ?""", (player_id, ))
    conn.commit()


def bullet_cooldown_update(player_id):
    cursor.execute("""UPDATE bullet_stats
                    SET bullet_cooldown = bullet_cooldown + 1
                    WHERE player_id = ?""", (player_id, ))
    conn.commit()


def shield_points_update(player_id):
    cursor.execute("""UPDATE player_stats
                    SET shield_points = shield_points + 10
                    WHERE id = ?""", (player_id, ))
    conn.commit()


# SETTINGS
def tips_select():
    res = cursor.execute("""SELECT tips_enabled FROM settings""").fetchall()
    return res[0][0]


def tips_update(enabled):
    cursor.execute("""UPDATE settings
                    SET tips_enabled = ?""", (False if enabled else True, ))
    conn.commit()


def music_select():
    res = cursor.execute("""SELECT music FROM settings""").fetchall()
    return res[0][0]


def music_update(enabled):
    cursor.execute("""UPDATE settings
                    SET music = ?""", (False if enabled else True, ))
    conn.commit()


def hands_detection_select():
    res = cursor.execute("""SELECT hands_detection FROM settings""").fetchall()
    return res[0][0]


def hands_detection_update(enabled):
    cursor.execute("""UPDATE settings
                    SET hands_detection = ?""", (False if enabled else True, ))
    conn.commit()
