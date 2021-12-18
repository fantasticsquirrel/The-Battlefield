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
    metadata['costA'] = decimal('1.1')
    metadata['cost_base'] = decimal('100.0')
    metadata['lower'] = decimal('100.0')
    metadata['upper'] = decimal('100.0')
    metadata['multiplier'] = decimal('10.0')
    metadata['STR_bonus'] = decimal('0.50')

    metadata['PLACEHOLDER','MS'] = decimal('0.0')
    metadata['PLACEHOLDER','MD'] = decimal('0.0')
    metadata['PLACEHOLDER','RS'] = decimal('0.0')
    metadata['PLACEHOLDER','RD'] = decimal('0.0')

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

    #DARK Unit Base Parameters
    metadata['GO_MS'] = decimal('1.0')
    metadata['GO_MD'] = decimal('0.75')
    metadata['GO_RS'] = decimal('0.0')
    metadata['GO_RD'] = decimal('0.75')

    metadata['OA_MS'] = decimal('2.0')
    metadata['OA_MD'] = decimal('1.0')
    metadata['OA_RS'] = decimal('6.0')
    metadata['OA_RD'] = decimal('2.0')

    metadata['OR_MS'] = decimal('2.0')
    metadata['OR_MD'] = decimal('1.0')
    metadata['OR_RS'] = decimal('6.0')
    metadata['OR_RD'] = decimal('2.0')

    #TEMPORARY PLACEHOLDERS FOR TROOP COUNTS
    metadata['TEMP_IN'] = decimal('200.0')
    metadata['TEMP_AR'] = decimal('50.0')
    metadata['TEMP_HI'] = decimal('75.0')

    metadata['TEMP_GO'] = decimal('400.0')
    metadata['TEMP_OA'] = decimal('25.0')
    metadata['TEMP_OR'] = decimal('100.0')

    #Light units per castle
    metadata['UNITS_PER_CSTL']={
        "IN": 200,
        "AR": 91,
        "HI": 67
    }

    #Dark units per fort
    metadata['UNITS_PER_FORT']={
        "GO": 333,
        "OA": 71,
        "OR": 100
    }

    cstl_contract.set('con_castle')
    fort_contract.set('con_fortress')

    data['cstl_staked_wallets'] = {}
    data['fort_staked_wallets'] = {}

    metadata['CSTL_FORT_PER_BATTLE'] = 100

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

    #LIGHT Unit Parameter factors
    IN_MDF = factorA * metadata['IN_MD'] + (factorB * metadata['IN_MD']) ** 3
    IN_RDF = factorA * metadata['IN_RD'] + (factorB * metadata['IN_RD']) ** 3
    #IN_WEAKNESS_1 =
    AR_MDF = factorA * metadata['AR_MD'] + (factorB * metadata['AR_MD']) ** 3
    AR_RDF = factorA * metadata['AR_RD'] + (factorB * metadata['AR_RD']) ** 3

    HI_MDF = factorA * metadata['HI_MD'] + (factorB * metadata['HI_MD']) ** 3
    HI_RDF = factorA * metadata['HI_RD'] + (factorB * metadata['HI_RD']) ** 3


    calc['IN','PARAM'] = [metadata['IN_MS'], metadata['IN_MD'], metadata['IN_RS'], metadata['IN_RD'], IN_MDF, IN_RDF, 0.0] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS
    calc['AR','PARAM'] = [metadata['AR_MS'], metadata['AR_MD'], metadata['AR_RS'], metadata['AR_RD'], AR_MDF, AR_RDF, 0.0] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS
    calc['HI','PARAM'] = [metadata['HI_MS'], metadata['HI_MD'], metadata['HI_RS'], metadata['HI_RD'], HI_MDF, HI_RDF, 0.0] #ADD STRENGTHS AND WEAKNESSES TO UNIT PARAMS

    #DARK Unit Parameter factors
    GO_MDF = factorA * metadata['GO_MD'] + (factorB * metadata['GO_MD']) ** 3
    GO_RDF = factorA * metadata['GO_RD'] + (factorB * metadata['GO_RD']) ** 3

    OA_MDF = factorA * metadata['OA_MD'] + (factorB * metadata['OA_MD']) ** 3
    OA_RDF = factorA * metadata['OA_RD'] + (factorB * metadata['OA_RD']) ** 3

    OR_MDF = factorA * metadata['OR_MD'] + (factorB * metadata['OR_MD']) ** 3
    OR_RDF = factorA * metadata['OR_RD'] + (factorB * metadata['OR_RD']) ** 3

    calc['GO','PARAM'] = [metadata['GO_MS'], metadata['GO_MD'], metadata['GO_RS'], metadata['GO_RD'], GO_MDF, GO_RDF, 0.0]
    calc['OA','PARAM'] = [metadata['OA_MS'], metadata['OA_MD'], metadata['OA_RS'], metadata['OA_RD'], OA_MDF, OA_RDF, 0.0]
    calc['OR','PARAM'] = [metadata['OR_MS'], metadata['OR_MD'], metadata['OR_RS'], metadata['OR_RD'], OR_MDF, OR_RDF, 0.0]

    #update calc list from metadata parameters. This will be called instead of each individual metadata tag to reduce stamp usage.
    calc['factor_list'] = [metadata['factorC'], metadata['factorD'], metadata['factorE'], metadata['lower'], metadata['upper'], metadata['multiplier'], metadata['STR_bonus']]

