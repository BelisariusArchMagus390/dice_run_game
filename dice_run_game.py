import random

# cria as variáveis globais
position_player = 0
position_cpu = 0
victorious = ''
dice_result = 0
flag_turn = True
# cria dicionário que guarda os eventos especiais da partida
special_events = {'broken_bridge': [-2, 'Você chegou em uma ponte quebrada e terá que dar a volta, -2 casas.'], 
                    'paving_path': [2, 'Você chegou em uma rua pavimentada que facilita muito a sua corrida, +2 casas'],
                    'ride': [3, 'Você encontrou um carro para te dar carona, +3 casas'],
                    'congestion': [-3, 'Você encontrou um congestionamento no caminho que te atrasou muito, -3 casas'],
                    'lost': [0, 'Você se perde no caminho, portanto volta onde parou, volta a posição anterior'],
                    '+turn': ['+', 'Você ultrapassou muito o outro competidor, mais 1 turno']}
path_vector = [0]*31

# verifica a entrada do usuário
def command_confirmation():
    flag_command = False
    while flag_command == False:
        confirm_command = input('\nVez do jogador rolar o dado: ')
    
        if confirm_command == '':
            flag_command = True
        else:
            print('\nEntrada incorreta')

# cria o mapameanto dos eventos especiais da partida
def creation_special_events():
    global special_events
    global path_vector    
    global dice_result

    # cria lista com o nome dos eventos especiais
    special_events_vector = list(special_events.keys())

    # escolhe o número de eventos que podem ocorrer na partida, onde 20 é o máximo
    number_special_events = random.randrange(1,21)

    # cria o vetor mapeada com o os eventos especiais
    for i in range(number_special_events):
        path_position = random.randrange(0,31)

        if path_vector[path_position] == 0:
            position = random.randrange(0,5)

            path_vector[path_position] = special_events_vector[position]

# verifica de se ocorreu ou não um evento e a aplicação do seu efeito caso seja detectado
def if_special_event(position, turn):
    global position_player
    global position_cpu
    global dice_result
    global flag_turn

    if dice_result == 6:
        event = '+turn'
        description = special_events[event][1]

        print('Evento especial!', description)
        flag_turn = False

    elif path_vector[position] != 0:
        event = path_vector[position]
        effect = special_events[event][0]
        description = special_events[event][1]

        print('Evento especial!', description)

        if turn == "player":
            if effect == 0:
                position_player -= dice_result
            else:
                position_player += effect
        elif turn == "cpu":
            if effect == 0:
                position_cpu -= dice_result
            else:
                position_cpu += effect

# rola o dado de 6 lados
def dice():
    return random.randrange(1,7)

# verifica a condição de vitória
def victory_condition(position):
    if position == 30 or position > 30:
        return True

# faz a visualização da resolução da partida
def victory_mode(turn):
    global position_player
    global position_cpu
    global victorious

    if turn == "player":
        print("\n----- O JOGADOR VENCEU!!! -----\n")
    elif turn == "cpu":
        print("\n----- A CPU VENCEU!!! -----\n")
    
    position_player = 0
    position_cpu = 0
    victorious = ''

    print('Obrigado por jogar.')

    option = input('Você quer jogar de novo? (S/N): ')

    option = option.upper()

    if option == 'S':
        main()
    elif option == 'N':
        exit(1)

# executa os turnos do jogador e da CPU (computador)
def main():
    global position_player
    global position_cpu
    global victorious
    global dice_result
    global flag_turn

    creation_special_events()

    flag_game = False

    while flag_game == False:

        # executa o turno do jogador
        flag_turn = True
        while flag_turn == True:
            command_confirmation()

            dice_result = dice()
            print('Dado do jogador: ', dice_result)

            position_player += dice_result

            if position_player <= 30:
                if_special_event(position_player, "player")

            if position_player < 30:
                print('Posição do jogador: ', position_player)
            
            if flag_turn == False:
                flag_turn = True
            else:
                flag_turn = False

        if victory_condition(position_player) == True:
            victorious = "player"
            break
        
        # executa o turno da CPU
        flag_turn = True
        while flag_turn == True:
            dice_result = dice()
            print('\nDado da CPU: ', dice_result)

            position_cpu += dice_result

            if position_cpu <= 30:
                if_special_event(position_cpu, "cpu")

            if position_player < 30:
                print('Posição da CPU: ', position_cpu)
        
            if flag_turn == False:
                    flag_turn = True
            else:
                flag_turn = False

        if victory_condition(position_cpu) == True:
            victorious = "cpu"
            break
    
    victory_mode(victorious)

main()