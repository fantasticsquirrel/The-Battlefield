metadata = Hash()
calc = Hash()
data = Hash(default_value=0)

cstl_contract = Variable()
fort_contract = Variable()

random.seed()

@construct
def seed():
    metadata['operator'] = ctx.caller

    #prize calclulation Parameters
    metadata['winner_percent'] = decimal('0.09')
    metadata['house_percent'] = decimal('0.01')

    #battle factors
    metadata['factorA'] = decimal('2.0')
    metadata['factorB'] = decimal('0.35')
    metadata['factorC'] = decimal('0.1')
    metadata['factorD'] = decimal('1.09')
    metadata['factorE'] = decimal('1.005')
    metadata['lower'] = decimal('100.0')
    metadata['upper'] = decimal('100.0')
    metadata['multiplier'] = decimal('5.0')
    metadata['STR_bonus'] = decimal('0.50')

    #LIGHT Unit Base Parameters
    metadata['IN_MS'] = decimal('2.0')
    metadata['IN_MD'] = decimal('1.0')
    metadata['IN_RS'] = decimal('0.0')
    metadata['IN_RD'] = decimal('1.0')

    metadata['AR_MS'] = decimal('0.5')
    metadata['AR_MD'] = decimal('1.0')
    metadata['AR_RS'] = decimal('5.0')
    metadata['AR_RD'] = decimal('2.0')

    metadata['HI_MS'] = decimal('3.0')
    metadata['HI_MD'] = decimal('5.0')
    metadata['HI_RS'] = decimal('0.0')
    metadata['HI_RD'] = decimal('4.0')

    metadata['CA_MS'] = decimal('7.0')
    metadata['CA_MD'] = decimal('4.0')
    metadata['CA_RS'] = decimal('2.0')
    metadata['CA_RD'] = decimal('3.0')

    metadata['CP_MS'] = decimal('0.0')
    metadata['CP_MD'] = decimal('5.0')
    metadata['CP_RS'] = decimal('15.0')
    metadata['CP_RD'] = decimal('10.0')

    #DARK Unit Base Parameters
    metadata['GO_MS'] = decimal('1.0')
    metadata['GO_MD'] = decimal('0.75')
    metadata['GO_RS'] = decimal('0.0')
    metadata['GO_RD'] = decimal('0.75')

    metadata['OA_MS'] = decimal('2.0')
    metadata['OA_MD'] = decimal('1.0')
    metadata['OA_RS'] = decimal('6.0')
    metadata['OA_RD'] = decimal('2.0')

    metadata['OR_MS'] = decimal('3.0')
    metadata['OR_MD'] = decimal('2.0')
    metadata['OR_RS'] = decimal('1.0')
    metadata['OR_RD'] = decimal('2.0')

    metadata['WO_MS'] = decimal('5.0')
    metadata['WO_MD'] = decimal('5.0')
    metadata['WO_RS'] = decimal('0.0')
    metadata['WO_RD'] = decimal('3.0')

    metadata['TR_MS'] = decimal('15.0')
    metadata['TR_MD'] = decimal('10.0')
    metadata['TR_RS'] = decimal('2.0')
    metadata['TR_RD'] = decimal('8.0')

    #Light units per castle
    metadata['UNITS_PER_CSTL']={
        "IN": 200,
        "AR": 91,
        "HI": 67,
        "CA": 48,
        "CP": 24
    }

    #Dark units per fort
    metadata['UNITS_PER_FORT']={
        "GO": 333,
        "OA": 71,
        "OR": 100,
        "WO": 59,
        "TR": 20
    }

    cstl_contract.set('con_silver_credits')
    fort_contract.set('con_silver_credits')

    calc['Castle Wins'] = 0
    calc['Fortress Wins'] = 0

    metadata['terrains'] = ['random','none', 'fields', 'forests', 'hills', 'chaotic']

@export
def change_metadata(key: str, new_value: str, convert_to_decimal: bool=False):
    assert ctx.caller == metadata['operator'], "only operator can set metadata"
    if convert_to_decimal:
        new_value = decimal(new_value)
    metadata[key] = new_value

