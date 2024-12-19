class Player:
    def __init__(self):
        pass
        
    def reset_state(self):
        """reset all the states"""
        self.opponent_history = []
        self.player_history = []   
        self.counter = 0
        self.opponent_name = None  # record opponent's name
        self.play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]
        
    def execute_strategy(self, prev_play):
        """main strategy of each move"""
        # check if it's new opponent
        if prev_play == "":
            self.reset_state()

        # update states
        self.counter += 1
        self.opponent_history.append(prev_play)
        
        
        # release baits to check opponent's move patterns
        if self.counter < 5:
            player_move = "S"
            self.player_history.append(player_move)
            return player_move

        # look at opponent's move patterns
        #print(self.opponent_history[0:6])
        
        # realize opponent
        if not self.opponent_name:
            if len(self.opponent_history) >= 6:
                if self.opponent_history[:5] ==    ["", "R", "R", "R", "R"]:
                    self.opponent_name = "mrugesh"
                elif self.opponent_history[0:6] == ["", "R", "P", "P", "S", "R"]:
                    self.opponent_name = "quincy"
                elif self.opponent_history[0:6] == ["", "P", "R", "R", "R", "R"]:
                    self.opponent_name = "kris"
                elif self.opponent_history[0:6] == ['', 'P', 'P', 'R', 'R', 'R']:
                    self.opponent_name = "abbey"

                    
        # choose strategy according to opponent
        if self.opponent_name == "quincy":
            player_move = self.anti_quincy()
        elif self.opponent_name == "mrugesh":
            player_move = self.anti_mrugesh()
        elif self.opponent_name == "abbey":
            player_move = self.anti_abbey()
        elif self.opponent_name == "kris":
            player_move = self.anti_kris()
        else:
            player_move = "R"   # default strategy

        self.player_history.append(player_move)
        
        return player_move
        
    def anti_quincy(self):
        choices = ["R", "P", "S", "S", "R"]
        return choices[self.counter % 5]
        
    def anti_mrugesh(self):
        last_five = self.opponent_history[-3:]
        most_frequent = max(set(last_five), key=last_five.count)
    
        if most_frequent == '':
            most_frequent = "S"
    
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
        return ideal_response[most_frequent]
        
    def anti_kris(self):
        # Kris's strategy is to take action based on the player's last action.
        # Then, every time the player loses to himself in the previous shot, he can win against kris.
        ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}
        player_prev_move = self.player_history[-1]
        return ideal_response[player_prev_move]
    
    def anti_abbey(self):
        # Abbey's strategy is: Analyze the frequency of opponent's recent two-step combinations, 
        # predict the opponent's most likely next move, and then play the counter move.  
        
        last_two = "".join(self.player_history[-2:])
        if len(last_two) == 2:
            self.play_order[0][last_two] += 1
    
        potential_plays = [
            self.player_history[-1] + "R",
            self.player_history[-1] + "P",
            self.player_history[-1] + "S",
        ]
    
        sub_order = {
            k: self.play_order[0][k]
            for k in potential_plays if k in self.play_order[0]
        }
    
        prediction = max(sub_order, key=sub_order.get)[-1:]  # abbey's prediction method
        ideal_response = {'P': 'R', 'R': 'S', 'S': 'P'}      # reverse abbey's method
        
        return ideal_response[prediction]




# Create a global instance
player_instance = Player()

def player(prev_play):
    """Wrapping function for the game system to call"""
    player_action = player_instance.execute_strategy(prev_play)
    return player_action