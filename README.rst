Gym 2048
=========

.. image:: https://travis-ci.com/activatedgeek/gym-2048.svg?branch=master
    :target: https://travis-ci.com/activatedgeek/gym-2048

.. image:: https://badge.fury.io/py/gym-2048.svg
    :target: https://pypi.org/project/gym-2048/

This package implements the classic grid game 2048
for OpenAI gym environment.

Install
--------

.. code:: shell

    pip install gym_2048


Usage
------

.. code:: python

    import gym_2048
    import gym

    if __name__ == '__main__':
      env = gym.make('2048-v0')
      env.render()

      done = False
      while not done:
        action = env.action_space.sample()
        next_state, reward, done, _ = env.step(action)
        env.render(mode='human')
