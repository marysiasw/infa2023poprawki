import codecs
import csv
import yaml
import random
import keyboard
import os
from psychopy import visual, event, gui, core
from os.path import join
from typing import Dict


RESULTS1 = [["NUMER PROBY", "EKSPERYMENT", "CZAS REAKCJI", "ZGODNOSC", "BODZIEC", "REAKCJA", "BLOK"]]

#TWORZENIE PLIKU YAMLA
def load_config():
    with open("config.yaml") as file:
        data = yaml.safe_load(file)
    return data

#FUKCJA DEFINIUJĄCA Z JAKICH KLAWISZY BĘDZIE KORZYSTAĆ OSOBA BADANA
#LISTA ZDEFINIOWANA W CONFIGU
def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=config["KEYS"])
    return key[0]

#FUNKCJA DEFINIUJĄCA Z JAKICH KLAWISZY BĘDZIE KORZYSTAĆ OSOBA BADANA W FAZIE EKSPERYMENTU
#LISTA ZDEFINIOWANA W CONFIGU
def experiment_keys(keys):
    event.clearEvents()
    exp_key = event.waitKeys(keyList=config["REACTION_KEYS"])
    return exp_key[0]

#FUNCKJA DEFINIUJACA CO SIE DZIEJE NA KONIEC PROGRAMU
def finish_experiment(win):
    message = visual.TextStim(win, text="", height=40)
    message.text = "Zakończyłeś eksperyment"
    message.draw()
    win.flip()
    core.wait(3)
    win.close()
    core.quit()
#ZAŁADOWANIE INSTRUKCJI UŻYWANYCH W EKSPERYMENCIE
def show_inst(win: visual.Window, file_name: str, insert: str = 'messages', keys=None):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=config["STIM_COLOR2"], text=msg, height=20)
    if keys is None:
        keys = ["space"]
    msg.draw()
    win.flip()
    reactions(keys)

#FUNKCJA KTÓRA CZYTA TEKST Z PLIKÓW W FOLDERZE MESSAGES (UŻYWANA DO INSTRUKCJI)
def read_text_from_file(file_name: str, insert: str = 'messages'):
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('insert'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)

#FUNKCJA ZAPISUJĄCA WYNIKI W FORMACIE CSV
def write_results_to_csv(results, info):
    filename = f"{info['ID']}_{info['Wiek']}_{info['Płeć']}.csv"
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, newline='') as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerow(result)

#TWORZENIE I RYSOWANIE BODZCÓW
#LOSOWANIE LICZBY/NARYSOWANIE
def bodsiec():
    b = random.choices([2, 1], [0.6, 0.4], k=1)[0]
    a = random.randrange(b, 1000, 2)
    stim = visual.TextStim(win=window, height=40, text=a, color=config['STIM_COLOR2'])
    stim.setPos((0, 0))
    stim.draw()
    return a


window = visual.Window(units="pix", color="grey", fullscr=False)
mouse = event.Mouse(win=window, visible=True)
clock = core.Clock()

config = load_config()
print(config)

#FEEDBACK W TRENINGU, KTÓRY OTRZYMUJE OSOBA BADANA
pozytywna_odp = visual.TextStim(win=window, text="DOBRZE!", color='green', height=40)
negatywna_odp = visual.TextStim(win=window, text="ŹLE!", color='black', height=40)
#WYŚWIETLENIE PUNKTU FIKSACJI I BODZCA
fix = visual.TextStim(win=window, text="+", pos=(0, 0), height=40, color=config["FIX_CROSS_COLOR"])
stim = visual.TextStim(win=window, height=60, color=config['STIM_COLOR2'])

