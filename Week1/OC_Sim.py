"""
This is the code to run the first simulation of the course! It illustrates the opportunity cost that
people in real life have to face when choosing a job candidate.

author: Justin Baratta
date: 5/29/2026
version: Python 3.13
"""

import random
import time

NUM_QUALITIES = 3

QUALITIES = [
    "technical skills", "communication skills", "leadership", 
    "creativity", "problem solving", "adaptability", "teamwork", 
    "time management", "critical thinking", "emotional intelligence"
]

DESIRED_QUALITIES = random.sample(QUALITIES, NUM_QUALITIES)

def welcome() -> None:
    welcome_message = f"""
Welcome to your week 1 simulation, brought to you by me, Justin!
This simulation will help you understand the opportunity costs associated with job selection that managers face in real life.
In this simulation, you are a manager at a company looking to hire a new employee. You have identified the following qualities as most important for the job:
{', '.join(DESIRED_QUALITIES)}\n
"""
    for char in welcome_message:
        print(char, end='', flush=True)
        time.sleep(0.03)

def rules() -> None:
    rules = """
You must choose one candidate from a list of 25 candidates, each with a unique score from 1 to 100 in each category.
You will have to hire one of these candidates that you think is the best fit for the job, based on their score in your desired qualities, as well as their overall score in each of the categories. (highest scores)

You have a total of 5 time blocks. Each candidate will be presented to you one at a time, along with their *average* score in the 10 qualities and their score in ONE of the three desired qualities.\nFor each candidate, you may choose to interview them, showing you their scores in your desired qualities and costing one time block.
For each candidate, you can choose to hire or pass on them. If you pass on a candidate, they will have an increasing chance each turn to be hired by another company, and thus will no longer be available to you.
If you hire them, the simulation will end and you will receive a score from 1 to 100 on how good the candidate *you* hired is in comparison to the other candidates.\nHave fun and CONSIDER THE OPPORTUNITY COSTS!\nHINT: though the average of the qualities is important (40% of the score), the most important factor is how well they do in your desired qualities (60% of the score). So keep that in mind when making your decisions!
"""
    for char in rules:
        print(char, end='', flush=True)
        time.sleep(0.03)

def generate_candidates() -> list[dict[str, int]]:
    candidates = []
    for i in range(25):
        candidate = {quality: random.randint(1, 100) for quality in QUALITIES}
        candidates.append(candidate)
    return candidates

def score_candidate(candidate: dict[str, int]) -> float:
    desired_score = sum(candidate[quality] for quality in DESIRED_QUALITIES) / NUM_QUALITIES
    background_qualities = [q for q in QUALITIES if q not in DESIRED_QUALITIES]
    background_score = sum(candidate[quality] for quality in background_qualities) / len(background_qualities)
    return (0.6 * desired_score) + (0.4 * background_score)

def calculate_performance_score(chosen: dict[str, int], all_candidates: list[dict[str, int]]) -> float:
    best_score = max(score_candidate(c) for c in all_candidates)
    user_score = score_candidate(chosen)
    return (user_score / best_score) * 100

candidates = generate_candidates()