@export
def update_units_factors():

    factorA = metadata['factorA']
    factorB = metadata['factorB']
    IN_MS = metadata['IN_MS']
    IN_MD = metadata['IN_MD']
    IN_RS = metadata['IN_RS']
    IN_RD = metadata['IN_RD']
    AR_MS = metadata['AR_MS']
    AR_MD = metadata['AR_MD']
    AR_RS = metadata['AR_RS']
    AR_RD = metadata['AR_RD']
    HI_MS = metadata['HI_MS']
    HI_MD = metadata['HI_MD']
    HI_RS = metadata['HI_RS']
    HI_RD = metadata['HI_RD']
    CA_MS = metadata['CA_MS']
    CA_MD = metadata['CA_MD']
    CA_RS = metadata['CA_RS']
    CA_RD = metadata['CA_RD']
    CP_MS = metadata['CP_MS']
    CP_MD = metadata['CP_MD']
    CP_RS = metadata['CP_RS']
    CP_RD = metadata['CP_RD']

    GO_MS = metadata['GO_MS']
    GO_MD = metadata['GO_MD']
    GO_RS = metadata['GO_RS']
    GO_RD = metadata['GO_RD']
    OA_MS = metadata['OA_MS']
    OA_MD = metadata['OA_MD']
    OA_RS = metadata['OA_RS']
    OA_RD = metadata['OA_RD']
    OR_MS = metadata['OR_MS']
    OR_MD = metadata['OR_MD']
    OR_RS = metadata['OR_RS']
    OR_RD = metadata['OR_RD']
    WO_MS = metadata['WO_MS']
    WO_MD = metadata['WO_MD']
    WO_RS = metadata['WO_RS']
    WO_RD = metadata['WO_RD']
    TR_MS = metadata['TR_MS']
    TR_MD = metadata['TR_MD']
    TR_RS = metadata['TR_RS']
    TR_RD = metadata['TR_RD']

    #LIGHT Unit Parameter factors
    IN_MDF = defense_factor(factorA, factorB, IN_MD)
    IN_RDF = defense_factor(factorA, factorB, IN_RD)
    AR_MDF = defense_factor(factorA, factorB, AR_MD)
    AR_RDF = defense_factor(factorA, factorB, AR_RD)
    HI_MDF = defense_factor(factorA, factorB, HI_MD)
    HI_RDF = defense_factor(factorA, factorB, HI_RD)
    CA_MDF = defense_factor(factorA, factorB, CA_MD)
    CA_RDF = defense_factor(factorA, factorB, CA_RD)
    CP_MDF = defense_factor(factorA, factorB, CP_MD)
    CP_RDF = defense_factor(factorA, factorB, CP_RD)

    calc['IN','PARAM'] = [IN_MS, IN_MD, IN_RS, IN_RD, IN_MDF, IN_RDF, 0.0, GO_MS, GO_RS] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS
    calc['AR','PARAM'] = [AR_MS, AR_MD, AR_RS, AR_RD, AR_MDF, AR_RDF, 0.0, OR_MS, OR_RS] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS
    calc['HI','PARAM'] = [HI_MS, HI_MD, HI_RS, HI_RD, HI_MDF, HI_RDF, 0.0, WO_MS, WO_RS] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS
    calc['CA','PARAM'] = [CA_MS, CA_MD, CA_RS, CA_RD, CA_MDF, CA_RDF, 0.0, OA_MS, OA_RS] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS
    calc['CP','PARAM'] = [CP_MS, CP_MD, CP_RS, CP_RD, CP_MDF, CP_RDF, 0.0, TR_MS, TR_RS] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS

    #DARK Unit Parameter factors
    GO_MDF = defense_factor(factorA, factorB, GO_MD)
    GO_RDF = defense_factor(factorA, factorB, GO_RD)
    OA_MDF = defense_factor(factorA, factorB, OA_MD)
    OA_RDF = defense_factor(factorA, factorB, OA_RD)
    OR_MDF = defense_factor(factorA, factorB, OR_MD)
    OR_RDF = defense_factor(factorA, factorB, OR_RD)
    WO_MDF = defense_factor(factorA, factorB, WO_MD)
    WO_RDF = defense_factor(factorA, factorB, WO_RD)
    TR_MDF = defense_factor(factorA, factorB, TR_MD)
    TR_RDF = defense_factor(factorA, factorB, TR_RD)

    calc['GO','PARAM'] = [GO_MS, GO_MD, GO_RS, GO_RD, GO_MDF, GO_RDF, 0.0, HI_MS, HI_RS]
    calc['OA','PARAM'] = [OA_MS, OA_MD, OA_RS, OA_RD, OA_MDF, OA_RDF, 0.0, IN_MS, IN_RS]
    calc['OR','PARAM'] = [OR_MS, OR_MD, OR_RS, OR_RD, OR_MDF, OR_RDF, 0.0, CP_MS, CP_RS]
    calc['WO','PARAM'] = [WO_MS, WO_MD, WO_RS, WO_RD, WO_MDF, WO_RDF, 0.0, AR_MS, AR_RS]
    calc['TR','PARAM'] = [TR_MS, TR_MD, TR_RS, TR_RD, TR_MDF, TR_RDF, 0.0, CA_MS, CA_RS]

    #update calc list from metadata parameters. This will be called instead of each individual metadata tag to reduce stamp usage.
    calc['factor_list'] = [metadata['factorC'], metadata['factorD'], metadata['factorE'], metadata['lower'], metadata['upper'], metadata['multiplier'], metadata['STR_bonus']]

