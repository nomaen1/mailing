import schedule, requests

def to_do():
    todo_dict = {
        '8:00' : 'Get Up',
        '8:30' : 'Breakfast',
        '9:00' : 'Go to Work',
        '12:00' : 'Lanch',
        '18:00' : 'Go home'
    }
    # print("Day's Tasks")
    # for time, do in todo_dict.items():
    #     print(time, do)
    print("Здраствуйтеб у вас сегодня урок в 20:00")
    response = requests.get('https://yobit.net/api/3/ticker/btc_usd').json()
    btc_price = response.get('btc_usd').get('last')
    print(f"{round(btc_price, 2)}$")

def main():
    # schedule.every(1).minutes.do(to_do)
    schedule.every().day.at('20:50').do(to_do)
    # to_do()
    while True:
        schedule.run_pending()
main()