@export
def battle():

    total_cstl = data['total_cstl']
    total_fort = data['total_fort']
    assert total_cstl == total_fort and total_cstl == metadata['CSTL_FORT_PER_BATTLE'], f'There are {total_cstl} CSTL and {total_fort} FORT staked. These must be equal for a battle to be initiated.'
    operator = metadata['operator']
    terrains = ['none', 'fields', 'forests', 'hills', 'chaotic']
    terrain_type = terrains[random.randint(0, 3)]
    data['terrain_type'] = terrain_type #not needed long term since it's just to see what terrain type was picked.

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

    GO_PARAM = calc['GO','PARAM']
    OA_PARAM = calc['OA','PARAM']
    OR_PARAM = calc['OR','PARAM']

    #MULTIPLIER to change range vs melee strength through the battle. For now it's set to 1 for the whole battle
    BATTLE_M_MULT = 1
    BATTLE_R_MULT = 1

    #battle setup
    IN_PARAM[6] = data['IN'] #add all other units here as they're added
    AR_PARAM[6] = data['AR']
    HI_PARAM[6] = data['HI']

    GO_PARAM[6] = data['GO']
    OA_PARAM[6] = data['OA']
    OR_PARAM[6] = data['OR']

    UNITS_TOTAL = calc_army_update(factorC, factorD, BATTLE_M_MULT, BATTLE_R_MULT, IN_PARAM, AR_PARAM, HI_PARAM, GO_PARAM, OA_PARAM, OR_PARAM) #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED

    battle_turn = 0

    while UNITS_TOTAL[0] > 0 and UNITS_TOTAL[1] > 0:

        battle_mult = battle_mult_update(terrain_type, battle_turn)

        IN_PARAM[6] = calc_losses(IN_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'L', 'D', 'IN', battle_mult[0], battle_mult[1]) # 3 STRING paremeters are faction of unit, opposing faction, unit name
        AR_PARAM[6] = calc_losses(AR_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'L', 'D', 'AR', battle_mult[0], battle_mult[1]) # 3 STRING paremeters are faction of unit, opposing faction, unit name
        HI_PARAM[6] = calc_losses(HI_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'L', 'D', 'HI', battle_mult[0], battle_mult[1]) # 3 STRING paremeters are faction of unit, opposing faction, unit name

        GO_PARAM[6] = calc_losses(GO_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'D', 'L', 'GO', battle_mult[0], battle_mult[1])
        OA_PARAM[6] = calc_losses(OA_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'D', 'L', 'OA', battle_mult[0], battle_mult[1])
        OR_PARAM[6] = calc_losses(OR_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'D', 'L', 'OR', battle_mult[0], battle_mult[1])

        UNITS_TOTAL = calc_army_update(factorC, factorD, BATTLE_M_MULT, BATTLE_R_MULT, IN_PARAM, AR_PARAM, HI_PARAM, GO_PARAM, OA_PARAM, OR_PARAM) #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED
        battle_turn += 1

    if UNITS_TOTAL[0] > 0 and UNITS_TOTAL[1] <= 0:
        winner = 'L'
    elif UNITS_TOTAL[1] > 0 and UNITS_TOTAL[0] <= 0:
        winner = 'D'
    else:
        winner = 'error'

    disperse(operator, winner)

    data['cstl_staked_wallets'].clear() #clears all staked wallets from storage so a new battle can start
    data['fort_staked_wallets'].clear()

    data['IN'] = 0 #add all other units here as they're added
    data['AR'] = 0
    data['HI'] = 0

    data['GO'] = 0
    data['OA'] = 0
    data['OR'] = 0

