from src.functions import load_image, flip, main_melody
from src.groups import *
from src.objects import Bullet, UltimateAttack
from src.db_functions import coins_update, shield_points_select, stamina_select, \
    bullet_cooldown_select

g = 10


class Player(pygame.sprite.Sprite):
    idle_images = [
        load_image(f'hero/hero_static/'
                   f'Player_Static_Animation_{i}.png') for i in range(1, 7)]

    walk_images = [
        load_image(f'hero/hero_walk/'
                   f'Player_Walk_Animation_{i}.png') for i in range(1, 11)]

    death_images = [load_image(f"hero/"
                               f"hero_death/{i}.png") for i in range(1, 13)]

    damaged_images = [load_image(f"hero/"
                                 f"hero_damaged/{i}.png") for i in range(1, 4)]

    def __init__(self, x, y):
        super().__init__(player_group)
        self.counter = 0
        self.image = Player.idle_images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x, self.rect.y = x * 128, y * 128
        self.width, self.height = self.image.get_width(), \
                                  self.image.get_height()

        self.velx, self.vely, self.ladder_vely = 0, 0, 0  # velocity vars

        self.health_points = 100
        self.stamina = stamina_select(1)
        self.shield_points = shield_points_select(1)
        self.coins_collected = 0
        self.isPoisoned = False
        self.poison_cooldown = 0
        self.able_to_heal = False

        self.animCount = 0
        self.death_animCount = 0
        self.death_time = 0
        self.death_anim = False
        self.view, self.isFlipped = "right", False
        self.state = False
        self.OnGround, self.onLadder, self.ladder_hit = False, False, False
        self.inJump = False

        self.dash = False
        self.dash_cooldown = 0

        self.is_killed = False
        self.able_to_shoot = True  # checks if the hero is able to shoot
        self.shoot_cooldown = 120

        self.end_movement = False  # activates when hero is
        # collided with the portal
        self.end_distance = 0  # var for stopping the hero in the
        # middle of the portal

        self.bullet_onScreen = False
        self.bulletList = []

    # collide_group
    def update(self):
        # DEATH ANIMATION AND COOLDOWN
        if self.death_anim:
            if self.death_time < 60:
                self.death_time += 1
                self.death()
            elif self.death_time >= 60:
                self.is_killed = True
        else:
            vl_x, vl_y = 0, 0
            ladder_vl_y = 0  # extra speed vars

            # BULLET COOLDOWN
            self.shoot_cooldown += 1

            # DASH COOLDOWN
            self.dash_cooldown += 1

            # POISON COOLDOWN
            self.poison_cooldown += 1

            # HERO MOVEMENT
            if not self.end_movement:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE] and not self.inJump and \
                        not self.onLadder and self.OnGround:
                    vl_y = -2
                    self.inJump = True
                    self.OnGround = False

                if key[pygame.K_a] and not key[pygame.K_d]:
                    if self.velx > 0:
                        self.velx = 0
                    self.velx -= 0.5
                    if self.velx <= -14:
                        self.velx = -14
                    vl_x += self.velx
                    self.animCount += 1
                    self.view = 'left'
                    self.state = True

                if key[pygame.K_d]:
                    if self.velx < 0:
                        self.velx = 0
                    self.velx += 0.5
                    if self.velx >= 14:
                        self.velx = 14
                    vl_x += self.velx
                    self.animCount += 1
                    self.view = 'right'
                    self.isFlipped, self.state = False, True

                if not key[pygame.K_d] and not key[pygame.K_a]:
                    self.state = False
                    if self.velx > 0:
                        self.velx -= 2
                        if self.velx <= 0:
                            self.velx = 0
                    elif self.velx < 0:
                        self.velx += 2
                        if self.velx >= 0:
                            self.velx = 0
                    vl_x += self.velx

                    # IDLE ANIMATION
                    if not self.onLadder:
                        if self.animCount + 1 >= 42:
                            self.animCount = 0

                        self.image = Player.idle_images[self.animCount // 7]
                        if self.view == 'left':
                            self.image = flip(self.image)

                        self.animCount += 1

                # LADDER PHYSICS
                if self.onLadder:
                    self.image = Player.idle_images[0]
                    if self.view == 'left':
                        self.image = flip(self.image)

                    if key[pygame.K_w]:
                        self.ladder_vely -= 0.5
                        if self.ladder_vely <= -10:
                            self.ladder_vely = -10
                        ladder_vl_y += self.ladder_vely

                    if key[pygame.K_s] and not self.ladder_collide and \
                            not key[pygame.K_w]:
                        self.ladder_vely += 0.5
                        if self.ladder_vely >= 10:
                            self.ladder_vely = 10
                        ladder_vl_y += self.ladder_vely
                    if not key[pygame.K_s] and not key[pygame.K_w]:
                        if self.ladder_vely > 0:
                            self.ladder_vely -= 2
                            if self.ladder_vely <= 0:
                                self.ladder_vely = 0
                            ladder_vl_y += self.ladder_vely
                        if self.ladder_vely < 0:
                            self.ladder_vely += 2
                            if self.ladder_vely >= 0:
                                self.ladder_vely = 0
                            ladder_vl_y += self.ladder_vely

                # WALKING ANIMATION
                if self.view == "left" and not self.isFlipped:
                    self.image = flip(self.image)
                    self.isFlipped = True

                if self.state and not self.onLadder:
                    if self.animCount + 1 >= 60:
                        self.animCount = 0

                    self.image = Player.walk_images[self.animCount // 6]

                    if self.view == "left":
                        self.image = flip(self.image)

                    self.animCount += 1

                # GRAVITY
                if not self.onLadder and not self.inJump:
                    self.vely += 1
                    if self.vely > 10:
                        self.vely = 10
                    vl_y += self.vely
                else:
                    self.rect.y += ladder_vl_y

                # POISON CHECK
                if self.isPoisoned:
                    if self.poison_cooldown % 60 == 0:
                        self.damage(5, from_poison=True)
                        self.poison_cooldown = 0

                if self.dash and not self.onLadder and self.dash_cooldown > 60:
                    self.counter += 1
                    if self.counter == 8:
                        self.dash = False
                        self.dash_cooldown = 0
                        self.counter = 0
                    else:
                        if self.view == 'right':
                            vl_x += 20
                            self.velx = 14
                        else:
                            vl_x -= 20
                            self.velx = -14
                else:
                    self.counter = 0

                # COLLIDERS
                for tile in tiles_group:
                    if tile.rect.colliderect(self.rect.x + vl_x, self.rect.y,
                                             self.width, self.height):
                        vl_x = 0
                        self.velx = 0
                    if tile.rect.colliderect(self.rect.x, self.rect.y + vl_y,
                                             self.width, self.height):
                        if self.vely < 0:
                            vl_y = tile.rect.bottom - self.rect.top
                            self.vely = 0
                        elif self.vely >= 0:
                            vl_y = tile.rect.top - self.rect.bottom
                            self.OnGround = True
                            self.vely = 0
                            self.inJump = False

                # LADDER COLLIDE
                ladder_collision = pygame.sprite.spritecollideany(self,
                                                                  ladder_group)
                if ladder_collision:
                    self.ladder_hit = True
                else:
                    self.ladder_hit = False

                # FOUNTAIN COLLIDE
                collide = pygame.sprite.spritecollideany(self, fountain_group)
                if collide:
                    self.able_to_heal = True
                else:
                    self.able_to_heal = False

                # ENEMY COLLIDE (if the player touches the enemy,
                # then he cannot shoot)
                for tile in enemies_group:
                    if tile.rect.colliderect(self.rect):
                        self.able_to_shoot = False
                        if self.dash:
                            tile.incoming_damage(20)
                    else:
                        self.able_to_shoot = True

                # COIN COLLIDE
                if pygame.sprite.spritecollide(self, coins_group, True):
                    self.coins_collected += 1

                # PHYSICS REALISATION
                if self.inJump:
                    self.vely -= 2
                    if self.vely <= -10:
                        self.vely = -10
                        self.inJump = False
                    vl_y += self.vely

                self.rect.x += vl_x
                if vl_y < -150:
                    vl_y = 10
                self.rect.y += vl_y

            # PORTAL COLLIDERS
            for tile in portal_group:
                if tile.rect.colliderect(self.rect.x + vl_x, self.rect.y,
                                         self.width, self.height):
                    self.end_movement = True
                    if self.portal_collide():
                        main_melody()
                        return True
                else:
                    self.end_movement = False

            return False

    def shoot(self):
        if self.able_to_shoot:
            if self.shoot_cooldown >= bullet_cooldown_select(1)[1]:
                if self.view == "left":
                    ratio = -30
                else:
                    ratio = 150
                bullet = Bullet(self.rect.x + ratio, self.rect.y + 145,
                                self.view, all_sprites, bullets)
                self.bulletList.append(bullet)
                self.bullet_onScreen = True
                self.shoot_cooldown = 0
            if len(self.bulletList) >= 1:
                return None

    def ultimate(self):
        if self.able_to_shoot:
            if self.view == "left":
                ratio = -30
            else:
                ratio = 150
            ultimate = UltimateAttack(self.rect.x + ratio, self.rect.y + 140,
                                      self.view, all_sprites, bullets)
            self.bulletList.append(ultimate)
            self.bullet_onScreen = True

    def bullet_update(self):
        if self.bullet_onScreen:
            for el in self.bulletList:
                state = el.update()
                if state == 'killed':
                    self.bulletList.remove(el)
            if len(bullets) == 0:
                self.bullet_onScreen = False

    def ladder_climb(self, collide_group, floor_group):
        hits = pygame.sprite.spritecollide(self, collide_group, False)
        if not hits:
            self.onLadder = False
            self.OnGround = False
            return False
        else:
            for el in collide_group:
                hits_mask = pygame.sprite.collide_mask(self, el)
                if hits_mask:
                    self.onLadder = True
                    if pygame.sprite.spritecollide(self, floor_group, False):
                        self.ladder_collide = True
                    else:
                        self.ladder_collide = False
                    return True
                else:
                    self.onLadder = False

    def damage(self, damage_amount, from_poison=False):
        if self.shield_points > 0 and not from_poison:
            self.shield_points -= damage_amount
            if self.shield_points < 0:
                self.health_points += self.shield_points
        else:
            self.health_points -= damage_amount
        if self.shield_points < 0:
            self.shield_points = 0
        if self.health_points <= 0:
            self.health_points = 0
            self.death_anim = True

    def portal_collide(self):
        vl_x = 0
        if self.view == 'left':
            vl_x = -1
        elif self.view == 'right':
            vl_x = 1
        if abs(self.end_distance) >= 100:
            coins_update(1, self.coins_collected)
            return True
        self.rect.x += vl_x
        self.end_distance += vl_x
        return False

    def death(self):
        if self.death_animCount >= 60:
            self.death_animCount = 0

        self.image = self.death_images[self.death_animCount // 5]
        if self.view == 'left':
            self.image = flip(self.image)

        self.death_animCount += 1

