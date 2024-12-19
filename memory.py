class Memory:

    def __init__(self, size=256):
        self.memory = {}
        self.size = size
        self.init_memory()


    def init_memory(self):
        for i in range(self.size):
            self.memory[format(i, "08b")] = None

    def load_data(self, data_path):
        try:
            with open(data_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    address, data = line.split(",", 1)
                    self.memory[address] = data
        except FileNotFoundError:
            print(f"Error: File not found at {data_path}")
        except Exception as error:
            print(f"An error occurred: {error}.")
        print("Data loaded successfully.")

    def fetch_data(self, address):
        return self.memory.get(address, f"No data found for address {address}.")
    
    def list_addresses(self):
        return list(self.memory.keys())
    
    def update_address(self, address, new_data):
        if address in self.memory:
            self.memory[address] = new_data
            print(f"Updated data at address {address}.")
        else:
            print(f"Address {address} not found.")

    def delete_data(self, address):
        if address in self.memory:
            del self.memory[address]
            print(f"Data from address {address} deleted.")
        else:
            print(f"Address {address} not found.")

    def clear_memory(self):
        self.init_memory()
        print("All memory cleared.")