def battle_mult_update(terrain_type, battle_turn): # ['none', 'fields', 'forests', 'hills', 'chaotic']
    if terrain_type == 'none':
        battle_m_mult = 1
        battle_r_mult = 1

    if terrain_type == 'fields':
        battle_m_mult = battle_turn * 0.1 + 0.25
        battle_r_mult = 1 - (battle_turn * 0.1)

    if terrain_type == 'forests':
        battle_m_mult = 1 - (battle_turn * 0.1)
        battle_r_mult = battle_turn * 0.1 + 0.25

    if terrain_type == 'hills':
        if (battle_turn % 2) == 0:
            battle_m_mult = 0.75 - (battle_turn * 0.1)
            battle_r_mult = 0.75 + (battle_turn * 0.1)
        else:
            battle_m_mult = 0.75 + (battle_turn * 0.1)
            battle_r_mult = 0.75 - (battle_turn * 0.1)

    if terrain_type == 'chaotic':
        battle_m_mult = random.randint(0, 100) * 0.01
        battle_r_mult = random.randint(0, 100) * 0.01

    if battle_m_mult > 1 : battle_m_mult = 1
    if battle_m_mult < 0.25 : battle_m_mult = 0.25
    if battle_r_mult > 1 : battle_r_mult = 1
    if battle_r_mult < 0.25 : battle_r_mult = 0.25

    battle_mult = [battle_m_mult, battle_r_mult]
    return battle_mult

@export
def calc_losses(unit_param: float, factorE: float, multiplier: float, lower : float, upper: float, STR_bonus: float, faction_unit: str, faction_other: str, unit_type: str, BATTLE_M_MULT: float, BATTLE_R_MULT: float, Mweak1: str='PLACEHOLDER', Mweak1count: float=0, Mweak2: str='PLACEHOLDER', Mweak2count: float=0,Rweak1: str='PLACEHOLDER', Rweak1count: float=0,Rweak2: str='PLACEHOLDER',Rweak2count: float=0):

    faction_unit_list = calc[faction_unit,'ARMY','PROPERTIES'] #[L_ARMY_MS, L_ARMY_MD, L_ARMY_RS, L_ARMY_RD, L_ARMY_MS_FACTOR, L_ARMY_RS_FACTOR]
    faction_other_list = calc[faction_other,'ARMY','PROPERTIES'] #[D_ARMY_MS, D_ARMY_MD, D_ARMY_RS, D_ARMY_RD, D_ARMY_MS_FACTOR, D_ARMY_RS_FACTOR]

    unit_update = (100 - (factorE ** ((((faction_other_list[0] - faction_unit_list[1] + (STR_bonus * BATTLE_M_MULT * (1 * 0 + 1 * 0)))/faction_unit_list[1]) * \
    random.randint(lower, upper) * faction_other_list[4])-unit_param[4]) + factorE ** ((((faction_other_list[2] - faction_unit_list[3] + (STR_bonus * BATTLE_R_MULT * (1 * 0 + 1 * 0))) \
    / faction_unit_list[1]) * random.randint(lower, upper) * faction_other_list[5])-unit_param[5])) * multiplier) / 100 * unit_param[6] #where it has 1 * 0 + 1 * 0 add weaknesses for this unit. the first one is melee weakesses and the second set is range weaknesses

    if unit_update < 0:
        unit_update = 0

    return unit_update

