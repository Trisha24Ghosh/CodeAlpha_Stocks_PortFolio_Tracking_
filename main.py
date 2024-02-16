import yfinance as yf


class StockPortfolioTracker:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, sign, aggregate):
        if sign in self.stocks:
            current_data = yf.Ticker(sign).history(period='1d')
            current_price = current_data['Close'].iloc[-1]
            total_cost = self.stocks[sign]['aggregate'] * self.stocks[sign]['average_price']
            total_cost += aggregate * current_price
            total_quantity = self.stocks[sign]['aggregate'] + aggregate
            self.stocks[sign]['average_price'] = total_cost / total_quantity
            self.stocks[sign]['aggregate'] = total_quantity
        else:
            current_data = yf.Ticker(sign).history(period='1d')
            current_price = current_data['Close'].iloc[-1]
            self.stocks[sign] = {'aggregate': aggregate, 'average_price': current_price}

    def remove_stock(self, sign, aggregate):
        if sign in self.stocks:
            if aggregate >= self.stocks[sign]['aggregate']:
                del self.stocks[sign]
            else:
                self.stocks[sign]['aggregate'] -= aggregate
        else:
            print(f"You don't own {sign} in your portfolio.")

    def update_portfolio(self):
        for sign in self.stocks:
            current_data = yf.Ticker(sign).history(period='1d')
            current_price = current_data['Close'].iloc[-1]
            self.stocks[sign]['average_price'] = current_price

    def display_portfolio(self):
        print("Stock Portfolio: ")
        for sign, data in self.stocks.items():
            print(f"{sign}: Quantity - {data['aggregate']}, Average Price - {data['average_price']:.2f} ")


def main():
    portfolio = StockPortfolioTracker()

    while True:
        print("\nMenu:")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Display Portfolio")
        print("4. Quit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            sign = input("Enter stock sign: ").upper()
            aggregate = int(input("Enter quantity: "))
            portfolio.add_stock(sign, aggregate)
        elif choice == '2':
            sign = input("Enter stock sign: ").upper()
            aggregate = int(input("Enter quantity to remove: "))
            portfolio.remove_stock(sign, aggregate)
        elif choice == '3':
            portfolio.update_portfolio()
            portfolio.display_portfolio()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
