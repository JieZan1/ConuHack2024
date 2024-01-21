import curses
import time
from curses import wrapper

from Zombie import Zombie
from Player import Player
from Bullet import Bullet

bullets = []
zombies = []

spawnrate = 40


def main(stdscr):
    screen_height, screen_width = stdscr.getmaxyx()
    player = Player(5, 100)
    counter = 0
    points = 0

    stdscr.clear()
    stdscr.refresh()

    player.update_stance()
    stdscr.addstr(player.y, 0, player.stance)
    stdscr.nodelay(True)

    while True:
        # Make sure wrong input will come out as None
        try: 
            key = stdscr.getkey()
        except:
            key = None

        if key == "KEY_UP" and player.y > 0:
            player.y -= 1
            # player.change_stance()
        elif key == "KEY_DOWN" and player.y + player.height < screen_height - 2:
            player.y += 1
            # player.change_stance()
        elif key == " ":
            bullets.append(Bullet(player.width + 1, player.y + 1, 1))
        elif key == "p":    # exit program
            player.y += 10000

        for bullet in bullets:
            if bullet.x < screen_width - 1:
                bullet.move()
            else:
                bullets.remove(bullet)

        for zombie in zombies:
            if zombie.x > 0:
                zombie.move("LEFT")
            else:
                zombies.remove(zombie)

        time.sleep(0.05)

        counter += 1

        if counter == spawnrate:
            zombies.append(Zombie(screen_width - 2, player.y))
            counter = 0

        stdscr.clear()

        player.update_stance()
        stdscr.addstr(player.y, 0, player.stance)
        for bullet in bullets:
            stdscr.addstr(bullet.y, bullet.x, "-")
        for zombie in zombies:
            stdscr.addstr(zombie.y, zombie.x, zombie.face)
            stdscr.addstr(zombie.y+1, zombie.x, zombie.face)

        for bullet in bullets:
            for i in zombies:
                if i.x == bullet.x+1 or i.x == bullet.x or i.x == bullet.x - 1:
                    if i.y == bullet.y+1 or i.y == bullet.y or i.y == bullet.y - 1:
                        bullets.remove(bullet)
                        zombies.remove(i)
                        points += round(1/i.x * 25 + 5)

        stdscr.addstr(screen_height - 1, screen_width - len(str(points)) - 10, f"Points: {str(points)}")

        stdscr.refresh()


wrapper(main)