def defense_factor(factorA, factorB, defense):
    DF = factorA * defense + (factorB * defense) ** 3
    return DF

@export
def battle(match_id: str):

    if data[match_id, 'private'] == 1:
        playerlist = data[match_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match and cannot start the battle. Contact the match creator if you wish to join.'

    total_cstl = data[match_id,'total_cstl']
    total_fort = data[match_id,'total_fort']
    assert total_cstl == total_fort and total_cstl == data[match_id, 'battle_size'], f'There are {total_cstl} CSTL and {total_fort} FORT staked. These must be equal and filled to max capacity for a battle to be initiated.'
    operator = metadata['operator']

    terrains = metadata['terrains']
    if data[match_id, 'terrain'] == 0 :
        terrain_type = terrains[random.randint(1, 5)]
    else:
        terrain_type = terrains[data[match_id, 'terrain']]

    factor_list = calc['factor_list']
    factorC = factor_list[0]
    factorD = factor_list[1]
    factorE = factor_list[2]
    lower = factor_list[3]
    upper = factor_list[4]
    multiplier = factor_list[5]
    STR_bonus = factor_list[6]

    IN_PARAM = calc['IN','PARAM'] #IN_MS = IN_PARAM[0] :: #IN_MD = IN_PARAM[1] :: #IN_RS = IN_PARAM[2] :: #IN_RD = IN_PARAM[3] :: #IN_MDF = IN_PARAM[4] :: #IN_RDF = IN_PARAM[5] :: #IN_count = IN_PARAM[6]
    AR_PARAM = calc['AR','PARAM']
    HI_PARAM = calc['HI','PARAM']
    CA_PARAM = calc['CA','PARAM']
    CP_PARAM = calc['CP','PARAM']

    GO_PARAM = calc['GO','PARAM']
    OA_PARAM = calc['OA','PARAM']
    OR_PARAM = calc['OR','PARAM']
    WO_PARAM = calc['WO','PARAM']
    TR_PARAM = calc['TR','PARAM']

    L_units = data[match_id, 'L_units']

    IN_PARAM[6] = L_units['IN'] #transfers all unit counts from staking tokens into the parameter list for use in the functions
    AR_PARAM[6] = L_units['AR']
    HI_PARAM[6] = L_units['HI']
    CA_PARAM[6] = L_units['CA']
    CP_PARAM[6] = L_units['CP']

    D_units = data[match_id, 'D_units']

    GO_PARAM[6] = D_units['GO']
    OA_PARAM[6] = D_units['OA']
    OR_PARAM[6] = D_units['OR']
    WO_PARAM[6] = D_units['WO']
    TR_PARAM[6] = D_units['TR']


    battle_turn = 0
    battle_mult = battle_mult_update(terrain_type, battle_turn)

    UNITS_TOTAL = calc_army_update(factorC, factorD, battle_mult[0], battle_mult[1], IN_PARAM, AR_PARAM, HI_PARAM, CA_PARAM, CP_PARAM, GO_PARAM, OA_PARAM, OR_PARAM, WO_PARAM, TR_PARAM) #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED

    while UNITS_TOTAL[0] > 0 and UNITS_TOTAL[1] > 0:

        battle_mult = battle_mult_update(terrain_type, battle_turn)
        L_ARMY_PROPERTIES = UNITS_TOTAL[2]
        D_ARMY_PROPERTIES = UNITS_TOTAL[3]

        IN_COUNT = IN_PARAM[6] #transfers all unit counts to a separate variable so loss calcs aren't dependant on who is first in the code.
        AR_COUNT = AR_PARAM[6]
        HI_COUNT = HI_PARAM[6]
        CA_COUNT = CA_PARAM[6]
        CP_COUNT = CP_PARAM[6]

        GO_COUNT = GO_PARAM[6]
        OA_COUNT = OA_PARAM[6]
        OR_COUNT = OR_PARAM[6]
        WO_COUNT = WO_PARAM[6]
        TR_COUNT = TR_PARAM[6]

        if IN_PARAM[6] > 0:
            IN_PARAM[6] = calc_losses(IN_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], GO_COUNT, L_ARMY_PROPERTIES, D_ARMY_PROPERTIES)
        if AR_PARAM[6] > 0:
            AR_PARAM[6] = calc_losses(AR_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], OR_COUNT, L_ARMY_PROPERTIES, D_ARMY_PROPERTIES)
        if HI_PARAM[6] > 0:
            HI_PARAM[6] = calc_losses(HI_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], WO_COUNT, L_ARMY_PROPERTIES, D_ARMY_PROPERTIES)
        if CA_PARAM[6] > 0:
            CA_PARAM[6] = calc_losses(CA_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], OA_COUNT, L_ARMY_PROPERTIES, D_ARMY_PROPERTIES)
        if CP_PARAM[6] > 0:
            CP_PARAM[6] = calc_losses(CP_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], TR_COUNT, L_ARMY_PROPERTIES, D_ARMY_PROPERTIES)

        if GO_PARAM[6] > 0:
            GO_PARAM[6] = calc_losses(GO_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], HI_COUNT, D_ARMY_PROPERTIES, L_ARMY_PROPERTIES)
        if OA_PARAM[6] > 0:
            OA_PARAM[6] = calc_losses(OA_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], IN_COUNT, D_ARMY_PROPERTIES, L_ARMY_PROPERTIES)
        if OR_PARAM[6] > 0:
            OR_PARAM[6] = calc_losses(OR_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], CP_COUNT, D_ARMY_PROPERTIES, L_ARMY_PROPERTIES)
        if WO_PARAM[6] > 0:
            WO_PARAM[6] = calc_losses(WO_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], AR_COUNT, D_ARMY_PROPERTIES, L_ARMY_PROPERTIES)
        if TR_PARAM[6] > 0:
            TR_PARAM[6] = calc_losses(TR_PARAM, factorE, multiplier, lower, upper, STR_bonus, battle_mult[0], battle_mult[1], CA_COUNT, D_ARMY_PROPERTIES, L_ARMY_PROPERTIES)

        UNITS_TOTAL = calc_army_update(factorC, factorD, battle_mult[0], battle_mult[1], IN_PARAM, AR_PARAM, HI_PARAM, CA_PARAM, CP_PARAM, GO_PARAM, OA_PARAM, OR_PARAM, WO_PARAM, TR_PARAM) #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED
        battle_turn += 1

    if UNITS_TOTAL[0] > 0 and UNITS_TOTAL[1] <= 0:
        winner = 'Castle'
        calc['Castle Wins'] += 1
    elif UNITS_TOTAL[1] > 0 and UNITS_TOTAL[0] <= 0:
        winner = 'Fortress'
        calc['Fortress Wins'] += 1
    else:
        winner = 'error'

    calc['Battle_Results'] = f'There are {int(IN_PARAM[6])} infantry, {int(AR_PARAM[6])} archers, {int(HI_PARAM[6])} heavy infantry, {int(CA_PARAM[6])} cavalry, {int(CP_PARAM[6])} catapults remaining in the LIGHT army, and there are {int(GO_PARAM[6])} goblins, {int(OA_PARAM[6])} orc archers, {int(OR_PARAM[6])} orcs, {int(WO_PARAM[6])} wolves, {int(TR_PARAM[6])} trolls remaining in the DARK army.'

    disperse(operator, winner, match_id)

    data['total_turns'] = battle_turn #may not need long term. This is just to track the total turns a battle took.

