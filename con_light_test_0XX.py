metadata = Hash()
calc = Hash()
data = Hash(default_value=0)

cstl_contract = Variable()

random.seed()

@construct
def seed():
    metadata['operator'] = ctx.caller

    cstl_contract.set('con_castle')


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

@export
def change_metadata(key: str, new_value: str, convert_to_decimal: bool=False):
    assert ctx.caller == metadata['operator'], "only operator can set metadata"
    if convert_to_decimal:
        new_value = decimal(new_value)
    metadata[key] = new_value

@export
def update_units_factors():

    #LIGHT Unit Parameter factors
    IN_MDF = metadata['factorA'] * metadata['IN_MD'] + (metadata['factorB'] * metadata['IN_MD']) ** 3
    IN_RDF = metadata['factorA'] * metadata['IN_RD'] + (metadata['factorB'] * metadata['IN_RD']) ** 3
    #IN_WEAKNESS_1 =
    AR_MDF = metadata['factorA'] * metadata['AR_MD'] + (metadata['factorB'] * metadata['AR_MD']) ** 3
    AR_RDF = metadata['factorA'] * metadata['AR_RD'] + (metadata['factorB'] * metadata['AR_RD']) ** 3

    HI_MDF = metadata['factorA'] * metadata['HI_MD'] + (metadata['factorB'] * metadata['HI_MD']) ** 3
    HI_RDF = metadata['factorA'] * metadata['HI_RD'] + (metadata['factorB'] * metadata['HI_RD']) ** 3


    calc['IN','PARAM'] = [metadata['IN_MS'], metadata['IN_MD'], metadata['IN_RS'], metadata['IN_RD'], IN_MDF, IN_RDF, 0.0] #ADD STRENGTHS ANDWEAKNESSES TO UNIT PARAMS
    calc['AR','PARAM'] = [metadata['AR_MS'], metadata['AR_MD'], metadata['AR_RS'], metadata['AR_RD'], AR_MDF, AR_RDF, 0.0] #ADD STRENGTHS ANDWEAKNESSES TO UNIT PARAMS
    calc['HI','PARAM'] = [metadata['HI_MS'], metadata['HI_MD'], metadata['HI_RS'], metadata['HI_RD'], HI_MDF, HI_RDF, 0.0] #ADD STRENGTHS ANDWEAKNESSES TO UNIT PARAMS

    #DARK Unit Parameter factors
    GO_MDF = metadata['factorA'] * metadata['GO_MD'] + (metadata['factorB'] * metadata['GO_MD']) ** 3
    GO_RDF = metadata['factorA'] * metadata['GO_RD'] + (metadata['factorB'] * metadata['GO_RD']) ** 3

    OA_MDF = metadata['factorA'] * metadata['OA_MD'] + (metadata['factorB'] * metadata['OA_MD']) ** 3
    OA_RDF = metadata['factorA'] * metadata['OA_RD'] + (metadata['factorB'] * metadata['OA_RD']) ** 3

    OR_MDF = metadata['factorA'] * metadata['OR_MD'] + (metadata['factorB'] * metadata['OR_MD']) ** 3
    OR_RDF = metadata['factorA'] * metadata['OR_RD'] + (metadata['factorB'] * metadata['OR_RD']) ** 3

    calc['GO','PARAM'] = [metadata['GO_MS'], metadata['GO_MD'], metadata['GO_RS'], metadata['GO_RD'], GO_MDF, GO_RDF, 0.0]
    calc['OA','PARAM'] = [metadata['OA_MS'], metadata['OA_MD'], metadata['OA_RS'], metadata['OA_RD'], OA_MDF, OA_RDF, 0.0]
    calc['OR','PARAM'] = [metadata['OR_MS'], metadata['OR_MD'], metadata['OR_RS'], metadata['OR_RD'], OR_MDF, OR_RDF, 0.0]

    #update calc list from metadata parameters. This will be called instead of each individual metadata tag to reduce stamp usage.
    calc['factor_list'] = [metadata['factorC'], metadata['factorD'], metadata['factorE'], metadata['lower'], metadata['upper'], metadata['multiplier'], metadata['STR_bonus']]

