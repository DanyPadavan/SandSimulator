from pygame import init, display, time, event, QUIT, Color, Surface, mouse, font
from time import perf_counter
from Point import Point
from random import randint


def main():
    init()
    surface_size = [500, 500]
    surface = display.set_mode(surface_size, vsync=1)
    display.set_caption('', '')
    display.set_icon(get_icon())
    loop(surface, time.Clock())


def loop(surface, clock, points=[]):
    text_color = Color(0, 0, 0)
    background_color = Color(255, 255, 255)
    my_font = font.SysFont('Segoe UI', 20)
    font_location = [15, 0]

    while len(event.get(QUIT)) == 0:
        clock.tick(100)
        begin_frame_time = perf_counter()
        surface.fill(background_color, surface.get_rect())
        [point.update(surface, points) for point in points]
        p = percent_frozen(list([point.frozen for point in points]))
        end_frame_time = perf_counter()
        info = f'Objects: {len(points)} Frozen: {p} % Elapsed: {elapsed(begin_frame_time, end_frame_time)} ms.'
        surface.blit(my_font.render(info, True, text_color), font_location)
        display.flip()
        mouse_handle(
            on_left_click=lambda pos: points.append(Point(pos)),
            on_right_click=lambda: points.clear()
        )


def mouse_handle(on_left_click, on_right_click):
    buttons = mouse.get_pressed(3)
    if buttons[0]:
        shift = 5
        x, y = mouse.get_pos()
        shift_x, shift_y = randint(-shift, shift), randint(-shift, shift)
        on_left_click((x + shift_x, y + shift_y))
    elif buttons[2]:
        on_right_click()


def get_icon():
    icon = Surface([50, 50])
    icon.fill(Color(255, 255, 255))
    return icon


def elapsed(begin, end):
    return round((end - begin) * 1000, 3)


def percent_frozen(points: list):
    if len(points) == 0:
        return 0.0
    count_frozen = len(list(filter(lambda x: x == True, points)))
    return round(count_frozen / len(points) * 100, 0)


if __name__ == '__main__':
    main()
