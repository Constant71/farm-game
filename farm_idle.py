# --- Simple Farm Sim (persistent plots + proper growth/harvest) ---

gold = 20

farm_inv = {
    "crops": {
        "pepper": 3,
        "carrot": 0,
        "pea": 0,
        "cucumber": 0,
        "eggplant": 0,
        "radish": 0,
        "onion": 0,
        "hops": 0,
        "potato": 0,
        "tomato": 0,
        "leek": 0,
        "watermelon": 0,
        "corn": 0,
        "cabbage": 0,
        "pine": 0,
        "pumpkin": 0
    }
}

# Active plots per crop type (how many are planted & growing)
crops = {
    "pepper": 0,
    "carrot": 0,
    "pea": 0,
    "cucumber": 0,
    "eggplant": 0,
    "radish": 0,
    "onion": 0,
    "hops": 0,
    "potato": 0,
    "tomato": 0,
    "leek": 0,
    "watermelon": 0,
    "corn": 0,
    "cabbage": 0,
    "pine": 0,
    "pumpkin": 0
}

VALID_CROPS = set(crops.keys())
MAX_PLOTS_PER_CROP = 5
MATURITY_STAGE = 5  # number of growth ticks to be harvestable

class Plot:
    def __init__(self, crop_type: str):
        self.crop_type = crop_type
        self.growth_stage = 0  # 0..MATURITY_STAGE
        self.ready = False

    def grow(self):
        if not self.ready:
            self.growth_stage += 1
            if self.growth_stage >= MATURITY_STAGE:
                self.growth_stage = MATURITY_STAGE
                self.ready = True

    def harvest(self):
        """Return True if harvested (i.e., was ready), False otherwise."""
        if self.ready:
            farm_inv["crops"][self.crop_type] += 1
            return True
        return False

# persistent list of all plots currently planted
active_plots = []

def plant_crop(crop_type: str):
    crop_type = crop_type.lower()
    if crop_type not in VALID_CROPS:
        print(f"'{crop_type}' is not a valid crop type.")
        return

    if crops[crop_type] >= MAX_PLOTS_PER_CROP:
        print(f"Cannot plant more {crop_type}. Max of {MAX_PLOTS_PER_CROP} plots reached.")
        return

    # Create and track the new plot
    active_plots.append(Plot(crop_type))
    crops[crop_type] += 1
    print(f"Planted {crop_type}. Active {crop_type} plots: {crops[crop_type]}")

def grow_all(days: int = 1):
    if days < 1:
        print("You must grow at least 1 day.")
        return
    for _ in range(days):
        for plot in active_plots:
            plot.grow()
    print(f"Time passed: {days} day(s). Crops progressed.")

def harvest_crop(crop_type: str):
    crop_type = crop_type.lower()
    if crop_type not in VALID_CROPS:
        print(f"'{crop_type}' is not a valid crop type.")
        return

    # Find the first ready plot of this crop
    for i, plot in enumerate(active_plots):
        if plot.crop_type == crop_type and plot.ready:
            if plot.harvest():
                # Remove the plot from active plots; reduce active count
                del active_plots[i]
                crops[crop_type] -= 1
                print(f"Harvested 1 {crop_type}. Inventory now: {farm_inv['crops'][crop_type]}")
                return
    print(f"No ready {crop_type} to harvest.")

def harvest_all_ready():
    """Harvest all plots that are ready, across all crop types."""
    harvested = 0
    # Iterate backwards so we can safely delete
    for i in range(len(active_plots) - 1, -1, -1):
        plot = active_plots[i]
        if plot.ready and plot.harvest():
            crops[plot.crop_type] -= 1
            del active_plots[i]
            harvested += 1
    if harvested:
        print(f"Harvested {harvested} crop(s) total.")
    else:
        print("No crops are ready to harvest.")

def display_inventory():
    print("\n=== Farm Inventory ===")
    for crop, count in farm_inv["crops"].items():
        print(f"{crop.capitalize():12}: {count}")
    print(f"Gold: {gold}")

def display_plots():
    print("\n=== Active Plots ===")
    if not active_plots:
        print("No plots planted.")
        return
    # Summarize per plot
    for idx, plot in enumerate(active_plots, start=1):
        status = "READY" if plot.ready else f"Stage {plot.growth_stage}/{MATURITY_STAGE}"
        print(f"{idx:2}. {plot.crop_type.capitalize():12} - {status}")
    # Also show counts per type
    print("\nActive plots per crop type:")
    for crop, count in crops.items():
        if count > 0:
            print(f"  {crop.capitalize():12}: {count}")

def main():
    while True:
        print("\nFarm Management System")
        print("1. Plant Crop")
        print("2. Wait a Day (Grow)")
        print("3. Harvest Crop")
        print("4. Harvest ALL Ready")
        print("5. Show Active Plots")
        print("6. Display Inventory")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            crop_type = input("Enter crop type to plant: ").strip().lower()
            plant_crop(crop_type)

        elif choice == '2':
            days_in = input("How many day(s) to wait? [default 1]: ").strip()
            days = 1 if days_in == "" else max(1, int(days_in))
            grow_all(days)

        elif choice == '3':
            crop_type = input("Enter crop type to harvest: ").strip().lower()
            harvest_crop(crop_type)

        elif choice == '4':
            harvest_all_ready()

        elif choice == '5':
            display_plots()

        elif choice == '6':
            display_inventory()

        elif choice == '7':
            print("Exiting the farm management system.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()