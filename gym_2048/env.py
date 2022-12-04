import gym
import numpy as np
import gym.spaces as spaces
from gym.utils import seeding
import matplotlib.pyplot as plt


class Base2048Env(gym.Env):
  metadata = {
    'render.modes': ['human'],
  }

  # NOTE: Don't modify these numbers as they define the number of
  # anti-clockwise rotations before applying the left action on a grid

  LEFT = 0
  UP = 1
  RIGHT = 2
  DOWN = 3

  ACTION_STRING = {
    LEFT: 'left',
    UP: 'up',
    RIGHT: 'right',
    DOWN: 'down',
  }

  def __init__(self, width=4, height=4, max_invalid_moves=16):
    self.width = width
    self.height = height

    self.max_power = 1 + self.width * self.height

    self.observation_space = spaces.Box(
      # low=2,
      # high=2 ** (1 + self.width * self.height),
      low=0,
      high=self.max_power,
      shape=(self.width, self.height),
      dtype=np.int64
    )
    self.action_space = spaces.Discrete(4)

    # Internal Variables
    self.board = None
    self.np_random = None
    self.score = 0
    self.n_invalid_moves = 0
    self.max_invalid_moves = max_invalid_moves

    self.seed()
    self.reset()

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

  def step(self, action: int):
    """Rotate board aligned with left action"""

    # Align board action with left action
    rotated_obs = np.rot90(self.board, k=action)
    reward, updated_obs = self._slide_left_and_merge(rotated_obs)
    self.board = np.rot90(updated_obs, k=4 - action)

    # check if the move was valid
    if (self.board == updated_obs).all():
      self.n_invalid_moves += 1
    else:
      self.n_invalid_moves = 0

      # Place one random tile on empty location
      self._place_random_tiles(self.board, count=1)

    done = self.is_done()

    return self.board, reward, done, {}

  def is_done(self):

    # check if invalid moves are more than max_invalid_moves
    if self.n_invalid_moves >= self.max_invalid_moves:
      return True

    copy_board = self.board.copy()

    if not copy_board.all():
      return False

    for action in [0, 1, 2, 3]:
      rotated_obs = np.rot90(copy_board, k=action)
      _, updated_obs = self._slide_left_and_merge(rotated_obs)
      if not updated_obs.all():
        return False

    return True

  def reset(self, **kwargs):
    """Place 2 tiles on empty board."""

    self.board = np.zeros((self.width, self.height), dtype=np.int64)
    self._place_random_tiles(self.board, count=2)

    return self.board

  def get_board(self):
    # raise board to power of 2, make zeros nan
    board = np.array(2 ** self.board, dtype=np.float64)
    board[self.board == 0] = np.nan

    return board

  def _sample_tiles(self, count=1):
    """Sample tile 2 or 4."""

    # choices = [2, 4]
    choices = [1, 2]
    probs = [0.9, 0.1]

    tiles = self.np_random.choice(choices, size=count, p=probs)
    return tiles.tolist()

  def _sample_tile_locations(self, board, count=1):
    """Sample grid locations with no tile."""

    zero_locs = np.argwhere(board == 0)
    zero_indices = self.np_random.choice(len(zero_locs), size=count)

    zero_pos = zero_locs[zero_indices]
    return zero_pos.tolist()

  def _place_random_tiles(self, board, count=1):
    if not board.all():
      tiles = self._sample_tiles(count)
      tile_locs = self._sample_tile_locations(board, count)
      for (x, y), tile in zip(tile_locs, tiles):
        board[x, y] = tile

  def _slide_left_and_merge(self, board):
    """Slide tiles on a grid to the left and merge."""

    result = []

    score = 0
    for row in board:
      row = np.extract(row > 0, row)
      score_, result_row = self._try_merge(row)
      score += score_
      row = np.pad(np.array(result_row), (0, self.width - len(result_row)),
                   'constant', constant_values=(0,))
      result.append(row)

    return score, np.array(result, dtype=np.int64)

  def _try_merge(self, row):
    score = 0
    result_row = []

    i = 1
    while i < len(row):
      if row[i] == row[i - 1]:
        score += (row[i] + row[i - 1]) ** 2
        result_row.append(row[i] + 1)
        i += 2
      else:
        result_row.append(row[i - 1])
        i += 1

    if i == len(row):
      result_row.append(row[i - 1])

    self.score += score

    return score, result_row

  def render(self):

    # import matplotlib.colors as mcolors
    # cmap, norm = mcolors.from_levels_and_colors(
    #   2 ** np.arange(1, self.max_power + 1), [
    #     'red', 'green', 'blue' ...
    #   ])

    board = self.get_board()

    fig, ax = plt.subplots(figsize=(4, 4))
    im = ax.imshow(board, cmap='viridis')

    plt.title(f'Score: {self.score}')

    plt.tick_params(
      bottom=False,
      labelbottom=False,
      left=False,
      labelleft=False,
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    width, height = board.shape
    for i in range(width):
      for j in range(height):
        if not np.isnan(board[i, j]):
          # todo need to scale to fit the tile
          ax.text(j, i, int(board[i, j]), ha="center", va="center", color="w", fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.show()
