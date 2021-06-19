import csv
import sys
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

TeamList = [] #lista wszystkich drużyn z pliku
HomeTeam = [] #1 home team
AwayTeam = [] #2 away team
FTR = [] #5 full time results (H,D,A)
PointsList = [] #lista punktów każdej z drużyn na liście
NumberOfGames = [] #liczba gier rozegranych przez każdą z drużyn
Effectiveness = [] #skuteczność każdej z drużyn

def read_file(file_name, list_of_teams, home_teams, away_teams, results, list_of_points, number_of_games, ratio):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                home_teams.append(row[1])
                away_teams.append(row[2])
                results.append(row[5])
                #Uzupełnienie listy wszystkich drużyn, ich punktów i iliści rozegranych meczów
                for i in range(len(home_teams)):
                    if home_teams[i] not in list_of_teams:
                        list_of_teams.append(home_teams[i])
                        list_of_points.append(0)
                        number_of_games.append(0)
                        ratio.append(0)
                line_count += 1

def count_points(list_of_teams, home_teams, away_teams, results, list_of_points, number_of_games):
    for team in range(len(list_of_teams)):
        for i in range(len(home_teams)):
            if home_teams[i] == list_of_teams[team]:
                if results[i] == 'H':
                    list_of_points[team] += 3
                elif results[i] == 'D':
                    list_of_points[team] += 1
                number_of_games[team] += 1
        for i in range(len(away_teams)):
            if away_teams[i] == list_of_teams[team]:
                if results[i] == 'A':
                    list_of_points[team] += 3
                elif results[i] == 'D':
                    list_of_points[team] += 1
                number_of_games[team] += 1

if __name__ == '__main__':
    read_file('data.csv', TeamList, HomeTeam, AwayTeam, FTR, PointsList, NumberOfGames, Effectiveness)
    count_points(TeamList, HomeTeam, AwayTeam, FTR, PointsList, NumberOfGames)
    for i in range(len(Effectiveness)):
        Effectiveness[i] = PointsList[i] / (3 * NumberOfGames[i])
    # home_team = sys.argv[1]
    # away_team = sys.argv[2]
    # for hteam in range(len(TeamList)):
    #     if TeamList[hteam] == home_team:
    #         home = hteam
    # for ateam in range(len(TeamList)):
    #     if TeamList[ateam] == away_team:
    #         away = ateam
    home = 0
    away = 2
    football_model = BayesianModel([('HomeTeam', 'Match'),
                                   ('AwayTeam', 'Match')])
    #CPD(0)-zwycięstwo, CPD(1)-przegrana
    cpd_home_team = TabularCPD('HomeTeam', 2, [[Effectiveness[home]], [1.0-Effectiveness[home]]])
    cpd_away_team = TabularCPD('AwayTeam', 2, [[Effectiveness[away]], [1.0 - Effectiveness[away]]])
    #CPD(0)-zwycięstwo HT, CPD(1)-zwycięstwo AT, CPD(2)-remis
    cpd_match = TabularCPD('Match', 3, [[0.0, 1.0, 0.0, 0.0],
                                        [0.0, 0.0, 1.0, 0.0],
                                        [1.0, 0.0, 0.0, 1.0]],
                                        evidence=['HomeTeam', 'AwayTeam'], evidence_card=[2,2])
    football_model.add_cpds(cpd_home_team, cpd_away_team, cpd_match)
    football_infer = VariableElimination(football_model)
    q = football_infer.query(['Match'])
    print('P(Match) =\n', q)
    print(TeamList)
    print(PointsList)
    print(Effectiveness)