@export
def battle():

    factor_list = calc['factor_list']
    factorC = factor_list[0]
    factorD = factor_list[1]
    factorE = factor_list[2]
    lower = factor_list[3]
    upper = factor_list[4]
    multiplier = factor_list[5]
    STR_bonus = factor_list[6]

    IN_PARAM = calc['IN','PARAM']
    #IN_MS = IN_PARAM[0]
    #IN_MD = IN_PARAM[1]
    #IN_RS = IN_PARAM[2]
    #IN_RD = IN_PARAM[3]
    #IN_MDF = IN_PARAM[4]
    #IN_RDF = IN_PARAM[5]
    #IN_count = IN_PARAM[6]
    AR_PARAM = calc['AR','PARAM']
    HI_PARAM = calc['HI','PARAM']

    GO_PARAM = calc['GO','PARAM']
    OA_PARAM = calc['OA','PARAM']
    OR_PARAM = calc['OR','PARAM']

    BATTLE_M_MULT = 1
    BATTLE_R_MULT = 1

    #battle setup
    IN_PARAM[6] = metadata['TEMP_IN'] #add all other units here as they're added
    AR_PARAM[6] = metadata['TEMP_AR']
    HI_PARAM[6] = metadata['TEMP_HI']

    GO_PARAM[6] = metadata['TEMP_GO']
    OA_PARAM[6] = metadata['TEMP_OA']
    OR_PARAM[6] = metadata['TEMP_OR']

    #MULTIPLIER to change range vs melee strength through the battle. For now it's set to 1 for the whole battle

    UNITS_TOTAL = calc_army_update(factorC, factorD, BATTLE_M_MULT, BATTLE_R_MULT, IN_PARAM, AR_PARAM, HI_PARAM, GO_PARAM, OA_PARAM, OR_PARAM) #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED

    while UNITS_TOTAL[0] > 0 and UNITS_TOTAL[1] > 0:
        IN_PARAM[6] = calc_losses(IN_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'L', 'D', 'IN', BATTLE_M_MULT, BATTLE_R_MULT) # 3 STRING paremeters are faction of unit, opposing faction, unit name
        AR_PARAM[6] = calc_losses(AR_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'L', 'D', 'AR', BATTLE_M_MULT, BATTLE_R_MULT) # 3 STRING paremeters are faction of unit, opposing faction, unit name
        HI_PARAM[6] = calc_losses(HI_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'L', 'D', 'HI', BATTLE_M_MULT, BATTLE_R_MULT) # 3 STRING paremeters are faction of unit, opposing faction, unit name

        GO_PARAM[6] = calc_losses(GO_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'D', 'L', 'GO', BATTLE_M_MULT, BATTLE_R_MULT)
        OA_PARAM[6] = calc_losses(OA_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'D', 'L', 'OA', BATTLE_M_MULT, BATTLE_R_MULT)
        OR_PARAM[6] = calc_losses(OR_PARAM, factorE, multiplier, lower, upper, STR_bonus, 'D', 'L', 'OR', BATTLE_M_MULT, BATTLE_R_MULT)

        UNITS_TOTAL = calc_army_update(factorC, factorD, BATTLE_M_MULT, BATTLE_R_MULT, IN_PARAM, AR_PARAM, HI_PARAM, GO_PARAM, OA_PARAM, OR_PARAM) #ADD ALL OTHER PARAM LISTS HERE AS UNITS ARE ADDED

    calc['Battle_Results'] = f'There are {int(IN_PARAM[6])} infantry, {int(AR_PARAM[6])} archers, and {int(HI_PARAM[6])} heavy infantry remaining in the LIGHT army, and there are {int(GO_PARAM[6])} goblins, {int(OA_PARAM[6])} orc archers, and {int(OR_PARAM[6])} orcs remaining in the DARK army.'

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

#put error checking total number of castles already in contract vs total possible for the battle.
#put error about more castle types than total castles.
#put error checking to see if a battle has been started.
#

    cstl = importlib.import_module(cstl_contract.get())

    UNITS_PER_CSTL = metadata['UNITS_PER_CSTL']

    IN_amount = UNITS_PER_CSTL["IN"] * IN_CSTL
    AR_amount = UNITS_PER_CSTL["AR"] * AR_CSTL
    HI_amount = UNITS_PER_CSTL["HI"] * HI_CSTL

    cstl.transfer_from(amount=cstl_amount, to=ctx.this, main_account=ctx.caller)
    data[ctx.caller] += cstl_amount

    data['IN'] += IN_amount
    data['AR'] += AR_amount
    data['HI'] += HI_amount






















#
