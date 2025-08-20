# --- Farm Sim with per-crop growth times, shop, seeds, and selling ---
# --- Farm Sim with limited plots and plot shop ---

gold = 20
total_plots = 5  # starting number of available plots
plot_purchase_count = 0  # number of extra plots bought
base_plot_cost = 10  # initial cost for buying an extra plot
plot_cost_increase = 5  # cost increase per purchased plot

# Crop data: seed cost, sell value, and growth time
crop_data = {
    "pepper":     {"seed_cost": 2, "sell_price": 5, "grow_time": 5},
    "carrot":     {"seed_cost": 1, "sell_price": 3, "grow_time": 3},
    "pea":        {"seed_cost": 2, "sell_price": 4, "grow_time": 4},
    "cucumber":   {"seed_cost": 3, "sell_price": 6, "grow_time": 5},
    "eggplant":   {"seed_cost": 3, "sell_price": 6, "grow_time": 6},
    "radish":     {"seed_cost": 1, "sell_price": 3, "grow_time": 3},
    "onion":      {"seed_cost": 2, "sell_price": 4, "grow_time": 4},
    "hops":       {"seed_cost": 3, "sell_price": 7, "grow_time": 6},
    "potato":     {"seed_cost": 2, "sell_price": 5, "grow_time": 5},
    "tomato":     {"seed_cost": 3, "sell_price": 6, "grow_time": 6},
    "leek":       {"seed_cost": 2, "sell_price": 4, "grow_time": 4},
    "watermelon": {"seed_cost": 5, "sell_price": 10, "grow_time": 8},
    "corn":       {"seed_cost": 4, "sell_price": 8, "grow_time": 7},
    "cabbage":    {"seed_cost": 3, "sell_price": 7, "grow_time": 5},
    "pine":       {"seed_cost": 6, "sell_price": 12, "grow_time": 10},
    "pumpkin":    {"seed_cost": 5, "sell_price": 11, "grow_time": 9},
}

# Inventory: starting seeds & harvested crops
farm_inv = {
    "seeds": {crop: 0 for crop in crop_data},
    "crops": {crop: 0 for crop in crop_data}
}
farm_inv["seeds"]["pepper"] = 3  # starting with 3 pepper seeds
farm_inv["seeds"]["pepper"] = 3  # starting seeds

VALID_CROPS = set(crop_data.keys())
MAX_PLOTS_PER_CROP = 5

class Plot:
    def __init__(self, crop_type: str):
        self.crop_type = crop_type
        self.growth_stage = 0
        self.ready = False
        self.required_growth = crop_data[crop_type]["grow_time"]

    def grow(self):
        if not self.ready:
            self.growth_stage += 1
            if self.growth_stage >= self.required_growth:
                self.growth_stage = self.required_growth
                self.ready = True

    def harvest(self):
        if self.ready:
            farm_inv["crops"][self.crop_type] += 1
            return True
        return False

# persistent plots
active_plots = []

def plant_crop(crop_type: str):
    global total_plots
    crop_type = crop_type.lower()
    if crop_type not in VALID_CROPS:
        print(f"'{crop_type}' is not valid.")
        return

    if len(active_plots) >= total_plots:
        print(f"All plots are occupied! You have {total_plots} plots.")
        return

    if farm_inv["seeds"][crop_type] <= 0:
        print(f"No {crop_type} seeds left. Buy some first.")
        return

    planted_count = sum(1 for p in active_plots if p.crop_type == crop_type)
    if planted_count >= MAX_PLOTS_PER_CROP:
        print(f"Cannot plant more {crop_type}. Max {MAX_PLOTS_PER_CROP} plots.")
        return

    farm_inv["seeds"][crop_type] -= 1
    active_plots.append(Plot(crop_type))
    print(f"Planted {crop_type}. Seeds left: {farm_inv['seeds'][crop_type]}")

def grow_all(days: int = 1):
    for _ in range(days):
        for plot in active_plots:
            plot.grow()
    print(f"Time passed: {days} day(s).")

def harvest_crop(crop_type: str):
    crop_type = crop_type.lower()
    for i, plot in enumerate(active_plots):
        if plot.crop_type == crop_type and plot.ready:
            plot.harvest()
            del active_plots[i]
            print(f"Harvested 1 {crop_type}. Stored: {farm_inv['crops'][crop_type]}")
            return
    print(f"No ready {crop_type} to harvest.")

def harvest_all_ready():
    harvested = 0
    for i in range(len(active_plots) - 1, -1, -1):
        if active_plots[i].ready:
            active_plots[i].harvest()
            del active_plots[i]
            harvested += 1
    print(f"Harvested {harvested} crops." if harvested else "No crops ready.")

