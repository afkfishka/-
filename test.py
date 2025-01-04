import pickle

# функция для сохранения игры
def save_game(state):
    with open('savegame.pkl', 'wb') as f:
        pickle.dump(state, f)

# функция для загрузки сохраненной игры
def load_game():
    with open('savegame.pkl', 'rb') as f:
        state = pickle.load(f)
    return state

# сохраняем игру
state = {}
save_game(state)

# загружаем игру
loaded_state = load_game()
print(loaded_state)