def battle_mult_update(terrain_type, battle_turn): # ['none', 'fields', 'forests', 'hills', 'chaotic']
    if terrain_type == 'none':
        battle_m_mult = 1
        battle_r_mult = 1

    if terrain_type == 'fields':
        battle_m_mult = battle_turn * 0.05 + 0.25
        battle_r_mult = 1 - (battle_turn * 0.04)

    if terrain_type == 'forests':
        battle_m_mult = 1 - (battle_turn * 0.04)
        battle_r_mult = battle_turn * 0.05 + 0.25

    if terrain_type == 'hills':
        if (battle_turn % 2) == 0:
            battle_m_mult = 0.75 - (battle_turn * 0.05)
            battle_r_mult = 0.75 + (battle_turn * 0.05)
        else:
            battle_m_mult = 0.75 + (battle_turn * 0.05)
            battle_r_mult = 0.75 - (battle_turn * 0.05)

    if terrain_type == 'chaotic':
        battle_m_mult = random.randint(0, 100) * 0.01
        battle_r_mult = random.randint(0, 100) * 0.01

    if battle_m_mult > 1 : battle_m_mult = 1
    if battle_m_mult < 0.25 : battle_m_mult = 0.25
    if battle_r_mult > 1 : battle_r_mult = 1
    if battle_r_mult < 0.25 : battle_r_mult = 0.25

    battle_mult = [battle_m_mult, battle_r_mult]
    return battle_mult

