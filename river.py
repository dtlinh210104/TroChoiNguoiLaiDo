import pygame
import sys

# Cấu hình
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Đưa Sói, Cừu và Bắp Cải Qua Sông")
clock = pygame.time.Clock()

# Tải và thay đổi kích thước hình ảnh
try:
    background = pygame.image.load("background.png")
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    boat = pygame.image.load("boat.png")
    boat = pygame.transform.scale(boat, (150, 100))

    wolf = pygame.image.load("wolf.png")
    wolf = pygame.transform.scale(wolf, (100, 100))

    sheep = pygame.image.load("sheep.png")
    sheep = pygame.transform.scale(sheep, (100, 100))

    cabbage = pygame.image.load("cabbage.png")
    cabbage = pygame.transform.scale(cabbage, (100, 100))

    person = pygame.image.load("person.png")
    person = pygame.transform.scale(person, (50, 100))
except pygame.error as e:
    print(f"Không thể tải hình ảnh: {e}")
    pygame.quit()
    sys.exit()

# Định nghĩa trạng thái ban đầu
left_side = {"wolf": (10, 400), "sheep": (10, 300), "cabbage": (10, 200)}
right_side = {}
boat_position = "left"
boat_objects = []  # Danh sách đối tượng trên thuyền
boat_capacity = 1  # Chỉ cho phép một đối tượng trên thuyền

# Vị trí cố định của thuyền
boat_positions = {"left": (100, 400), "right": (500, 400)}

# Kiểm tra trạng thái hợp lệ
def is_valid_state(left_side, right_side):
    # Kiểm tra nếu sói và cừu ở cùng một bên mà không có người thì sói sẽ ăn cừu
    if "wolf" in left_side and "sheep" in left_side and "person" not in left_side:
        return False
    if "wolf" in right_side and "sheep" in right_side and "person" not in right_side:
        return False

    # Kiểm tra nếu cừu và bắp cải ở cùng một bên mà không có người thì cừu sẽ ăn bắp cải
    if "sheep" in left_side and "cabbage" in left_side and "person" not in left_side:
        return False
    if "sheep" in right_side and "cabbage" in right_side and "person" not in right_side:
        return False

    return True

# Hàm vẽ các đối tượng
def draw_objects():
    screen.blit(background, (0, 0))
    screen.blit(boat, boat_positions[boat_position])

    # Vẽ người trên thuyền
    screen.blit(person, (boat_positions[boat_position][0] + 50, 350))

    # Vẽ các đối tượng ở bờ trái
    for obj, pos in left_side.items():
        if obj == "wolf":
            screen.blit(wolf, pos)
        elif obj == "sheep":
            screen.blit(sheep, pos)
        elif obj == "cabbage":
            screen.blit(cabbage, pos)

    # Vẽ các đối tượng ở bờ phải
    for obj, pos in right_side.items():
        if obj == "wolf":
            screen.blit(wolf, pos)
        elif obj == "sheep":
            screen.blit(sheep, pos)
        elif obj == "cabbage":
            screen.blit(cabbage, pos)

    # Vẽ các đối tượng trên thuyền
    for i, obj in enumerate(boat_objects):
        if obj == "wolf":
            screen.blit(wolf, (boat_positions[boat_position][0] + i * 50, 350))
        elif obj == "sheep":
            screen.blit(sheep, (boat_positions[boat_position][0] + i * 50, 350))
        elif obj == "cabbage":
            screen.blit(cabbage, (boat_positions[boat_position][0] + i * 50, 350))

# Hàm kiểm tra thắng
def check_win():
    # Kiểm tra nếu tất cả đối tượng đã ở bên phải và không còn đối tượng nào ở bên trái
    return len(left_side) == 0 and len(boat_objects) == 0 and len(right_side) == 3

# Hàm hiển thị hộp thoại thông báo chiến thắng
def show_win_message():
    font = pygame.font.Font(None, 72)
    text = font.render("You Win!!!", True, GREEN)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Chờ người chơi bấm "OK" hoặc bất kỳ phím nào để chơi lại
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Bấm Enter để chơi lại
                    waiting_for_input = False
                    reset_game()

# Hàm hiển thị hộp thoại thông báo thua
def show_lose_message():
    font = pygame.font.Font(None, 36)
    text = font.render("You Lose!!!", True, RED)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Chờ người chơi bấm "OK" để tiếp tục
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Bấm Enter để chơi lại
                    waiting_for_input = False
                    reset_game()

# Hàm reset trò chơi
def reset_game():
    global left_side, right_side, boat_position, boat_objects
    left_side = {"wolf": (10, 400), "sheep": (10, 300), "cabbage": (10, 200)}
    right_side = {}
    boat_position = "left"
    boat_objects = []

# Vị trí của các đối tượng sau khi thả (trên bờ phải hoặc bờ trái)
def drop_object_on_side(obj, position, side):
    if obj == "wolf":
        side[obj] = position[0], 400
    elif obj == "sheep":
        side[obj] = position[0], 300
    elif obj == "cabbage":
        side[obj] = position[0], 200

# Vòng lặp chính
running = True
click_mode = "pick"  # "pick": chọn đối tượng lên thuyền, "drop": thả đối tượng xuống thuyền
while running:
    screen.fill(WHITE)
    draw_objects()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Chọn đối tượng để đưa lên thuyền
            if click_mode == "pick":
                if boat_position == "left":
                    for obj, pos in list(left_side.items()):
                        if pos[0] <= mouse_pos[0] <= pos[0] + 100 and pos[1] <= mouse_pos[1] <= pos[1] + 100:
                            if len(boat_objects) < boat_capacity:
                                boat_objects.append(obj)
                                del left_side[obj]
                            break
                elif boat_position == "right":
                    for obj, pos in list(right_side.items()):
                        if pos[0] <= mouse_pos[0] <= pos[0] + 100 and pos[1] <= mouse_pos[1] <= pos[1] + 100:
                            if len(boat_objects) < boat_capacity:
                                boat_objects.append(obj)
                                del right_side[obj]
                            break
                click_mode = "drop"

            # Thả đối tượng xuống thuyền
            elif click_mode == "drop":
                for i, obj in enumerate(boat_objects):
                    if boat_position == "left" and boat_positions[boat_position][0] + i * 50 <= mouse_pos[0] <= boat_positions[boat_position][0] + (i + 1) * 50:
                        drop_object_on_side(obj, (10, 400), left_side)
                        boat_objects.remove(obj)
                        break
                    elif boat_position == "right" and boat_positions[boat_position][0] + i * 50 <= mouse_pos[0] <= boat_positions[boat_position][0] + (i + 1) * 50:
                        drop_object_on_side(obj, (690, 400), right_side)
                        boat_objects.remove(obj)
                        break
                click_mode = "pick"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Di chuyển thuyền và thả đối tượng xuống bờ
                if boat_position == "left":
                    boat_position = "right"
                else:
                    boat_position = "left"

                # Kiểm tra nếu trò chơi thắng
                if check_win():
                    show_win_message()

                # Kiểm tra nếu trò chơi vi phạm
                elif not is_valid_state(left_side, right_side):
                    show_lose_message()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()


















