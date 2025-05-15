import pygame

bg_color = (30, 30, 30)
running = True

# Input state tracking
keys_pressed = set()
buttons_pressed = set()
joy_axis_values = {}  # {(instance_id, axis): value}
joy_hat_values = {}   # {(instance_id, hat): value}
TRIGGER_AXES = {4, 5}  # typical trigger axis numbers
TRIGGER_REST = -1.0
THRESHOLD = 0.2


def all_joy_motion_below_threshold():
    # Check regular axes and triggers separately
    for (instance_id, axis), value in joy_axis_values.items():
        if axis in TRIGGER_AXES:
            # Triggers: active when pressed beyond rest state + threshold
            if value > (TRIGGER_REST + THRESHOLD):
                return False
        else:
            # Regular axes: active when outside [-threshold, threshold]
            if abs(value) > THRESHOLD:
                return False

    # Check hats
    for value in joy_hat_values.values():
        if value != (0, 0):
            return False

    return True


def input_event():
    global bg_color, running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
            print(f"Key down: {pygame.key.name(event.key)}")
        if event.type == pygame.KEYUP:
            keys_pressed.discard(event.key)
            print(f"Key up: {pygame.key.name(event.key)}")

        # Controller button events
        if event.type == pygame.JOYBUTTONDOWN:
            buttons_pressed.add((event.instance_id, event.button))
            print(f"Joystick {event.instance_id} button {event.button} down")
        if event.type == pygame.JOYBUTTONUP:
            buttons_pressed.discard((event.instance_id, event.button))
            print(f"Joystick {event.instance_id} button {event.button} up")

        # Store analog/hat values
        if event.type == pygame.JOYAXISMOTION:
            joy_axis_values[(event.instance_id, event.axis)] = event.value
            print(f"Joystick {event.instance_id} axis {event.axis}: {event.value:.2f}")
        if event.type == pygame.JOYHATMOTION:
            joy_hat_values[(event.instance_id, event.hat)] = event.value
            print(f"Joystick {event.instance_id} hat {event.hat}: {event.value}")

    # Determine active input states
    joy_active = not all_joy_motion_below_threshold()
    keys_active = len(keys_pressed) > 0
    btns_active = len(buttons_pressed) > 0

    # Set color with priority: keys > buttons > analog/hat
    if keys_active:
        bg_color = (255, 0, 0)  # Red
    elif btns_active:
        bg_color = (0, 255, 0)  # Green
    elif joy_active:
        bg_color = (0, 0, 255)  # Blue
    else:
        bg_color = (30, 30, 30)  # Dark gray


def main():
    global running
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("PyTemplate")

    # Initialize joysticks/controllers
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()

    clock = pygame.time.Clock()

    # game loop
    while running:
        input_event()
        screen.fill(bg_color)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
