metadata = Hash()
data = Hash(default_value=0)
sc_contract = Variable()
unit_contract = Variable()
terrain_contract = Variable()

random.seed()

@construct
def seed():
    metadata['operator'] = ctx.caller

    #prize calclulation Parameters
    metadata['winner_percent'] = decimal('0.09')
    metadata['house_percent'] = decimal('0.01')

    sc_contract.set('con_silver_credits')
    unit_contract.set('con_battlefield_units_001')
    terrain_contract.set('con_battlefield_terrains_001')

    #units per SC token
    metadata['UNITS_PER_SC']={
        "IN": 200,
        "AR": 91,
        "HI": 67,
        "CA": 48,
        "CP": 24,
        "GO": 333,
        "OA": 71,
        "OR": 100,
        "WO": 59,
        "TR": 20
    }

    data['L Wins'] = 0
    data['D Wins'] = 0

@export
def update_contract(update_var: str, new_contract: str):
    assert ctx.caller == metadata['operator'], "Only the operator update the contracts."
    update_var.set(new_contract)

@export
def change_metadata(key: str, new_value: str, convert_to_decimal: bool=False):
    assert ctx.caller == metadata['operator'], "Only the operator can set metadata."
    if convert_to_decimal:
        new_value = decimal(new_value)
    metadata[key] = new_value

