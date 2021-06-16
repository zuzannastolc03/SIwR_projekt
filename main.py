import numpy as np
import csv

def read_file(file_name):
    # Date = [] #0 date
    TeamList = [] #lista wszystkich drużyn z pliku
    HomeTeam = [] #1 home team
    AwayTeam = [] #2 away team
    FTHG = [] #3 full time home team goals
    FTAG = [] #4 full time away team goals
    FTR = [] #5 full time results (H,D,A)
    # HTHG = [] #6 half time home team goals
    # HTAG = [] #7 half time away team goals
    # HTR = [] #8 half time results (H,D,A)
    # HS = [] #9 home team shots
    # AS = [] #10 away team shots
    HST = [] #11 home team shots on target
    AST = [] #12 away team shots on target
    # HF = [] #13 home team fouls committed
    # AF = [] #14 away team fouls committed
    HC = [] #15 home team corners
    AC = [] #16 away team corners
    # HY = [] #17 home team yellow cards
    # AY = [] #18 away team yellow cards
    # HR = [] #19 home team red cards
    # AR = [] #20 away team red cards
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                # Date.append(row[0])
                HomeTeam.append(row[1])
                AwayTeam.append(row[2])
                FTHG.append(row[3])
                FTAG.append(row[4])
                FTR.append(row[5])
                # HTHG.append(row[6])
                # HTAG.append(row[7])
                # HTR.append(row[8])
                # HS.append(row[9])
                # AS.append(row[10])
                HST.append(row[11])
                AST.append(row[12])
                # HF.append(row[13])
                # AF.append(row[14])
                HC.append(row[15])
                AC.append(row[16])
                # HY.append(row[17])
                # AY.append(row[18])
                # HR.append(row[19])
                # AR.append(row[20])
                #Stworzenie listy wszystkich drużyn
                for i in range(len(HomeTeam)):
                    if HomeTeam[i] in TeamList:
                        continue
                    else:
                        TeamList.append(HomeTeam[i])
                line_count += 1
    print(HomeTeam)
    print(TeamList)
if __name__ == '__main__':
    read_file('data.csv')
