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

class Plot:
    def __init__(self, crop_type):
        self.crop_type = crop_type
        self.growth_stage = 0
        self.harvested = False

    def grow(self):
        if not self.harvested:
            self.growth_stage += 1
            if self.growth_stage >= 5:  # Assuming 5 stages to fully grow
                self.harvested = True

    def harvest(self):
        if self.harvested:
            farm_inv["crops"][self.crop_type] += 1
            self.reset()

    def reset(self):
        self.growth_stage = 0
        self.harvested = False


def plant_crop(crop_type):
    if crop_type in crops and crops[crop_type] < 5:  # Assuming a max of 5 plots per crop type
        crops[crop_type] += 1
        farm_inv["crops"][crop_type] += 1
        print(f"Planted {crop_type}. Total now: {crops[crop_type]}")
    else:
        print(f"Cannot plant more {crop_type}. Max limit reached or invalid crop type.")

def harvest_crop(crop_type):
    if crop_type in crops and farm_inv["crops"][crop_type] > 0:
        plot = Plot(crop_type)
        plot.grow()  # Simulate growth
        if plot.harvested:
            plot.harvest()
            print(f"Harvested {crop_type}. Total now: {farm_inv['crops'][crop_type]}")
        else:
            print(f"{crop_type} is not ready for harvest yet.")
    else:
        print(f"No {crop_type} to harvest or invalid crop type.")


def display_inventory():
    print("Farm Inventory:")
    for crop, count in farm_inv["crops"].items():
        print(f"{crop.capitalize()}: {count}")
    print(f"Gold: {gold}")

def main():
    while True:
        print("\nFarm Management System")
        print("1. Plant Crop")
        print("2. Harvest Crop")
        print("3. Display Inventory")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            crop_type = input("Enter crop type to plant: ").lower()
            plant_crop(crop_type)
        elif choice == '2':
            crop_type = input("Enter crop type to harvest: ").lower()
            harvest_crop(crop_type)
        elif choice == '3':
            display_inventory()
        elif choice == '4':
            print("Exiting the farm management system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