@export
def battle(match_id: str):

    if data[match_id, 'private'] == 1:
        playerlist = data[match_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match and cannot start the battle. Contact the match creator if you wish to join.'

    total_L = data[match_id,'total_L']
    total_D = data[match_id,'total_D']
    assert total_L == total_D and total_L == data[match_id, 'battle_size'], f'There are {total_L} SC and {total_D} SC staked. These must be equal and filled to max capacity for a battle to be initiated.'
    operator = metadata['operator']
    calc = ForeignHash(foreign_contract=unit_contract.get(), foreign_name='param_calc')
    terraindata = ForeignHash(foreign_contract=terrain_contract.get(), foreign_name='metadata')

    terrains = terraindata['terrains']
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
    terrain_ = importlib.import_module(terrain_contract.get())
    battle_mult = terrain_.battle_mult_update(terrain_type=terrain_type, battle_turn=battle_turn)

    UNITS_TOTAL = calc_army_update(factorC, factorD, battle_mult[0], battle_mult[1], IN_PARAM, AR_PARAM, HI_PARAM, CA_PARAM, CP_PARAM, GO_PARAM, OA_PARAM, OR_PARAM, WO_PARAM, TR_PARAM) #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED

    while UNITS_TOTAL[0] > 0 and UNITS_TOTAL[1] > 0:

        battle_mult = terrain_.battle_mult_update(terrain_type=terrain_type, battle_turn=battle_turn)
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
        winner = 'L'
        data['L Wins'] += 1
    elif UNITS_TOTAL[1] > 0 and UNITS_TOTAL[0] <= 0:
        winner = 'D'
        data['D Wins'] += 1
    else:
        winner = 'error'

    data['Battle_Results'] = f'There are {int(IN_PARAM[6])} infantry, {int(AR_PARAM[6])} archers, {int(HI_PARAM[6])} heavy infantry, {int(CA_PARAM[6])} cavalry, {int(CP_PARAM[6])} catapults remaining in the LIGHT army, and there are {int(GO_PARAM[6])} goblins, {int(OA_PARAM[6])} orc archers, {int(OR_PARAM[6])} orcs, {int(WO_PARAM[6])} wolves, {int(TR_PARAM[6])} trolls remaining in the DARK army.'

    disperse(operator, winner, match_id)

    data['total_turns'] = battle_turn #may not need long term. This is just to track the total turns a battle took.

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

    SC = importlib.import_module(sc_contract.get())
    L_staked_wallets = data[match_id, 'L_staked_wallets']
    D_staked_wallets = data[match_id, 'D_staked_wallets']
    winner_percent = metadata['winner_percent']
    house_percent = metadata['house_percent']
    loser_percent = 1 - winner_percent - house_percent

    if winner == 'L':
        #send winnings to L army stakers
        for key, value in dict(L_staked_wallets).items():
            SC.transfer(amount=value * (1 + winner_percent) , to=key)
            SC.transfer(amount= (value * house_percent), to=operator) #make variable for OWNER

        for key, value in dict(D_staked_wallets).items():
            SC.transfer(amount= (value * loser_percent), to=key)
    if winner == 'D':
        #send winnings to D army stakers stakers
        for key, value in dict(D_staked_wallets).items():
            SC.transfer(amount=value * (1 + winner_percent), to=key)
            SC.transfer(amount= (value * house_percent), to=operator)

        for key, value in dict(L_staked_wallets).items():
            SC.transfer(amount= (value * loser_percent), to=key)

    data[match_id, 'L_staked_wallets'] = {} #clears all staked wallets from storage so a new battle can start
    data[match_id, 'D_staked_wallets'] = {}
    data[match_id, 'total_L'] = 0
    data[match_id, 'total_D'] = 0
    data[match_id, 'players'] = []
    data[match_id, 'match_owner'] = None
    data[match_id, 'terrain'] = None

    data[match_id, 'L_units'] = {}
    data[match_id, 'D_units'] = {}

@export
def stake_L(match_id: str, IN_L: int=0, AR_L: int=0, HI_L: int=0, CA_L: int=0,  CP_L: int=0):

#check to see if match is private. If public, don't check the list. If private, check to see if the player is on player list.
    if data[match_id, 'private'] == 1:
        playerlist = data[match_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match. Contact the match creator if you wish to join.'
    sc_amount = IN_L + AR_L + HI_L + CA_L + CP_L
    assert sc_amount <= data[match_id, 'max_stake_per'], f"You can only stake up to {data[match_id, 'max_stake_per']} tokens per transaction. Stake less and try again."
    assert data[match_id, 'total_L'] + sc_amount <= data[match_id, 'battle_size'], f"You are attempting to stake {sc_amount} which is more than the {data[match_id, 'battle_size'] - data[match_id, 'total_L']} remaining to be staked for this battle. Please try again with a smaller number."

    staked_wallets = data[match_id, 'L_staked_wallets']
    SC = importlib.import_module(sc_contract.get())
    UNITS_PER_SC = metadata['UNITS_PER_SC']
    L_units = data[match_id, 'L_units']

    IN_amount = UNITS_PER_SC["IN"] * IN_L
    AR_amount = UNITS_PER_SC["AR"] * AR_L
    HI_amount = UNITS_PER_SC["HI"] * HI_L
    CA_amount = UNITS_PER_SC["CA"] * CA_L
    CP_amount = UNITS_PER_SC["CP"] * CP_L

    SC.transfer_from(amount=sc_amount, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: sc_amount})
    else:
        staked_wallets[ctx.caller] += sc_amount

    data[match_id, 'L_staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data[match_id, 'total_L'] += sc_amount #adds total SC to storage for calculating rewards

    L_units['IN'] += IN_amount
    L_units['AR'] += AR_amount
    L_units['HI'] += HI_amount
    L_units['CA'] += CA_amount
    L_units['CP'] += CP_amount

    data[match_id, 'L_units'] = L_units

@export
def stake_D(match_id: str, GO_D: int=0, OA_D: int=0, OR_D: int=0,  WO_D: int=0, TR_D: int=0):

#check to see if match is private. If public, don't check the list. If private, check to see if the player is on player list.
    if data[match_id, 'private'] == 1:
        playerlist = data[match_id, 'players']
        assert ctx.caller in playerlist, 'You are not on the list of players for this match. Contact the match creator if you wish to join.'
    sc_amount = GO_D + OA_D + OR_D + WO_D + TR_D
    assert sc_amount <= data[match_id, 'max_stake_per'], f"You can only stake up to {data[match_id, 'max_stake_per']} tokens per transaction. Stake less and try again."
    assert data[match_id, 'total_D'] + sc_amount <= data[match_id, 'battle_size'], f"You are attempting to stake {sc_amount} which is more than the {data[match_id, 'battle_size'] - data[match_id, 'total_D']} remaining to be staked for this battle. Please try again with a smaller number."

    staked_wallets = data[match_id, 'D_staked_wallets']
    SC = importlib.import_module(sc_contract.get())
    UNITS_PER_SC = metadata['UNITS_PER_SC']
    D_units = data[match_id, 'D_units']

    GO_amount = UNITS_PER_SC["GO"] * GO_D
    OA_amount = UNITS_PER_SC["OA"] * OA_D
    OR_amount = UNITS_PER_SC["OR"] * OR_D
    WO_amount = UNITS_PER_SC["WO"] * WO_D
    TR_amount = UNITS_PER_SC["TR"] * TR_D

    SC.transfer_from(amount=sc_amount, to=ctx.this, main_account=ctx.caller)

    if ctx.caller not in staked_wallets:
        staked_wallets.update({ctx.caller: sc_amount})
    else:
        staked_wallets[ctx.caller] += sc_amount

    data[match_id, 'D_staked_wallets'] = staked_wallets #adds the staker to the dict for calculating rewards for winners and losers
    data[match_id, 'total_D'] += sc_amount #adds total SC to storage for calculating rewards

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
    data[match_id, 'L_staked_wallets'] = {}
    data[match_id, 'D_staked_wallets'] = {}

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
    assert tokens > (data[match_id, 'total_L'] + data[match_id, 'total_D']), 'The match is over half full and can no longer be cancelled.'

    SC = importlib.import_module(sc_contract.get())

    L_staked_wallets = data[match_id, 'L_staked_wallets']
    D_staked_wallets = data[match_id, 'D_staked_wallets']

    for key, value in dict(L_staked_wallets).items():
        SC.transfer(amount=value, to=key)

    for key, value in dict(D_staked_wallets).items():
        SC.transfer(amount=value, to=key)

    data[match_id, 'L_staked_wallets'] = {} #clears all staked wallets from storage so a new battle can start
    data[match_id, 'D_staked_wallets'] = {}
    data[match_id, 'total_L'] = 0
    data[match_id, 'total_D'] = 0
    data[match_id, 'players'] = []
    data[match_id, 'match_owner'] = None
    data[match_id, 'terrain'] = None

    data[match_id, 'L_units'] = {}
    data[match_id, 'D_units'] = {}

#Add data to store winner for each match, and then add a reset function for only me to run, so I can check balance of factions long term and reset after I update a parameter.

@export
def reset_stats():
    assert ctx.caller == metadata['operator'], "Only the operator can reset statistics."
    data['L Wins'] = 0
    data['D Wins'] = 0

@export
def new_conquest(conquest_id : str, grid_size : int, battles_per_day: int, private : bool, battle_size : int = 500):

    caller = ctx.caller
    data[conquest_id, 'conquest_owner'] = caller
    data[conquest_id, 'private'] = private
    data[conquest_id, 'players'] = [caller]
    data[conquest_id, 'battle_size'] = battle_size

    terraindata = ForeignHash(foreign_contract=terrain_contract.get(), foreign_name='metadata')
    terrains = terraindata['terrains']

    grid = []

    g = 0
    while g < grid_size:
        grid.append(g)
        g += 1

    for x in grid:
        y = 0
        while y < grid_size:
            grid[x].append( zone = {
                'Owner' : caller,
                'Faction' : random.randint(0, 1), # 0 is L and 1 is D
                'Units' : {
                    "IN": 0,
                    "AR": 0,
                    "HI": 0,
                    "CA": 0,
                    "CP": 0,
                    "GO": 0,
                    "OA": 0,
                    "OR": 0,
                    "WO": 0,
                    "TR": 0
                },
                'Terrain' : terrains[random.randint(1, 5)],
            })
            data[conquest_id , 'map' , x , y ] = grid[x][y]
            y += 1
        x += 1

@export
def conquest_test(conquest_id: str, row : int, column : int):
    zone = data[conquest_id , 'map' , row , column ]
    data['array_test'] = zone['Faction']
    data['array_test2'] = zone['Terrain']

@export
def conquest_battle(conquest_id: str, row : int, column : int): #enter row and column of zone you want to attack
    zone = data[conquest_id , 'map' , row , column ]
    assert zone['Owner'] != ctx.caller, 'You own this territory and cannot attack it.'

    zoneup    = data[conquest_id , 'map' , row , column - 1]
    zonedown  = data[conquest_id , 'map' , row , column + 1]
    zoneleft  = data[conquest_id , 'map' , row , column - 1]
    zoneright = data[conquest_id , 'map' , row , column + 1]
    assert zoneup['Owner'] or zonedown['Owner'] or zoneleft['Owner'] or zoneright['Owner'] == ctx.caller, 'You cannot attack this territory since you do not own an adjacent territory.'

    #add check to make sure the zone you're attacking is attackable

@export
def emergency_return(match_id : str):
    assert ctx.caller == metadata['operator'], "Only the operator can initiate an emergency return of tokens."

    SC = importlib.import_module(sc_contract.get())
    L_staked_wallets = data[match_id, 'L_staked_wallets']
    D_staked_wallets = data[match_id, 'D_staked_wallets']

    for key, value in dict(L_staked_wallets).items():
        SC.transfer(amount=value, to=key)

    for key, value in dict(D_staked_wallets).items():
        SC.transfer(amount=value, to=key)

    data[match_id, 'L_staked_wallets'] = {} #clears all staked wallets from storage so a new battle can start
    data[match_id, 'D_staked_wallets'] = {}
    data[match_id, 'total_L'] = 0
    data[match_id, 'total_D'] = 0
    data[match_id, 'players'] = []
    data[match_id, 'match_owner'] = None
    data[match_id, 'terrain'] = None

    data[match_id, 'L_units'] = {}
    data[match_id, 'D_units'] = {}