def shop_menu():
    global gold, plot_purchase_count, base_plot_cost
    print("\n=== Farm Shop ===")
    print(f"Gold: {gold}")
    print("Seed Shop:")
    print(f"{'Crop':12} {'Seed Cost':10} {'Sell Price':10} {'Growth Time':12}")
    for crop, data in crop_data.items():
        print(f"{crop.capitalize():12} {data['seed_cost']:10} {data['sell_price']:10} {data['grow_time']:12}")
    next_plot_cost = base_plot_cost + plot_purchase_count * plot_cost_increase
    print(f"\nPlot Shop: Buy additional plot (current total plots: {total_plots}) for {next_plot_cost} gold.")

def buy_seeds(crop_type: str, qty: int):
    global gold
    crop_type = crop_type.lower()
    if crop_type not in VALID_CROPS:
        print(f"'{crop_type}' is not valid.")
        return
    cost = crop_data[crop_type]["seed_cost"] * qty
    if gold < cost:
        print(f"Not enough gold. Need {cost}, you have {gold}.")
        return
    gold -= cost
    farm_inv["seeds"][crop_type] += qty
    print(f"Bought {qty} {crop_type} seeds for {cost} gold. Gold left: {gold}")

def buy_plot():
    global gold, total_plots, plot_purchase_count
    cost = base_plot_cost + plot_purchase_count * plot_cost_increase
    if gold < cost:
        print(f"Not enough gold to buy a new plot. Cost: {cost}, you have: {gold}")
        return
    gold -= cost
    total_plots += 1
    plot_purchase_count += 1
    print(f"Bought a new plot! Total plots: {total_plots}. Gold left: {gold}")

def sell_crops(crop_type: str, qty: int):
    global gold
    crop_type = crop_type.lower()
    if crop_type not in VALID_CROPS:
        print(f"'{crop_type}' is not valid.")
        return
    if farm_inv["crops"][crop_type] < qty:
        print(f"Not enough {crop_type} to sell.")
        return
    revenue = crop_data[crop_type]["sell_price"] * qty
    farm_inv["crops"][crop_type] -= qty
    gold += revenue
    print(f"Sold {qty} {crop_type} for {revenue} gold. Gold now: {gold}")

def display_inventory():
    print("\n=== Inventory ===")
    print("-- Seeds --")
    for crop, count in farm_inv["seeds"].items():
        if count > 0:
            print(f"{crop.capitalize():12}: {count}")
    print("-- Crops --")
    for crop, count in farm_inv["crops"].items():
        if count > 0:
            print(f"{crop.capitalize():12}: {count}")
    print(f"Gold: {gold}")
    print(f"Available Plots: {total_plots} (Occupied: {len(active_plots)})")

def display_plots():
    print("\n=== Active Plots ===")
    if not active_plots:
        print("No plots planted.")
        return
    for idx, plot in enumerate(active_plots, start=1):
        status = "READY" if plot.ready else f"Stage {plot.growth_stage}/{plot.required_growth}"
        print(f"{idx:2}. {plot.crop_type.capitalize():12} - {status}")

def main():
    while True:
        print("\nFarm Management System")
        print("1. Plant Crop")
        print("2. Wait a Day")
        print("3. Harvest Crop")
        print("4. Harvest ALL")
        print("5. Show Plots")
        print("6. Display Inventory")
        print("7. Shop (Buy Seeds / Plots)")
        print("8. Sell Crops")
        print("9. Exit")

        choice = input("Choose: ").strip()

        if choice == '1':
            crop = input("Which crop to plant? ").strip().lower()
            plant_crop(crop)
        elif choice == '2':
            days = input("Days to wait [1]: ").strip()
            grow_all(int(days) if days else 1)
        elif choice == '3':
            crop = input("Which crop to harvest? ").strip().lower()
            harvest_crop(crop)
        elif choice == '4':
            harvest_all_ready()
        elif choice == '5':
            display_plots()
        elif choice == '6':
            display_inventory()
        elif choice == '7':
            shop_menu()
            shop_choice = input("Buy Seeds (S) or Plot (P)? ").strip().upper()
            if shop_choice == 'S':
                crop = input("Which crop seed to buy? ").strip().lower()
                qty = int(input("How many? "))
                buy_seeds(crop, qty)
            elif shop_choice == 'P':
                buy_plot()
        elif choice == '8':
            crop = input("Which crop to sell? ").strip().lower()
            qty = int(input("How many? "))
            sell_crops(crop, qty)
        elif choice == '9':
            print("Exiting farm sim.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