@export
def calc_army_update(factorC: float, factorD: float, BATTLE_M_MULT: float, BATTLE_R_MULT: float, IN_PARAM: float, AR_PARAM: float, HI_PARAM: float, GO_PARAM: float, OA_PARAM: float, OR_PARAM: float): #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED

    L_UNITS_IN = IN_PARAM[6]
    L_UNITS_AR = AR_PARAM[6]
    L_UNITS_HI = HI_PARAM[6]

    D_UNITS_GO = GO_PARAM[6]
    D_UNITS_OA = OA_PARAM[6]
    D_UNITS_OR = OR_PARAM[6]

    L_UNITS_TOTAL = L_UNITS_IN + L_UNITS_AR + L_UNITS_HI #add all other L units to this variable when other units are added

    D_UNITS_TOTAL = D_UNITS_GO + D_UNITS_OA + D_UNITS_OR #add all other D units to this variable when other units are added

    if L_UNITS_TOTAL > 0:
        #calculate updated L army totals
        L_ARMY_MS = (L_UNITS_IN * IN_PARAM[0] + L_UNITS_AR * AR_PARAM[0] + L_UNITS_HI * HI_PARAM[0]) * BATTLE_M_MULT #add all other L unit strengths here when other units are added
        L_ARMY_MD = (L_UNITS_IN * IN_PARAM[1] + L_UNITS_AR * AR_PARAM[1] + L_UNITS_HI * HI_PARAM[1]) #add all other L unit DEFENSE here when other units are added
        L_ARMY_RS = (L_UNITS_IN * IN_PARAM[2] + L_UNITS_AR * AR_PARAM[2] + L_UNITS_HI * HI_PARAM[2]) * BATTLE_R_MULT
        L_ARMY_RD = (L_UNITS_IN * IN_PARAM[3] + L_UNITS_AR * AR_PARAM[3] + L_UNITS_HI * HI_PARAM[3])
        L_ARMY_AVG_MS = L_ARMY_MS / L_UNITS_TOTAL
        L_ARMY_AVG_RS = L_ARMY_RS / L_UNITS_TOTAL
        L_ARMY_MS_FACTOR = factorC * L_ARMY_AVG_MS + factorD ** L_ARMY_AVG_MS
        L_ARMY_RS_FACTOR = factorC * L_ARMY_AVG_RS + factorD ** L_ARMY_AVG_RS
        calc['L','ARMY','PROPERTIES'] = [L_ARMY_MS, L_ARMY_MD, L_ARMY_RS, L_ARMY_RD, L_ARMY_MS_FACTOR, L_ARMY_RS_FACTOR]

    if D_UNITS_TOTAL > 0:
        #calculate updated D army totals
        D_ARMY_MS = (D_UNITS_GO * GO_PARAM[0] + D_UNITS_OA * OA_PARAM[0] + D_UNITS_OR * OR_PARAM[0]) * BATTLE_M_MULT
        D_ARMY_MD = (D_UNITS_GO * GO_PARAM[1] + D_UNITS_OA * OA_PARAM[1] + D_UNITS_OR * OR_PARAM[1])
        D_ARMY_RS = (D_UNITS_GO * GO_PARAM[2] + D_UNITS_OA * OA_PARAM[2] + D_UNITS_OR * OR_PARAM[2]) * BATTLE_R_MULT
        D_ARMY_RD = (D_UNITS_GO * GO_PARAM[3] + D_UNITS_OA * OA_PARAM[3] + D_UNITS_OR * OR_PARAM[3])
        D_ARMY_AVG_MS = D_ARMY_MS / D_UNITS_TOTAL
        D_ARMY_AVG_RS = D_ARMY_RS / D_UNITS_TOTAL
        D_ARMY_MS_FACTOR = factorC * D_ARMY_AVG_MS + factorD ** D_ARMY_AVG_MS
        D_ARMY_RS_FACTOR = factorC * D_ARMY_AVG_RS + factorD ** D_ARMY_AVG_RS
        calc['D','ARMY','PROPERTIES'] = [D_ARMY_MS, D_ARMY_MD, D_ARMY_RS, D_ARMY_RD, D_ARMY_MS_FACTOR, D_ARMY_RS_FACTOR]

    UNITS_TOTAL = [L_UNITS_TOTAL,D_UNITS_TOTAL]

    return UNITS_TOTAL


