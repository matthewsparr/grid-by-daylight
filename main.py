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

wrapper.build_gym_from_yaml('dbd', 'dbd.yaml', level=3)
# Press the green button in the gutter to run the script.

def random_direction():
    return(np.random.choice([1, 2, 3, 4]))
def random_action(actions):
    return (np.random.choice(actions))

actions_list = ['initialize_killer', 'move', 'attack', 'recharge', 'damage_generator', 'place_trap', 'pick_up_trap', 'heal', 'repair_generator', 'disarm_trap', 'open_exit_gate']
killer_actions = ['move', 'attack', 'recharge', 'damage_generator', 'place_trap', 'pick_up_trap']
survivor_actions = ['move', 'heal', 'repair_generator', 'disarm_trap', 'open_exit_gate']
killer_action_ids = [actions_list.index(i) for i in killer_actions]
survivor_action_ids = [actions_list.index(i) for i in survivor_actions]

if __name__ == '__main__':

    env = gym.make('GDY-dbd-v0', global_observer_type=gd.ObserverType.ISOMETRIC, image_path='C:/Users/Matthew/Desktop/griddly/sprites') #  ISOMETRIC SPRITE_2D
    env.enable_history(True)
    env.reset()
    # env.render(observer='global')

    ## progress bars
    if False:
        generator_progress_bar = tqdm(total=100, leave=True, desc = 'generators', position=0)
        downed_survivor_progress_bar = tqdm(total=4, leave=True, desc = 'downed survivors', position=0)
        exit_gate_progress_bar = tqdm(total=100, leave=True, desc='exit gate', position=0)
        monitor_generators = True
        monitor_exit_gate = True
        monitor_survivors = False

    for s in range(10000):
        time.sleep(0.05)
        # actions = env.action_space.sample()
        actions = []
        for player in range(1,6):
            if player==1: ## killer
                actions.append(np.array([random_action(killer_action_ids), random_direction()], dtype=np.int64))
            else: ## survivor
                actions.append(np.array([random_action(survivor_action_ids), random_direction()], dtype=np.int64))
            # actions.append(np.array([1,random_direction()]))
        obs, reward, done, info = env.step(actions)
        state = env.get_state()

        ## progress bars
        if False:

            progress = sum([i['Variables']['progress'] for i in state['Objects'] if i['Name']=='generator'])/3
            if monitor_generators:
                generator_progress_bar.n = progress
                generator_progress_bar.refresh()

            downed_survivors = state['GlobalVariables']['downed_survivors'][0]
            if monitor_survivors:
                downed_survivor_progress_bar.n = downed_survivors
                downed_survivor_progress_bar.refresh()

            if progress >= 100 and monitor_exit_gate:
                exit_gate_progress = [i['Variables']['progress'] for i in state['Objects'] if i['Name']=='exit_gate'][0]
                exit_gate_progress_bar.n = exit_gate_progress
                exit_gate_progress_bar.refresh() ## progress bar handling

        # env.render(observer=3) # Renders the entire environment
        env.render(observer='global')

        if done:
            outcome = info['PlayerResults']['1']
            if outcome=='Win':
                print('Survivors won')
            else:
                print('Killer won')
            break
    time.sleep(5)
    env.close()