#FUCKJA DEFINIUJĄCA PRZEBIEG TRENINGU
def part_of_training(n_trials, experiment, sz):
    for i in range(n_trials):
        keys = event.getKeys();
        if 'f7' in keys:
            print("'F7' key pressed!")
            f7_pressed = True
            finish_experiment(window)
            break
        mouse.setVisible(False)
        fix.draw()
        window.flip()
        core.wait(0.8)
        b = bodsiec()
        b
        window.callOnFlip(clock.reset)
        window.flip()

        acc = 100
        r = 0
        blok = "trening"

        if event.waitKeys(maxWait=1.0, keyList=['right'], timeStamped=True, clearEvents=True):
            r = 1

            if b % 2 == 0:

                rt = clock.getTime()

                acc = 1

                pozytywna_odp.draw()
                window.flip()
                core.wait(0.5)

                break

            else:

                acc = 0

                negatywna_odp.draw()
                window.flip()
                core.wait(0.5)

                break

        else:

            r = 0

        window.flip()
        core.wait(((random.randint(800, 900)) * 0.001))

        RESULTS1.append([i + 1, experiment, rt, acc, b, r, blok])
        # ZAPISANIE WYNIKÓW JAKO LISTY


#FUNKCJA DEFINIUJACA PRZEBIEG EKSPERYMENTU
def part_of_experiment(n_trials, experiment, sz):
    x = n_trials
    for i in range(x):
        keys = event.getKeys();
        if 'f7' in keys:
            print("'F7' key pressed!")
            f7_pressed = True
            finish_experiment(window)
            break
        mouse.setVisible(False)
        fix.draw()
        window.flip()
        core.wait(0.8)
        b = bodsiec()
        b
        window.callOnFlip(clock.reset)
        window.flip()
        rt = 0
        acc = 100
        r = 209

        if event.waitKeys(maxWait=1.0, keyList=['right'], timeStamped=True):
            r = 1
            if b % 2 == 0:
                rt = clock.getTime()
                acc = 1
                break
            else:
                acc = 0
                break
        else:
            r = 0
            if b % 2 == 0:
                acc = 0
            else:
                acc = 1

    window.flip()
    if (sz == False):
        blok = "normalny"
        core.wait(((random.randint(800, 900)) * 0.001))
    else:
        core.wait(((random.randint(700, 800)) * 0.001))
        blok = "szybki"
    RESULTS1.append([i + 1, experiment, rt, acc, b, r, blok])
    #ZAPISANIE WYNIKÓW JAKO LISTY


#TWORZENIE OKIENKA ZBIERAJĄCEGO DANE OD OSOBY BADANEJ
info: Dict = {"ID": "", "Wiek": "", "Płeć": ["M", "K"]}
gui.DlgFromDict(dictionary=info, title="Kwadraciki")

# TRAINING
show_inst(window, join('.', 'messages', 'inst1.txt'))
show_inst(window, join('.', 'messages', 'inst2.txt'))
show_inst(window, join('.', 'messages', 'inst3.txt'))
part_of_training(n_trials=config["N_TRIALS_TRAINING"], experiment=False, sz=False)

# EXPERIMENT_NORMAL
show_inst(window, join('.', 'messages', 'inst_exsp.txt'))
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True, sz=False)

# SERIES
show_inst(window, join('.', 'messages', 'inst_seria_pierwsza.txt'))
#show_text(info=inst_seria_pierwsza, win=window)

# EXPERIMENT_NORMAL
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True, sz=False)

# SERIES
show_inst(window, join('.', 'messages', 'inst_seria_kolejna.txt'))

# EXPERIMENT_NORMAL
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True, sz=False)

# BREAK
show_inst(window, join('.', 'messages', 'inst_break.txt'))

# EXPERIMENT_FAST
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True, sz=True)

# SERIES
show_inst(window, join('.', 'messages', 'inst_seria_pierwsza.txt'))

# EXPERIMENT_FAST
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True, sz=True)

# SERIES
show_inst(window, join('.', 'messages', 'inst_seria_kolejna.txt'))

# EXPERIMENT_FAST
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True, sz=True)

# END
show_inst(window, join('.', 'messages', 'inst_end.txt'))

# WRITE TO CSV
write_results_to_csv(RESULTS1, info)
