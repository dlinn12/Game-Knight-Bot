class GameNight():
    def __init__(self, id):
        self.id = id
        self.phase = 0  # 0: date, 1: game, 2: concluded
        self.dates = []
        self.games = []
        self.dates_votes = [0, 0, 0, 0]
        self.games_votes = [0 for x in range(17)]
        self.winning_date = None
        self.winning_games = []
        self.user_votes = {}  # (user_id, votes)
        self.host = None

    def set_dates(self, d1, d2, d3, d4):
        self.dates.append(d1)
        self.dates.append(d2)
        self.dates.append(d3)
        self.dates.append(d4)

    def set_phase(self, phase):
        self.phase = phase

    def set_id(self, id):
        self.id = id

    def set_host(self, host):
        self.host = host

    def get_id(self):
        return self.id

    def get_phase(self):
        return self.phase

    def get_date(self):
        vote = 0
        index = 0
        for i, v in enumerate(self.dates_votes):
            if v > vote:
                vote = v
                index = i

        self.winning_date = self.dates[index]

        return self.winning_date

    def get_games(self):
        copy_game_votes = self.games_votes.copy()

        gold_index = copy_game_votes.index(max(copy_game_votes))
        gold = self.games[gold_index]
        self.winning_games.append(gold)
        copy_game_votes.pop(gold_index)
        self.games.pop(gold_index)

        silver_index = copy_game_votes.index(max(copy_game_votes))
        silver = self.games[silver_index]
        self.winning_games.append(silver)
        copy_game_votes.pop(silver_index)
        self.games.pop(silver_index)

        bronze_index = copy_game_votes.index(max(copy_game_votes))
        bronze = self.games[bronze_index]
        self.winning_games.append(bronze)
        copy_game_votes.pop(bronze_index)
        self.games.pop(bronze_index)

        return self.winning_games

    def add_game(self, game):
        self.games.append(game)

    def tally_vote(self, vote, user):
        answer = True
        if self.phase == 0:
            if vote.emoji == '🐭':
                self.dates_votes[0] += 1
            elif vote.emoji == '🦊':
                self.dates_votes[1] += 1
            elif vote.emoji == '🐰':
                self.dates_votes[2] += 1
            elif vote.emoji == '🐦':
                self.dates_votes[3] += 1
            else:
                pass
        elif self.phase == 1:
            game_vote = True
            if vote.emoji == '🏠':
                self.games_votes[0] += 1
            elif vote.emoji == '❄':
                self.games_votes[1] += 1
            elif vote.emoji == '⛄':
                self.games_votes[2] += 1
            elif vote.emoji == '☃':
                self.games_votes[3] += 1
            elif vote.emoji == '🐱':
                self.games_votes[4] += 1
            elif vote.emoji == '👨‍🌾':
                self.games_votes[5] += 1
            elif vote.emoji == '🗺':
                self.games_votes[6] += 1
            elif vote.emoji == '💍':
                self.games_votes[7] += 1
            elif vote.emoji == '💉':
                self.games_votes[8] += 1
            elif vote.emoji == '🕐':
                self.games_votes[9] += 1
            elif vote.emoji == '🏛':
                self.games_votes[10] += 1
            elif vote.emoji == '🐦':
                self.games_votes[11] += 1
            elif vote.emoji == '👿':
                self.games_votes[12] += 1
            elif vote.emoji == '🗡':
                self.games_votes[13] += 1
            elif vote.emoji == '🐲':
                self.games_votes[14] += 1
            elif vote.emoji == '🍺':
                self.games_votes[15] += 1
            elif vote.emoji == '🍻':
                self.games_votes[16] += 1
            else:
                game_vote = False

            if game_vote:
                if not self.vote_added(user):
                    answer = False
        else:
            answer = False
        return answer

    def untally_vote(self, vote, user):
        if self.phase == 0:
            if vote.emoji == '🐭':
                self.dates_votes[0] -= 1
            elif vote.emoji == '🦊':
                self.dates_votes[1] -= 1
            elif vote.emoji == '🐰':
                self.dates_votes[2] -= 1
            elif vote.emoji == '🐦':
                self.dates_votes[3] -= 1
            else:
                pass
        elif self.phase == 1:
            game_vote = True
            if vote.emoji == '🏠':
                self.games_votes[0] -= 1
            elif vote.emoji == '❄':
                self.games_votes[1] -= 1
            elif vote.emoji == '⛄':
                self.games_votes[2] -= 1
            elif vote.emoji == '☃':
                self.games_votes[3] -= 1
            elif vote.emoji == '🐱':
                self.games_votes[4] -= 1
            elif vote.emoji == '👨‍🌾':
                self.games_votes[5] -= 1
            elif vote.emoji == '🗺':
                self.games_votes[6] -= 1
            elif vote.emoji == '💍':
                self.games_votes[7] -= 1
            elif vote.emoji == '💉':
                self.games_votes[8] -= 1
            elif vote.emoji == '🕐':
                self.games_votes[9] -= 1
            elif vote.emoji == '🏛':
                self.games_votes[10] -= 1
            elif vote.emoji == '🐦':
                self.games_votes[11] -= 1
            elif vote.emoji == '👿':
                self.games_votes[12] -= 1
            elif vote.emoji == '🗡':
                self.games_votes[13] -= 1
            elif vote.emoji == '🐲':
                self.games_votes[14] -= 1
            elif vote.emoji == '🍺':
                self.games_votes[15] -= 1
            elif vote.emoji == '🍻':
                self.games_votes[16] -= 1
            else:
                game_vote = False

            if game_vote:
                self.vote_removed(user)

    def vote_added(self, user):
        if user.id not in self.user_votes:
            self.user_votes[user.id] = 1
            return True
        else:
            current_votes = self.user_votes[user.id]

            if current_votes >= 3:
                self.user_votes[user.id] = current_votes + 1
                return False
            else:
                self.user_votes[user.id] = current_votes + 1
                return True

    def vote_removed(self, user):
        current_votes = self.user_votes[user.id]
        self.user_votes[user.id] = current_votes - 1

    def finalize_gamenight(self):
        self.winning_date = self.get_date()
        self.get_games()