if __name__ == "__main__":
    intro = input("Welcome to the Opportunity Cost Simulation! Do you want to see the welcome message and rules? (yes/no): ").strip().lower()
    match intro:
        case "yes":
            welcome()
            rules()
        case "no":
            print("Alright, let's get started!")
        case _:
            print("Invalid input, let's get started!")

    time_blocks = 5
    passed_candidates = {}
    interviewed_candidates = set()
    hired_candidate = None
    i = 0

    while i < len(candidates):
        print(f"\nYou have {time_blocks} time blocks remaining.")
        
        overall_avg = sum(candidates[i].values()) / len(QUALITIES)
        print(f"Candidate {i + 1}: General Average Score: {overall_avg:.2f}")

        if i in interviewed_candidates:
            print("Interview Results (All Target Qualities Revealed):")
            for quality in DESIRED_QUALITIES:
                print(f" - {quality}: {candidates[i][quality]}/100")
        else:
            revealed_quality = random.choice(DESIRED_QUALITIES)
            print(f"Resume Snippet -> {revealed_quality}: {candidates[i][revealed_quality]}/100")

        if time_blocks == 0 and i not in interviewed_candidates:
            print("\n[ALERT] You ran out of time blocks! You are forced to hire this candidate.")
            hired_candidate = candidates[i]
            break

        taken_candidates = []
        for passed_index, percentage in list(passed_candidates.items()):
            if random.randint(1, 100) <= percentage:
                print(f"-> NOTICE: Candidate {passed_index + 1} has just been hired by a competitor!")
                taken_candidates.append(passed_index)
            else:
                passed_candidates[passed_index] += 5
        
        for index in taken_candidates:
            del passed_candidates[index]

        print("\nWhat would you like to do?")
        if i not in interviewed_candidates and time_blocks > 0:
            print("[I] Interview this candidate (Reveals desired qualities. Costs 1 time block)")
        print("[H] Hire a candidate (Current or previously passed)")
        print("[P] Pass on this candidate")
        print("[S] See all currently available candidates")

        action = input("Selection: ").strip().upper()

        if action == "S":
            print("\n--- Listing All Currently Available Candidates ---")
            if i in interviewed_candidates:
                print(f"Current Candidate {i + 1}: General Average Score: {overall_avg:.2f} (Fully Interviewed)")
                for quality in DESIRED_QUALITIES:
                    print(f"   - {quality}: {candidates[i][quality]}/100")
            else:
                print(f"Current Candidate {i + 1}: General Average Score: {overall_avg:.2f} (Snippet -> {revealed_quality}: {candidates[i][revealed_quality]}/100)")
            time.sleep(1)
            
            if passed_candidates:
                print("Previously Passed Candidates:")
                for index in passed_candidates:
                    past_avg = sum(candidates[index].values()) / len(QUALITIES)
                    if index in interviewed_candidates:
                        print(f" - Candidate {index + 1}: General Average Score: {past_avg:.2f} (Fully Interviewed)")
                        for quality in DESIRED_QUALITIES:
                            print(f"     - {quality}: {candidates[index][quality]}/100")
                    else:
                        print(f" - Candidate {index + 1}: General Average Score: {past_avg:.2f}")
                    time.sleep(1)
            else:
                print("No previously passed candidates are currently available.")
            continue

        if action == "I" and i not in interviewed_candidates and time_blocks > 0:
            time_blocks -= 1
            interviewed_candidates.add(i)
            print(f"\n--- Interviewing Candidate {i + 1} ---")
            for quality in DESIRED_QUALITIES:
                print(f" - {quality}: {candidates[i][quality]}/100")
            
            hire_now = input("\nDo you want to hire them after this interview? (yes/no): ").strip().lower()
            if hire_now == "yes":
                hired_candidate = candidates[i]
                break

        elif action == "H":
            print(f"\nAvailable options to hire:")
            print(f" - Candidate {i + 1} (Current)")
            for passed_index in passed_candidates:
                print(f" - Candidate {passed_index + 1} (Passed)")
                
            try:
                choice = int(input("\nEnter the candidate number you wish to hire: ")) - 1
                if choice == i:
                    hired_candidate = candidates[i]
                    break
                elif choice in passed_candidates:
                    hired_candidate = candidates[choice]
                    break
                else:
                    print("That candidate is not available for hire.")
            except ValueError:
                print("Invalid input. Returning to menu.")

        elif action == "P":
            passed_candidates[i] = 20
            print(f"Passed on Candidate {i + 1}.")
            i += 1

        else:
            print("Invalid input choice. Please select a valid option.")

    if not hired_candidate and i >= len(candidates):
        print("\nYou have reviewed all 25 candidates and passed on everyone!")
        if passed_candidates:
            print("You are forced to choose from your remaining available talent pool.")
            while True:
                print("\nAvailable past candidates:")
                for index in passed_candidates:
                    if index in interviewed_candidates:
                        print(f" - Candidate {index + 1} (Fully Interviewed)")
                    else:
                        print(f" - Candidate {index + 1}")
                try:
                    review_choice = int(input("Enter candidate number to hire: ")) - 1
                    if review_choice in passed_candidates:
                        hired_candidate = candidates[review_choice]
                        break
                    else:
                        print("That candidate is no longer available. Choose another.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        else:
            print("Every candidate you passed on was snatched up by competitors! You are forced to hire a random temp worker.")
            hired_candidate = {"technical skills": 1, "communication skills": 1, "leadership": 1, "creativity": 1, "problem solving": 1, "adaptability": 1, "teamwork": 1, "time management": 1, "critical thinking": 1, "emotional intelligence": 1}

    if hired_candidate:
        final_score = calculate_performance_score(hired_candidate, candidates)
        best_candidate = max(candidates, key=score_candidate)
        best_candidate_index = candidates.index(best_candidate) + 1
        
        print("\n" + "="*50)
        print("SIMULATION COMPLETE")
        print(f"Your Score: {final_score:.2f}%")
        print("="*50)
        
        if hired_candidate == best_candidate:
            print("INCREDIBLE! You actually hired the absolute BEST candidate in the pool!")
        else:
            print(f"\nMissing out is the true opportunity cost!")
            print(f"The TRUE best candidate was Candidate {best_candidate_index}.")
            print("Their target qualities were:")
            for quality in DESIRED_QUALITIES:
                print(f" - {quality}: {best_candidate[quality]}/100")
            print(f"Their calculated score was: {score_candidate(best_candidate):.2f}")
        print("="*50)