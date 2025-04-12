import json

class Data():

    def load_data():
        with open("data.json", "r") as file:
            data = json.load(file)
            return data
    
    def save_data(data):
        with open("data.json", "w") as file:
            json.dump(data, file)

    def add_paid_followers(user_id, amount_do):
        data = Data.load_data()
        # Check if user id exists
        i = -1
        for c in data["paid"]:
            i += 1
            if c["id"] == user_id:
                data["paid"][i]["amount_do"] += amount_do
                Data.save_data(data)
                return
        # If not, add it
        data["paid"].append({"id": user_id, "amount_do": amount_do, "amount_done": 0})
        Data.save_data(data)

    def add_advertise_followers(user_id, amount_do=10, data=None, check_duplicate=True):
        save = False
        if data == None:
            save = True
            data = Data.load_data()
        # Check if user id exists
        if check_duplicate:
            for c in data["advertise"]:
                print("Checked: " + c["id"] + " | " + user_id)
                if c["id"] == user_id:
                    return
        # If not, add it
        data["advertise"].append({"id": user_id, "amount_do": amount_do, "amount_done": 0})
        if save:
            Data.save_data(data)
        else:
            print("Added the " + str(len(data["advertise"])) + "th advertise order")
        return data
    
    def add_refresh_token(token, expires_in, is_user, access_token=None):
        with open("refresh_tokens.json", "r") as file:
            data = json.load(file)
        if is_user:
            data["users"].append({"token": token, "expires_at": expires_in, "access_token": (access_token if access_token != None else "")})
        else:
            data["public"].append({"token": token, "expires_at": expires_in, "access_token": (access_token if access_token != None else "")})
        with open("refresh_tokens.json", "w") as file:
            json.dump(data, file)
    
    def get_refresh_token_data():
        with open("refresh_tokens.json", "r") as file:
            data = json.load(file)
        return data

def print_payment_plan():
    print("="*7 + " Payment Plan " + "="*7)
    print("1. 10 followers - 1.50$") # 0.15 per follower
    print("2. 20 followers - 2.50$") # 0.125 per follower
    print("3. 50 followers - 5.00$") # 0.1 per follower
    print("4. 100 followers - 8.00$") # 0.08 per follower
    print("5. 200 followers - 12.00$") # 0.06 per follower
    print("6. 500 followers - 20.00$") # 0.04 per follower
    print("7. 1000 followers - 30.00$") # 0.03 per follower
    print("8. 2000 followers - 50.00$") # 0.025 per follower
    print("9. 5000 followers - 100.00$") # 0.02 per follower
    print("10. 10000 followers - 150.00$") # 0.015 per follower
    print("="*30)


def on_exit():
    print(" ")
    print("Okay bye...")
    exit()

def main():
    while True:
        data = Data.load_data()
        print("")
        print("="*7 + " Follow Bot Overview " + "="*7)
        print("1. Add order")
        print("2. View orders")
        print("3. Add Advertisement")
        print("4. Bulk add advertisement")
        print("5. Stats")
        print("6. Payment Plan")
        print("7. Exit")
        print("="*35)
        choice = input("C:\\Users\\admin> follow_bot.exe --option=").replace(" ", "")
        print("")
        if choice == "1":
            user_id = input("Enter the user id: ")
            amount_do = int(input("Enter the amount to follow: "))
            Data.add_paid_followers(user_id, amount_do)
        elif choice == "2":
            print("Paid Orders (User ID | Amount to follow | Amount done)")
            for c in data["paid"]:
                print(f"User ID: {c['id']} | Amount to follow: {c['amount_do']} | Amount done: {c['amount_done']}")
            print("Total: " + str(len(data["paid"])))
        elif choice == "3":
            user_id = input("Enter the user id: ")
            amount_do = input("Enter the amount to follow: [Default: 10]")
            if len(amount_do) == 0:
                amount_do = 10
            else:
                amount_do = int(amount_do)
            data = Data.add_advertise_followers(user_id, amount_do=amount_do)
        elif choice == "4":
            ids = []
            inp = input("Enter the user ids separated by spaces: ").split(" ")
            for c in inp:
                if c in ids:
                    continue
                try:
                    just_a_test = int(c)
                except:
                    print("Continued: " + c + " is not a valid user id")
                    continue
                ids.append(c)
            amount_do = input("Enter the amount to follow: [Default: 10]")
            if len(amount_do) == 0:
                amount_do = 10
            else:
                amount_do = int(amount_do)
            for c in data["advertise"]:
                # Check if the ID is in the set of user IDs
                if c["id"] in ids:
                    print("Removed: " + str(c["id"]) + " from the list")
                    ids.remove(c["id"]) 
            for c in ids:
                data = Data.add_advertise_followers(c, amount_do=amount_do, data=data, check_duplicate=False)
            Data.save_data(data)
        elif choice == "5":
            print("="*11 + " Paid Stats " + "="*12)
            print(f'Total orders: {(len(data["paid"])):,}')
            # Completed = amount_done >= amount_do
            print(f'Total orders completed: {(len([c for c in data["paid"] if c["amount_done"] >= c["amount_do"]])):,}')
            print(f'Total orders remaining: {(len([c for c in data["paid"] if c["amount_done"] < c["amount_do"]])):,}')
            print(f'Follows done: {(sum([c["amount_done"] for c in data["paid"]])):,} / {(sum(c["amount_do"] for c in data["paid"])):,}')
            print("Average follows per order: " + str(sum([c["amount_do"] for c in data["paid"]]) / len(data["paid"])))
            print("="*36)
            print(" ")
            print("="*7 + " Advertisement Stats " + "="*7)
            print(f'Total orders: {(len(data["advertise"])):,}')
            print(f'Total orders completed: {(len([c for c in data["advertise"] if c["amount_done"] >= c["amount_do"]])):,}')
            print(f'Total orders remaining: {(len([c for c in data["advertise"] if c["amount_done"] < c["amount_do"]])):,}')
            print(f'Follows done: {(sum([c["amount_done"] for c in data["advertise"]])):,} / {(sum([c["amount_do"] for c in data["advertise"]])):,}')
            print("Average follows per order: " + str(sum([c["amount_do"] for c in data["advertise"]]) / len(data["advertise"])))
            print("="*36)
            print("")
        elif choice == "6":
            print_payment_plan()
        elif choice == "7":
            on_exit()
            break
        else:
            print("Invalid option")
            main()

if __name__ == "__main__":
    main()