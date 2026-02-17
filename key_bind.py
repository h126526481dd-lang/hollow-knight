import pygame
import json
import os


class KeyBindingManager:
    def __init__(self, filename="keybindings.json"):
        self.filename = filename

        # 預設按鍵
        self.default_bindings = {
            
            "saving": pygame.K_w,
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "go_down": pygame.K_s,
            "jump": pygame.K_SPACE,
            "dash": pygame.K_LSHIFT,
            "attack": pygame.K_j,
            "heal": pygame.K_r,
            "block": pygame.K_l
        }

        self.bindings = self.default_bindings.copy()
        self.load()

    # 取得某動作的按鍵
    def get_key(self, action):
        return self.bindings.get(action)

    # 修改按鍵
    def set_key(self, action, new_key):
        self.bindings[action] = new_key

    # 儲存到 JSON
    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.bindings, f)

    # 載入 JSON
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.bindings = json.load(f)

    # 將 key 轉換成顯示文字
    def get_key_name(self, action):
        key = self.get_key(action)
        return pygame.key.name(key)
