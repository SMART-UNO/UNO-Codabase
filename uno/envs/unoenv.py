import numpy as np
from collections import OrderedDict
from icecream import ic

# LOCAL IMPORT
from uno.envs.env import Env
from uno.game.uno import Game
from uno.game.uno.utils import encode_hand, encode_target
from uno.game.uno.utils import ACTION_SPACE, ACTION_LIST
from uno.game.uno.utils import cards2list

DEFAULT_GAME_CONFIG = {
    'game_num_players': 2,
}
# TODO: (Xiaoyang): Refactor this class later...


class UnoEnv(Env):

    def __init__(self, config):
        self.name = 'uno'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[4, 4, 15] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):
        obs = np.zeros((4, 4, 15), dtype=int)
        encode_hand(obs[:3], state['hand'])
        encode_target(obs[3], state['target'])
        legal_action_id = self._get_legal_actions()
        extracted_state = {'obs': obs, 'legal_actions': legal_action_id}
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [
            a for a in state['legal_actions']]
        extracted_state['action_record'] = self.action_recorder
        return extracted_state

    def get_payoffs(self):

        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        # ic(legal_ids)
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        # ic(legal_ids)
        legal_ids = list(legal_ids)
        # ic(list(legal_ids))
        # legal_ids = [x[0] for x in list(legal_ids)]
        return ACTION_LIST[np.random.choice(legal_ids)]

    def _get_legal_actions(self):
        legal_actions, target = self.game.get_legal_actions()
        # ic(target.str)
        legal_ids = {ACTION_SPACE[action]: None for action in legal_actions}
        return OrderedDict(legal_ids)

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['num_players'] = self.num_players
        state['hand_cards'] = [cards2list(player.hand)
                               for player in self.game.players]
        state['played_cards'] = cards2list(self.game.round.played_cards)
        state['target'] = self.game.round.target.str
        state['current_player'] = self.game.round.current_player
        state['legal_actions'], _ = self.game.round.get_legal_actions(
            self.game.players, state['current_player'])
        return state
