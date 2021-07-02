import csv
import sys
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# TODO Jakość kodu (1/2)

# TODO Skuteczność 0.333 (0/3)
# TODO [0.56, 1.00] - 3.0
# TODO [0.53, 0.56) - 2.5
# TODO [0.50, 0.53) - 2.0
# TODO [0.47, 0.50) - 1.5
# TODO [0.44, 0.47) - 1.0
# TODO [0.41, 0.44) - 0.5
# TODO [0.00, 0.41) - 0.0

# TODO Niepotrzebnie te tablice są globalne.
TeamList = [] #lista wszystkich drużyn z pliku
HomeTeam = [] #1 home team
AwayTeam = [] #2 away team
FTR = [] #5 full time results (H,D,A)
PointsListHome = [] #lista punktów każdej z drużyn na liście zdobytych u siebie
PointsListAway = [] #lista punktów każdej z drużyn na liście zdobytych u kogoś
NumberOfGamesHome = [] #liczba gier rozegranych przez każdą z drużyn u siebie
NumberOfGamesAway = [] #liczba gier rozegranych przez każdą z drużyn u kogoś
EffectivenessHome = [] #skuteczność każdej z drużyn u siebie
EffectivenessAway = [] #skuteczność każdej z drużyn u kogoś

def read_file(file_name, list_of_teams, home_teams, away_teams, results, list_of_points_home, list_of_points_away, number_of_games_home, number_of_games_away, ratio_home, ratio_away):
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
                        list_of_points_home.append(0)
                        list_of_points_away.append(0)
                        number_of_games_home.append(0)
                        number_of_games_away.append(0)
                        ratio_home.append(0)
                        ratio_away.append(0)
                line_count += 1

def count_points(list_of_teams, home_teams, away_teams, results, list_of_points_home, list_of_points_away, number_of_games_home, number_of_games_away):
    for team in range(len(list_of_teams)):
        for i in range(len(home_teams)):
            if home_teams[i] == list_of_teams[team]:
                if results[i] == 'H':
                    list_of_points_home[team] += 3
                elif results[i] == 'D':
                    list_of_points_home[team] += 1
                number_of_games_home[team] += 1
        for i in range(len(away_teams)):
            if away_teams[i] == list_of_teams[team]:
                if results[i] == 'A':
                    list_of_points_away[team] += 3
                elif results[i] == 'D':
                    list_of_points_away[team] += 1
                number_of_games_away[team] += 1

if __name__ == '__main__':
    read_file('data.csv', TeamList, HomeTeam, AwayTeam, FTR, PointsListHome, PointsListAway, NumberOfGamesHome, NumberOfGamesAway, EffectivenessHome, EffectivenessAway)
    count_points(TeamList, HomeTeam, AwayTeam, FTR, PointsListHome, PointsListAway, NumberOfGamesHome, NumberOfGamesAway)
    for i in range(len(EffectivenessHome)):
        EffectivenessHome[i] = PointsListHome[i] / (3 * NumberOfGamesHome[i])
    for i in range(len(EffectivenessAway)):
        EffectivenessAway[i] = PointsListAway[i] / (3 * NumberOfGamesAway[i])
    # TODO W ten sposób na wyjście zostanie przekazany ciąg znaków "Proszę wprowadzić datę spotkania " (-1).
    date = input('Proszę wprowadzić datę spotkania ')
    home_team = input('Proszę wprowadzić nazwę drużyny grającej u siebie ')
    away_team = input('Proszę wprowadzić nazwę drużyny grającej na wyjeździe ')

    #gdyby jednak nie chodziło o input tylko sys.argv
    # home_team = sys.argv[2]
    # away_team = sys.argv[3]

    for hteam in range(len(TeamList)):
        if TeamList[hteam] == home_team:
            home = hteam
    for ateam in range(len(TeamList)):
        if TeamList[ateam] == away_team:
            away = ateam

    # TODO Model i dobór parametrów (3/5)

    football_model = BayesianModel([('HomeTeam', 'Match'),
                                   ('AwayTeam', 'Match')])
    #CPD(0)-zwycięstwo, CPD(1)-przegrana
    cpd_home_team = TabularCPD('HomeTeam', 2, [[EffectivenessHome[home]], [1.0-EffectivenessHome[home]]])
    cpd_away_team = TabularCPD('AwayTeam', 2, [[EffectivenessAway[away]], [1.0 - EffectivenessAway[away]]])
    # TODO Chyba lepiej gdyby "HomeTeam" i "AwayTeam" oznaczało np. formę drużyny,
    # TODO wtedy tutaj mogłyby być inne wartości.
    #CPD(0)-zwycięstwo HT, CPD(1)-zwycięstwo AT, CPD(2)-remis
    cpd_match = TabularCPD('Match', 3, [[0.0, 1.0, 0.0, 0.0],
                                        [0.0, 0.0, 1.0, 0.0],
                                        [1.0, 0.0, 0.0, 1.0]],
                                        evidence=['HomeTeam', 'AwayTeam'], evidence_card=[2,2])
    football_model.add_cpds(cpd_home_team, cpd_away_team, cpd_match)
    football_infer = VariableElimination(football_model)
    q = football_infer.query(['Match'], show_progress=False)
    # TODO Czemu tak, a nie q['Match']?
    Q = str(q)
    result = []
    for i in range(len(Q)):
        if Q[i].isnumeric():
            result.append(Q[i])
    M0 = str(result[1] + '.' + result[2] + result[3] + result[4] + result[5])
    M0 = float(M0)
    M1 = str(result[7] + '.' + result[8] + result[9] + result[10] + result[11])
    M1 = float(M1)
    M2 = str(result[13] + '.' + result[14] + result[15] + result[16] + result[17])
    M2 = float(M2)
    max = max(M0, M1, M2)
    if max == M2:
        print('D', end='')
    elif max == M0 and M0 == M1:
        print('D', end='')
    elif max == M0:
        print('H', end='')
    else:
        print('A', end='')
