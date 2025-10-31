# main.py
# Main entry point for running the crew.

from src.crew import ResearchCrew
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables

def main():
    # --- Environment Checks ---
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: 'GOOGLE_API_KEY' environment variable is not set.")
        print("Please create a .env file in the project root with GOOGLE_API_KEY=your_api_key_here")
        return

    if not os.getenv("ENTREZ_EMAIL"):
        print("Warning: 'ENTREZ_EMAIL' environment variable is not set.")
        print("Using 'your.email@example.com' by default for PubMed. A real email is recommended.")
    
    # --- Dynamic User Inputs ---
    print("Starting the academic research system...")
    research_topic = input("Please, enter the research topic: ")
    
    print("\nEnter the key methodologies to search for (e.g., Deep Learning, U-Net, Transformers):")
    print("(One per line, press 'enter' on an empty line to finish)")
    
    methodologies = []
    while True:
        met = input().strip()
        if not met:
            break
        methodologies.append(met)
    
    # Use a default list if the user doesn't provide any
    if not methodologies:
        print("No methodologies entered. Using default list.")
        methodologies = ["Deep Learning", "CNNs", "U-Net", "Transformers"]

    print(f"\nStarting research on: '{research_topic}'")
    print(f"Searching for methodologies: {', '.join(methodologies)}")
    
    # --- Crew Execution ---
    crew = ResearchCrew(research_topic, methodologies)
    result = crew.run()
    
    print("\n################################################")
    print("## Research process completed ##")
    print("################################################\n")
    print(result)

if __name__ == "__main__":
    main()