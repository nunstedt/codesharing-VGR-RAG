import json
import os

class SystemProfile:
    def __init__(self, system_name = "", functionality = "", users = "", data="",
                environment="", ai_system: bool=False, ai_components = "", accessability = "", criticality = ""):
        self.system_name = system_name
        self.functionality = functionality
        self.users = users
        self.data = data
        self.environment = environment
        self.ai_system = ai_system
        self.ai_components = ai_components
        self.accessability = accessability
        self.criticality = criticality

    
    def format_for_prompt(self) -> str:
        return(
            f"System name: {self.system_name}\n"
            f"System functionality: {self.functionality}\n"
            f"System users: {self.users}\n"
            f"Data types: {self.data}\n"
            f"Host environment: {self.environment}\n"
            f"AI system: {self.ai_system}\n"
            f"AI components: {self.ai_components}\n"
            f"Accessability: {self.accessability}\n"
            f"Criticality: {self.criticality}\n"
        )

    def make_dictionary(self) -> dict:
        return self.__dict__
    
    def save_system_to_file(self, summary:str = None, folder: str = "system_profile"):

        os.makedirs(folder, exist_ok=True)

        safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in self.system_name)
        filename = os.path.join(folder, f"{safe_name}.json")

        with open(filename, "w") as f:
            json.dump(self.make_dictionary(), f, indent=2)
            print(f"System description saved")
        
        if summary:
            summary_filename = os.path.join(folder, f"{safe_name}.txt")
            with open(summary_filename, "w") as f:
                f.write(summary)
            print(f"Summary saved")

    @classmethod
    def load_system_from_file(cls, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f) 
        return cls(**data)


def collect_new_system_description() -> SystemProfile:
    print("\n Describe your system by answering the following questions...")
    
    # 1. Name the system
    system_name = input("1. What is the name of the system? ")

    # 2. Describe the system
    functionality = input("2. Describe what the system in used for: ")

    # 3. Define the users
    user_options = {
        "1": "Internal staff at VGR",
        "2": "Specialists",
        "3": "Citizens",
        "4": "External contractors",
        "5": "Internal staff at VGR",
        "6": "Non-specified",

    }

    print("\n2. Who are the primary users of the system? (You can choose multiple, separate by comma) ")
    for k, v in user_options.items():
        print(f"  {k}. {v}")
    selected_users = input("Choose 1–6: ").split(",")
    users = [user_options.get(key.strip(), "Non-specified") for key in selected_users]

    # 4. Choose data type
    data_options ={
        "1": "Personal data",
        "2": "Health data",
        "3": "Non-sensitive data",
        "4": "Security classified data",
        "5": "Mixed"
    }

    print("\n2. What data does the system handle? (You can choose multiple, separate by comma) ")
    for k, v in data_options.items():
        print(f"  {k}. {v}")
    selected_data = input("Choose 1–5: ").split(",")
    data = [data_options.get(key.strip(), "Non-sensitive data") for key in selected_data]

    # 5. Where is the system hosted
    env_options ={
        "1": "On-premisse",
        "2": "Cloud (public)",
        "3": "Cloud (private)",
        "4": "Hybrid",
        "5": "Unknown"
    }    

    print("\n2. What is the hosting environment of the system? (You can choose multiple, separate by comma) ")
    for k, v in env_options.items():
        print(f"  {k}. {v}")
    selected_environment = input("Choose 1–5: ").split(",")
    environment = [env_options.get(key.strip(), "Unknown") for key in selected_environment]

    ai_input = input("\n6. Is this an AI system (yes/no)?").strip().lower()
    ai_system = ai_input in ["yes", "y", "true", "1"]

    ai_components = ""
    if ai_system:
            ai_components = input("What AI components or models are included?")
    
        # 8. Accessibility
    access_options = {
        "1": "Internal network only",
        "2": "Public internet",
        "3": "VPN access",
        "4": "Mobile device accessible",
        "5": "Other"
    }
    print("\n7. How is the system accessed? (You can choose multiple, separate by comma) ")
    for k, v in access_options.items():
        print(f"  {k}. {v}")
    selected_accessability = input("Choose 1–5: ").split(",")
    accessability = [access_options.get(key.strip(), "Other") for key in selected_accessability]

    # 9. Criticality
    criticality_options = {
        "1": "Low – loss would have minor impact",
        "2": "Medium – operational impact",
        "3": "High – safety/life-critical or vital to operations"
    }
    print("\n8. How would you rate the system's criticality?")
    for k, v in criticality_options.items():
        print(f"  {k}. {v}")
    criticality = criticality_options.get(input("Choose 1–3: "), "Low – loss would have minor impact")

    profile = SystemProfile(
        system_name=system_name,
        functionality=functionality,
        users=users,
        data=data,
        environment=environment,
        ai_system=ai_system,
        ai_components=ai_components,
        accessability=accessability,
        criticality=criticality
    )
    return profile 


