"""System profile management functionality."""

import os
from llama_index.core import Settings
from system_user_profile import collect_new_system_description


def get_system_summary(system_description: str) -> str:
    """Generate a human-readable summary of a system description."""
    prompt = (
        "You are a regulatory assistant helping with documentation and compliance. "
        "Based on the following structured system description, generate a clear, human-readable, flowing summary in natural language"
        "that highlights the system's purpose, users, data types, environment, AI usage, and criticality:\n\n"
        f"{system_description}."    
    )
    return Settings.llm.complete(prompt).text


def create_new_profile():
    """Create a new system profile interactively."""
    print("Add a new system to your profile ")
    profile = collect_new_system_description()

    print("Generating summary of the described system...")
    system_text = profile.format_for_prompt()
    summary = get_system_summary(system_text)
    Settings.llm.complete(summary)
    print(f"\nBased on your description, this is the system you want to add to your profile:\n{summary} ")

    confirm = input("\n Do you want to save this system to your profile? (yes/no) ")
    if confirm.lower().startswith("y"):
        profile.save_system_to_file("system_profile")
        profile.save_system_to_file(summary=summary)
        print("System profile saved successfully!")
    else:
        print("System profile was not saved.")


def get_saved_systems(folder: str = "system_profile") -> list[str]:
    """Get list of saved system files."""
    if not os.path.exists(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith(".txt")]


def select_system(folder: str = "system_profile") -> str:
    """Let user select a system from saved profiles. Returns the system summary content."""
    files = get_saved_systems(folder)

    if not files:
        print("No saved systems found")
        add_new = input(" Do you want to add a new system? (y/n) ")
        if add_new.startswith("y"):
            create_new_profile()
            # Try again after creating new profile
            files = get_saved_systems(folder)
            if not files:
                return None
        else:
            return None
    
    print("\nAvailable systems:")
    for i, file in enumerate(files, start=1):
        file_notxt = os.path.splitext(file)[0]
        print(f"{i}. {file_notxt}")
    
    try:
        choice = int(input("\nChoose a system using numbers: "))
        filename = files[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection...")
        return None
    
    try:
        with open(os.path.join(folder, filename), "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Could not read file {filename}")
        return None