def calc_losses(unit_param, factorE, multiplier, lower, upper, STR_bonus, BATTLE_M_MULT, BATTLE_R_MULT, weakness_count, faction_unit_list, faction_other_list):

    unit_update = (100 - (factorE ** ((((faction_other_list[0] - faction_unit_list[1] + (STR_bonus * BATTLE_M_MULT * (unit_param[7] * weakness_count)))/faction_unit_list[1]) * \
    random.randint(lower, upper) * faction_other_list[4])-unit_param[4]) + factorE ** ((((faction_other_list[2] - faction_unit_list[3] + (STR_bonus * BATTLE_R_MULT * (unit_param[8] * weakness_count))) \
    / faction_unit_list[3]) * random.randint(lower, upper) * faction_other_list[5])-unit_param[5])) * multiplier) / 100 * unit_param[6]

    if unit_update < 0:
        unit_update = 0

    return unit_update

def calc_army_update(factorC, factorD, BATTLE_M_MULT, BATTLE_R_MULT, IN_PARAM, AR_PARAM, HI_PARAM, CA_PARAM, CP_PARAM, GO_PARAM, OA_PARAM, OR_PARAM, WO_PARAM, TR_PARAM): #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED

    L_UNITS_IN = IN_PARAM[6]
    L_UNITS_AR = AR_PARAM[6]
    L_UNITS_HI = HI_PARAM[6]
    L_UNITS_CA = CA_PARAM[6]
    L_UNITS_CP = CP_PARAM[6]

    D_UNITS_GO = GO_PARAM[6]
    D_UNITS_OA = OA_PARAM[6]
    D_UNITS_OR = OR_PARAM[6]
    D_UNITS_WO = WO_PARAM[6]
    D_UNITS_TR = TR_PARAM[6]

    L_UNITS_TOTAL = L_UNITS_IN + L_UNITS_AR + L_UNITS_HI + L_UNITS_CA + L_UNITS_CP #add all other L units to this variable when other units are added

    D_UNITS_TOTAL = D_UNITS_GO + D_UNITS_OA + D_UNITS_OR + D_UNITS_WO + D_UNITS_TR #add all other D units to this variable when other units are added

    if L_UNITS_TOTAL > 0:
        #calculate updated L army totals
        L_ARMY_MS = (L_UNITS_IN * IN_PARAM[0] + L_UNITS_AR * AR_PARAM[0] + L_UNITS_HI * HI_PARAM[0] + L_UNITS_CA * CA_PARAM[0] + L_UNITS_CP * CP_PARAM[0]) * BATTLE_M_MULT #add all other L unit strengths here when other units are added
        L_ARMY_MD = (L_UNITS_IN * IN_PARAM[1] + L_UNITS_AR * AR_PARAM[1] + L_UNITS_HI * HI_PARAM[1] + L_UNITS_CA * CA_PARAM[1] + L_UNITS_CP * CP_PARAM[1]) #add all other L unit DEFENSE here when other units are added
        L_ARMY_RS = (L_UNITS_IN * IN_PARAM[2] + L_UNITS_AR * AR_PARAM[2] + L_UNITS_HI * HI_PARAM[2] + L_UNITS_CA * CA_PARAM[2] + L_UNITS_CP * CP_PARAM[2]) * BATTLE_R_MULT
        L_ARMY_RD = (L_UNITS_IN * IN_PARAM[3] + L_UNITS_AR * AR_PARAM[3] + L_UNITS_HI * HI_PARAM[3] + L_UNITS_CA * CA_PARAM[3] + L_UNITS_CP * CP_PARAM[3])
        L_ARMY_MS_FACTOR = factorC * (L_ARMY_MS / L_UNITS_TOTAL) + factorD ** (L_ARMY_MS / L_UNITS_TOTAL)
        L_ARMY_RS_FACTOR = factorC * (L_ARMY_RS / L_UNITS_TOTAL) + factorD ** (L_ARMY_RS / L_UNITS_TOTAL)
        L_ARMY_PROPERTIES = [L_ARMY_MS, L_ARMY_MD, L_ARMY_RS, L_ARMY_RD, L_ARMY_MS_FACTOR, L_ARMY_RS_FACTOR]
    else:
        L_ARMY_PROPERTIES=[0,0,0,0,0,0]

    if D_UNITS_TOTAL > 0:
        #calculate updated D army totals
        D_ARMY_MS = (D_UNITS_GO * GO_PARAM[0] + D_UNITS_OA * OA_PARAM[0] + D_UNITS_OR * OR_PARAM[0] + D_UNITS_WO * WO_PARAM[0] + D_UNITS_TR * TR_PARAM[0]) * BATTLE_M_MULT
        D_ARMY_MD = (D_UNITS_GO * GO_PARAM[1] + D_UNITS_OA * OA_PARAM[1] + D_UNITS_OR * OR_PARAM[1] + D_UNITS_WO * WO_PARAM[1] + D_UNITS_TR * TR_PARAM[1])
        D_ARMY_RS = (D_UNITS_GO * GO_PARAM[2] + D_UNITS_OA * OA_PARAM[2] + D_UNITS_OR * OR_PARAM[2] + D_UNITS_WO * WO_PARAM[2] + D_UNITS_TR * TR_PARAM[2]) * BATTLE_R_MULT
        D_ARMY_RD = (D_UNITS_GO * GO_PARAM[3] + D_UNITS_OA * OA_PARAM[3] + D_UNITS_OR * OR_PARAM[3] + D_UNITS_WO * WO_PARAM[3] + D_UNITS_TR * TR_PARAM[3])
        D_ARMY_MS_FACTOR = factorC * (D_ARMY_MS / D_UNITS_TOTAL) + factorD ** (D_ARMY_MS / D_UNITS_TOTAL)
        D_ARMY_RS_FACTOR = factorC * (D_ARMY_RS / D_UNITS_TOTAL) + factorD ** (D_ARMY_RS / D_UNITS_TOTAL)
        D_ARMY_PROPERTIES = [D_ARMY_MS, D_ARMY_MD, D_ARMY_RS, D_ARMY_RD, D_ARMY_MS_FACTOR, D_ARMY_RS_FACTOR]
    else:
        D_ARMY_PROPERTIES=[0,0,0,0,0,0]

    UNITS_TOTAL = [L_UNITS_TOTAL, D_UNITS_TOTAL, L_ARMY_PROPERTIES, D_ARMY_PROPERTIES]

    return UNITS_TOTAL

