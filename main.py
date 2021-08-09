# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import gym
import griddly
from gym.utils.play import play
from griddly import GymWrapperFactory, gd
import time
import numpy as np
from tqdm import tqdm

wrapper = GymWrapperFactory()

wrapper.build_gym_from_yaml('dbd', 'dbd.yaml', level=1)
# Press the green button in the gutter to run the script.

def random_direction():
    return(np.random.choice([1, 2, 3, 4]))
def random_action(actions):
    return (np.random.choice(actions))

killer_actions = [1,2,4,6]
survivor_actions = [3,4,5,7,8]
if __name__ == '__main__':
    env = gym.make('GDY-dbd-v0', global_observer_type=gd.ObserverType.SPRITE_2D) #  ISOMETRIC
    env.enable_history(True)
    env.reset()
    env.render(observer='global')
    print(env.action_space)

    # time.sleep(1)
    # play(env, fps=30, zoom=3)
    # Replace with your own control algorithm!
    generator_progress_bar = tqdm(total=100, leave=True, desc = 'generators', position=0)
    downed_survivor_progress_bar = tqdm(total=4, leave=True, desc = 'downed survivors', position=0)
    monitor_generators = True
    monitor_survivors = False
    for s in range(10000):
        time.sleep(0.01)
        # actions = env.action_space.sample()
        actions = []
        for player in range(1,6):
            if player==1: ## killer
                actions.append(np.array([random_action(killer_actions), random_direction()], dtype=np.int64))
            else: ## survivor
                actions.append(np.array([random_action(survivor_actions), random_direction()], dtype=np.int64))

        obs, reward, done, info = env.step(actions)

        state = env.get_state()
        # print([i['Variables']['progress'] for i in state['Objects'] if i['Name']=='generator'])
        progress = [i['Variables']['progress'] for i in state['Objects'] if i['Name']=='generator'][0]
        if monitor_generators:
            generator_progress_bar.n = progress
            generator_progress_bar.refresh()

        downed_survivors = state['GlobalVariables']['downed_survivors'][0]
        if monitor_survivors:
            downed_survivor_progress_bar.n = downed_survivors
            downed_survivor_progress_bar.refresh()

        exit_gate_progress = [i['Variables']['progress'] for i in state['Objects'] if i['Name']=='exit_gate'][0]
        if exit_gate_progress > 0:
            print(exit_gate_progress)
        env.render(observer='global') # Renders the entire environment

        if done:
            outcome = info['PlayerResults']['1']
            if outcome=='Win':
                print('Survivors won')
            else:
                print('Killer won')
            break
    time.sleep(5)
    env.close()
