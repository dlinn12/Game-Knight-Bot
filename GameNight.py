class GameNight():
    def __init__(self, id):
        self.id = id
        self.phase = 0  # 0: date, 1: game, 2: concluded
        self.dates = []
        self.games = []
        self.dates_votes = [0, 0, 0, 0]
        self.games_votes = [0 for x in range(17)]
        self.winning_date = ''
        self.winning_games = []

    def set_dates(self, d1, d2, d3, d4):
        self.dates.append(d1)
        self.dates.append(d2)
        self.dates.append(d3)
        self.dates.append(d4)

    def set_phase(self, phase):
        self.phase = phase

    def set_id(self, id):
        self.id = id

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
        vote = 0
        index = 0
        for i, v in enumerate(self.games_votes):
            if v > vote:
                vote = v
                index = i

        self.winning_games.append(self.games_votes[index])
        return self.winning_games # fix me; I use index in game votes but that is not neccessarily the order db spits out games in

    def tally_vote(self, vote):
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
                pass
            # print(self.games_votes)

    def untally_vote(self, vote):
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
                pass
            # print(self.games_votes)