def disperse(operator, winner, match_id):
    #calculate winnings where winners get 1.09, loser gets 0.90 and house gets 0.01

    SC = importlib.import_module(cstl_contract.get())
    cstl_staked_wallets = data[match_id, 'cstl_staked_wallets']
    fort_staked_wallets = data[match_id, 'fort_staked_wallets']
    winner_percent = metadata['winner_percent']
    house_percent = metadata['house_percent']
    loser_percent = 1 - winner_percent - house_percent

    if winner == 'Castle':
        #send winnings to CASTLE stakers
        for key, value in dict(cstl_staked_wallets).items():
            SC.transfer(amount=value * (1 + winner_percent) , to=key)
            SC.transfer(amount= (value * house_percent), to=operator) #make variable for OWNER

        for key, value in dict(fort_staked_wallets).items():
            SC.transfer(amount= (value * loser_percent), to=key)
    if winner == 'Fortress':
        #send winnings to FORTRESS stakers
        for key, value in dict(fort_staked_wallets).items():
            SC.transfer(amount=value * (1 + winner_percent), to=key)
            SC.transfer(amount= (value * house_percent), to=operator)

        for key, value in dict(cstl_staked_wallets).items():
            SC.transfer(amount= (value * loser_percent), to=key)

    data[match_id, 'cstl_staked_wallets'] = {} #clears all staked wallets from storage so a new battle can start
    data[match_id, 'fort_staked_wallets'] = {}
    data[match_id, 'total_cstl'] = 0
    data[match_id, 'total_fort'] = 0
    data[match_id, 'players'] = []
    data[match_id, 'match_owner'] = None
    data[match_id, 'terrain'] = None

    data[match_id, 'L_units'] = {}
    data[match_id, 'D_units'] = {}