@export
def stake_CSTL(cstl_amount: int, IN_CSTL: float, AR_CSTL: float, HI_CSTL: float):

    assert IN_CSTL + AR_CSTL + HI_CSTL == cstl_amount, "Total number of CSTL must equal the sum of the CSTL used to train each unit."
    assert data['total_cstl'] + cstl_amount <= metadata['CSTL_FORT_PER_BATTLE'], f'You are attempting to stake {cstl_amount} which is more than the {metadata["CSTL_FORT_PER_BATTLE"] - data["total_cstl"]} remaining to be staked for this battle. Please try again with a smaller number.'
#put error checking to see if a battle has been started.
#copy this whole function but make it for FORT

    staked_wallets = data['cstl_staked_wallets']
    cstl = importlib.import_module(cstl_contract.get())

    UNITS_PER_CSTL = metadata['UNITS_PER_CSTL']

    IN_amount = UNITS_PER_CSTL["IN"] * IN_CSTL
    AR_amount = UNITS_PER_CSTL["AR"] * AR_CSTL
    HI_amount = UNITS_PER_CSTL["HI"] * HI_CSTL

    cstl.transfer_from(amount=cstl_amount, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: cstl_amount})
    else:
        staked_wallets[ctx.caller] += cstl_amount

    data['cstl_staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data['total_cstl'] += cstl_amount #adds total CSTL to storage for calculating rewards

    data['IN'] += IN_amount
    data['AR'] += AR_amount
    data['HI'] += HI_amount

@export
def stake_FORT(fort_amount: int, GO_FORT: float, OA_FORT: float, OR_FORT: float):

    assert GO_FORT + OA_FORT + OR_FORT == fort_amount, "Total number of FORT must equal the sum of the FORT used to train each unit."
    assert data['total_fort'] + fort_amount <= metadata['CSTL_FORT_PER_BATTLE'], f'You are attempting to stake {fort_amount} which is more than the {metadata["CSTL_FORT_PER_BATTLE"] - data["total_fort"]} remaining to be staked for this battle. Please try again with a smaller number.'
#put error checking to see if a battle has been started.
#copy this whole function but make it for FORT

    staked_wallets = data['fort_staked_wallets']
    fort = importlib.import_module(fort_contract.get())

    UNITS_PER_FORT = metadata['UNITS_PER_FORT']

    GO_amount = UNITS_PER_FORT["GO"] * GO_FORT
    OA_amount = UNITS_PER_FORT["OA"] * OA_FORT
    OR_amount = UNITS_PER_FORT["OR"] * OR_FORT

    fort.transfer_from(amount=fort_amount, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: fort_amount})
    else:
        staked_wallets[ctx.caller] += fort_amount

    data['fort_staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data['total_fort'] += fort_amount #adds total FORT to storage for calculating rewards

    data['GO'] += GO_amount
    data['OA'] += OA_amount
    data['OR'] += OR_amount

def disperse(operator: str, winner: str):
    #calculate winnings where winners get 1.09, loser gets 0.90 and house gets 0.01

    cstl = importlib.import_module(cstl_contract.get())
    fort = importlib.import_module(fort_contract.get())

    cstl_staked_wallets = data['cstl_staked_wallets']
    fort_staked_wallets = data['fort_staked_wallets']
    winner_percent = metadata['winner_percent']
    house_percent = metadata['house_percent']
    loser_percent = 1 - winner_percent - house_percent

    if winner == 'L':
        #send winnings to CASTLE stakers
        for key, value in dict(cstl_staked_wallets).items():
            cstl.transfer(amount=value, to=key)
            fort.transfer(amount= (value * winner_percent), to=key)
            fort.transfer(amount= (value * house_percent), to=operator) #make variable for OWNER

        for key, value in dict(fort_staked_wallets).items():
            fort.transfer(amount= (value * loser_percent), to=key)
    if winner == 'D':
        #send winnings to FORTRESS stakers
        for key, value in dict(fort_staked_wallets).items():
            fort.transfer(amount=value, to=key)
            cstl.transfer(amount= (value * winner_percent), to=key)
            cstl.transfer(amount= (value * house_percent), to=operator)

        for key, value in dict(cstl_staked_wallets).items():
            cstl.transfer(amount= (value * loser_percent), to=key)















#









#
