def calculate_total_debts(splits):
    total_debts = {}

    for e in splits:
        payer = e['payer']
        members = e['members']

        for member, debt in members.items():
            if member != payer:
                if payer not in total_debts:
                    total_debts[payer] = {}
                if member not in total_debts[payer]:
                    total_debts[payer][member] = 0
                
                if not debt['paid']:
                    total_debts[payer][member] += debt['amount']

    for debts in list(total_debts.values()):
        for creditor in list(debts.keys()):
            if debts[creditor] < 0:
                del debts[creditor]

    return total_debts