@export
def stake_CSTL(match_id: str, IN_CSTL: int=0, AR_CSTL: int=0, HI_CSTL: int=0, CA_CSTL: int=0,  CP_CSTL: int=0):

#check to see if match is private. If public, don't check the list. If private, check to see if the player is on player list.
    if data[match_id, 'private'] == 1:
        playerlist = data[match_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match. Contact the match creator if you wish to join.'
    cstl_amount = IN_CSTL + AR_CSTL + HI_CSTL + CA_CSTL + CP_CSTL
    assert cstl_amount <= data[match_id, 'max_stake_per'], f"You can only stake up to {data[match_id, 'max_stake_per']} tokens per transaction. Stake less and try again."
    assert data[match_id, 'total_cstl'] + cstl_amount <= data[match_id, 'battle_size'], f"You are attempting to stake {cstl_amount} which is more than the {data[match_id, 'battle_size'] - data[match_id, 'total_cstl']} remaining to be staked for this battle. Please try again with a smaller number."

    staked_wallets = data[match_id, 'cstl_staked_wallets']
    cstl = importlib.import_module(cstl_contract.get())
    UNITS_PER_CSTL = metadata['UNITS_PER_CSTL']
    L_units = data[match_id, 'L_units']

    IN_amount = UNITS_PER_CSTL["IN"] * IN_CSTL
    AR_amount = UNITS_PER_CSTL["AR"] * AR_CSTL
    HI_amount = UNITS_PER_CSTL["HI"] * HI_CSTL
    CA_amount = UNITS_PER_CSTL["CA"] * CA_CSTL
    CP_amount = UNITS_PER_CSTL["CP"] * CP_CSTL

    cstl.transfer_from(amount=cstl_amount, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: cstl_amount})
    else:
        staked_wallets[ctx.caller] += cstl_amount

    data[match_id, 'cstl_staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data[match_id, 'total_cstl'] += cstl_amount #adds total CSTL to storage for calculating rewards

    L_units['IN'] += IN_amount
    L_units['AR'] += AR_amount
    L_units['HI'] += HI_amount
    L_units['CA'] += CA_amount
    L_units['CP'] += CP_amount

    data[match_id, 'L_units'] = L_units

@export
def stake_FORT(match_id: str, GO_FORT: int=0, OA_FORT: int=0, OR_FORT: int=0,  WO_FORT: int=0, TR_FORT: int=0):

#check to see if match is private. If public, don't check the list. If private, check to see if the player is on player list.
    if data[match_id, 'private'] == 1:
        playerlist = data[match_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match. Contact the match creator if you wish to join.'
    fort_amount = GO_FORT + OA_FORT + OR_FORT + WO_FORT + TR_FORT
    assert fort_amount <= data[match_id, 'max_stake_per'], f"You can only stake up to {data[match_id, 'max_stake_per']} tokens per transaction. Stake less and try again."
    assert data[match_id, 'total_fort'] + fort_amount <= data[match_id, 'battle_size'], f"You are attempting to stake {fort_amount} which is more than the {data[match_id, 'battle_size'] - data[match_id, 'total_fort']} remaining to be staked for this battle. Please try again with a smaller number."

    staked_wallets = data[match_id, 'fort_staked_wallets']
    fort = importlib.import_module(fort_contract.get())
    UNITS_PER_FORT = metadata['UNITS_PER_FORT']
    D_units = data[match_id, 'D_units']

    GO_amount = UNITS_PER_FORT["GO"] * GO_FORT
    OA_amount = UNITS_PER_FORT["OA"] * OA_FORT
    OR_amount = UNITS_PER_FORT["OR"] * OR_FORT
    WO_amount = UNITS_PER_FORT["WO"] * WO_FORT
    TR_amount = UNITS_PER_FORT["TR"] * TR_FORT

    fort.transfer_from(amount=fort_amount, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: fort_amount})
    else:
        staked_wallets[ctx.caller] += fort_amount

    data[match_id, 'fort_staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data[match_id, 'total_fort'] += fort_amount #adds total FORT to storage for calculating rewards

    D_units['GO'] += GO_amount
    D_units['OA'] += OA_amount
    D_units['OR'] += OR_amount
    D_units['WO'] += WO_amount
    D_units['TR'] += TR_amount

    data[match_id, 'D_units'] = D_units

@export
def new_match(match_id : str, terrain: int, private : bool, battle_size : int = 500, max_stake_per_transaction : int = 500):

    assert bool(data[match_id, 'match_owner']) == False, "This match has already been created, please create one with a different name."

    data[match_id, 'match_owner'] = ctx.caller
    data[match_id, 'private'] = private
    data[match_id, 'players'] = [ctx.caller]
    data[match_id, 'terrain'] = terrain
    data[match_id, 'max_stake_per'] = max_stake_per_transaction
    data[match_id, 'battle_size'] = battle_size
    data[match_id, 'cstl_staked_wallets'] = {}
    data[match_id, 'fort_staked_wallets'] = {}

    data[match_id, 'L_units'] = {
        "IN": 0,
        "AR": 0,
        "HI": 0,
        "CA": 0,
        "CP": 0
    }

    data[match_id, 'D_units'] = {
        "GO": 0,
        "OA": 0,
        "OR": 0,
        "WO": 0,
        "TR": 0
    }

@export
def add_players(match_id : str, add1: str='', add2: str='', add3: str='', add4: str=''):

    assert data[match_id, 'match_owner'] == ctx.caller, 'You are not the match creator and cannot add players to this match.'
    assert data[match_id, 'private'] == True, 'This is a public game and individual players cannot be added.'

    addlist = [add1, add2, add3, add4]
    playerlist = data[match_id, 'players']

    for x in addlist:
        playerlist.append(x)

    data[match_id, 'players'] = playerlist

@export
def cancel_match(match_id : str):

    assert data[match_id, 'match_owner'] == ctx.caller, 'You are not the match creator and cannot cancel this match.'
    tokens = data[match_id, 'battle_size']
    assert tokens > (data[match_id, 'total_cstl'] + data[match_id, 'total_fort']), 'The match is over half full and can no longer be cancelled.'

    SC = importlib.import_module(cstl_contract.get())

    cstl_staked_wallets = data[match_id, 'cstl_staked_wallets']
    fort_staked_wallets = data[match_id, 'fort_staked_wallets']

    for key, value in dict(cstl_staked_wallets).items():
        SC.transfer(amount=value, to=key)

    for key, value in dict(fort_staked_wallets).items():
        SC.transfer(amount=value, to=key)

    data[match_id, 'cstl_staked_wallets'] = {} #clears all staked wallets from storage so a new battle can start
    data[match_id, 'fort_staked_wallets'] = {}
    data[match_id, 'total_cstl'] = 0
    data[match_id, 'total_fort'] = 0
    data[match_id, 'players'] = []
    data[match_id, 'match_owner'] = None
    data[match_id, 'terrain'] = None

    data[match_id, 'L_units'] = {}
    data[match_id, 'D_units'] = {}

#Add data to store winner for each match, and then add a reset function for only me to run, so I can check balance of factions long term and reset after I update a parameter.

@export
def reset_stats():
    assert ctx.caller == metadata['operator'], "Only the operator can reset statistics."
    calc['Castle Wins'] = 0
    calc['Fortress Wins'] = 0




