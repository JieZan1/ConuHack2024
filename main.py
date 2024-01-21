import curses
import time
import random
from curses import wrapper

from Zombie import Zombie
from Player import Player
from Bullet import Bullet


def main(stdscr):
    points = play(stdscr)
    stdscr.clear()

    stdscr.addstr(1, 1, f"GAME OVER Points achieve{points}")
    stdscr.addstr(2, 1, f"Press R to restart, any other keys to quit")
    stdscr.refresh()
    stdscr.nodelay(False)
    time.sleep(2)
    key = stdscr.getkey()

    while key == "r":
        stdscr.clear()

        points = play(stdscr)
        stdscr.addstr(1, 1, f"GAME OVER Points achieve{points}")
        stdscr.addstr(2, 1, f"Press R to restart, any other keys to quit")
        stdscr.refresh()
        stdscr.nodelay(False)
        time.sleep(2)
        key = stdscr.getkey()


def play(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()
    player = Player(5, 5)
    hp = player.hp

    bullets = []
    zombies = []

    spawnrate = 6

    gameover = False
    counter = 0
    points = 0
    counter_tree = 0
    stdscr.clear()
    stdscr.refresh()
    bullet_counter = 0
    fire = True

    reload_timer = 0

    player.update_stance()
    stdscr.addstr(player.y, 0, player.stance)
    stdscr.nodelay(True)

    while True:
        # Make sure wrong input will come out as None
        try:
            key = stdscr.getkey()
        except:
            key = None

        if not gameover:
            if key == "KEY_UP" and player.y > 0:
                player.y -= 1
            elif key == "KEY_DOWN" and player.y + player.height < screen_height - 2:
                player.y += 1
            elif key == " " and fire:

                bullets.append(Bullet(player.width + 1, player.y + 1, 1))
                bullet_counter += 1

        if key == "q":  # exit program
            player.y += 10000

        for bullet in bullets:
            if bullet.x < screen_width - 1:
                bullet.move()
            else:
                bullets.remove(bullet)

        if bullet_counter >= 10:
            fire = False
            reload_timer += 1

            if reload_timer >= 20:
                bullet_counter = 0
                fire = True
        else:
            reload_timer = 0

        if not gameover:
            for zombie in zombies:
                if zombie.x > 0:
                    zombie.move("LEFT")
                    if player.y > zombie.y and zombie.counter >= random.randrange(10, 40):
                        zombie.move("UP")
                        zombie.counter = 0
                    elif player.y < zombie.y and zombie.counter >= random.randrange(10, 40):
                        zombie.move("DOWN")
                        zombie.counter = 0
                else:
                    zombies.remove(zombie)

        time.sleep(0.05)
        if random.getrandbits(1):
            counter += 1
            counter_tree += 1
            for zombie in zombies:
                zombie.counter += 1

        if not gameover:
            if counter == spawnrate:
                zombies.append(Zombie(screen_width - 3, random.randrange(1, screen_height - 5)))
                counter = 0

        stdscr.clear()

        player.update_stance()
        stdscr.addstr(player.y, 0, player.stance)
        for zombie in zombies:
            zombie.update_leg()
            stdscr.addstr(zombie.y, zombie.x, zombie.face)
            stdscr.addstr(zombie.y + 1, zombie.x, zombie.leg)

        for zombie in zombies:
            if zombie.x == player.width:
                if zombie.y == player.y + 1 or zombie.y == player.y or zombie.y == player.y - 1:
                    zombies.remove(zombie)
                    hp -= 1

                    if hp == 0:
                        gameover = True
                        return points

        for bullet in bullets:
            stdscr.addstr(bullet.y, bullet.x, "-")

        for bullet in bullets:
            for zombie in zombies:
                if zombie.x == bullet.x + 1 or zombie.x == bullet.x or zombie.x == bullet.x - 1:
                    if zombie.y == bullet.y + 1 or zombie.y == bullet.y or zombie.y == bullet.y - 1:
                        bullets.remove(bullet)
                        zombies.remove(zombie)
                        points += round(1 / zombie.x * 25 + 5)

        hp_string = "HP: "
        for i in range(player.hp):
            if i < hp:
                hp_string += "▩"
            else:
                hp_string += "▢"

        bullet_string = "Bullets: "
        if reload_timer != 0 and reload_timer % 2 == 0:
            for i in range(reload_timer // 2):
                if i < 10:
                    bullet_string += "-"
                else:
                    bullet_string += " "

        if reload_timer == 20:
            bullet_string = "Bullets: "

        for i in range(10 - bullet_counter):
            if i < 10:
                bullet_string += "|"
            else:
                bullet_string += " "

        stdscr.addstr(screen_height - 2, 1, hp_string)
        stdscr.addstr(screen_height - 1, 1, bullet_string)
        stdscr.addstr(screen_height - 1, screen_width - len(str(points)) - 10, f"Points: {str(points)}")

        stdscr.refresh()


wrapper(main)
