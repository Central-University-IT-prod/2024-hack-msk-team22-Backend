token = request.headers.get('Authorization')

event = {
    "id": "asdasd",
    "creator": "3254345345",
    "splits": [
        {
            "name": place_name,
            "event" : categoryId,
            "icon" : image_url, #строка на картинку
            "payer": decode_token(token),
            "members": {
                "Вася": 300,
                "Максим": 300
            }
        },
        {
            "name": "египет",
            "payer": "Вася",
            "members": {
                "Миша": 200,
                "Максим": 400
            }
        },
    ]

}

debt_sum = {}
for i in event["splits"]:
    total_sum = sum(i["members"].values())
    debt_sum[i["currency"]] = debt_sum.setdefault(i["currency"], 0) + total_sum

print(debt_sum)




def calculate_total_debts(event):
    total_debts = {}

    for e in event['splits']:
        payer = e['payer']
        members = e['members']

        for member, amount in members.items():
            if member != payer:
                if member not in total_debts:
                    total_debts[member] = {}
                if payer not in total_debts[member]:
                    total_debts[member][payer] = 0
                total_debts[member][payer] += amount

            if payer != member:
                if payer not in total_debts:
                    total_debts[payer] = {}
                if member not in total_debts[payer]:
                    total_debts[payer][member] = 0
                total_debts[payer][member] -= amount

    # Удаляем долги, которые равны 0
    for debtor, debts in list(total_debts.items()):
        for creditor in list(debts.keys()):
            if debts[creditor] <= 0:
                del debts[creditor]

    return total_debts

def main():
    total_debts = calculate_total_debts(event)
    print("Словарь total_debts:")
    for debtor, debts in total_debts.items():
        print(f"{debtor}: {debts}")

if __name__ == "__main__":
    main()


print(event["splits"][0]["members"])
print(total_sum)