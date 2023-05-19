from utils.gpt import COMPLETION_MODEL_3_5, COMPLETION_MODEL_4, extract_json_from_text_string, gpt_completion

# ==========================================================
# TREES OF THOUGHT
# https://huggingface.co/papers/2305.10601
# Trying to implement this idea, but the implementation details are super vague, so reproducing is hard.
# It seems as if they have a more complex agent/task running setup going
# ---
# Concepts to explore
# - breadth vs depth search of several plans (at which point does the system reflect)
# - How can this more closely reflect human exploration/planning
# ==========================================================


def tot(prompt_task):
		print(f'\nPROMPT:\n{prompt_task}\n')
		# THOUGHT STEP #1: GET IMPLICIT NORTH STAR
		# Finding that I need to steer the plan statements a bit, so they don't disregard the writing task, but think more wholistcally
		# success_criteria = gpt_completion(
		# 	prompt=f'In a single sentence, describe a successful outcome for user in the following task. TASK: {prompt_task}',
		# 	model=COMPLETION_MODEL_4)
		# print(f'\nSUCCESS CRITERIA:\n{success_criteria}\n')

		# THOUGHT STEP #2: GENERATE PLANS (5)
		# v1 - repeated task with success 
		# prompt_plan_v1 = f'Do the following task. SUCCESS CRITERIA: {success_criteria} TASK: {prompt_task}'
		prompt_plan_v2 = f'Describe a way to be successful in the following task. TASK: {prompt_task}'
		plans = []
		while len(plans) < 3:
				print('Planning...')
				fetched_plan = gpt_completion(prompt=prompt_plan_v2, model=COMPLETION_MODEL_4)
				plans.append(fetched_plan)
		print(f'PLAN EXECUTIONS:\n')
		print("\n---\n".join(plans))
		print("\n\n")

		# THOUGHT STEP #3: VOTE (5)
		# --- generate
		votes = []
		while len(votes) < 5:
				print('Voting...')
				execution_plans = "\n\n".join(f"CHOICE {idx}) {str}" for idx, str in enumerate(plans))
				vote_response = gpt_completion(
					prompt=f'Analyizing each choice in detail in relation to the task, choose the best and respond in JSON format with keys "choice_integer" and "choice_reason". TASK: {prompt_task} \n\n {execution_plans}',
					model=COMPLETION_MODEL_3_5)
				votes.append(vote_response)
		# --- tally
		tally = dict()
		for vote_string in votes:
				try:
						json = extract_json_from_text_string(vote_string)
						choice = int(json['choice_integer'])
						print(f'Voted {choice}: {json.get("choice_reason", "")[0:300]}...')
						tally[choice] = tally.get(choice, 0) + 1
				except Exception as err: 
						print('No vote json/choice.', err)
		print(f'\nTALLY:\n{tally}\n')

		# THOUGHT STEP #4: Use highest vote as inspiration, write again
		highest_voted_plan = plans[max(tally)]
		final_execution = gpt_completion(
				prompt=f'Do the following task.\n\nINSPIRATION: {highest_voted_plan}\n\nTASK: {prompt_task}',
				model=COMPLETION_MODEL_4)
		# RETURN (select plan via index with highest int)

		return final_execution
		


# ==========================================================
# TEST: Creative Writing
# ==========================================================
prompt = "Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: 1. It isn't difficult to do a handstand if you just stand on your hands. 2. It caught him off guard that space smelled of seared steak. 3. When she didn't like a guy who was trying to pick her up, she started using sign language. 4. Each person who knows you has a different perception of who you are."
response_tot = tot(prompt)
print(f'========== ToT Response ==========')
print(response_tot)
print(f'========== IO Response ==========')
response_io = gpt_completion(prompt=prompt, model=COMPLETION_MODEL_4)
print(response_io)

# Comparison of ToT and IO responses
# Result: ToT voted on a plan that presented the thread/idea of personal growth

# ToT  --> 
# The journey of personal growth is often paved with new experiences that teach us valuable lessons about ourselves and the world around us. As we face challenges and learn new skills, we become more versatile and resilient. One such example can be seen in the process of learning to do a handstand. With dedication and practice, one can go from barely being able to balance on their hands to confidently performing this impressive feat. It isn't difficult to do a handstand if you just stand on your hands.
# Sometimes, these lessons come from unexpected sources and can catch us completely off guard. An astronaut, venturing into the vastness of space for the first time, might anticipate many strange and wonderful sights. However, they might not expect the peculiar sensory experiences that await them. Floating weightlessly in the International Space Station, the astronaut noticed an odd aroma filling the airlock after a spacewalk. It caught him off guard that space smelled of seared steak.
# Creative problem-solving is another skill we often develop through personal experiences. Life has a way of presenting us with difficult situations that require quick thinking and adaptability. For instance, a woman at a bar might find herself dealing with the unwelcome advances of a man. Rather than confronting him outright or enduring the uncomfortable situation, she devises a clever solution to deter his attention. When she didn't like a guy who was trying to pick her up, she started using sign language.
# Ultimately, our experiences shape not only our skills and knowledge but also how others perceive us. As we navigate through life, each person we encounter will form their own unique understanding of who we are based on their interactions with us. Just as the handstand practitioner becomes an acrobat in the eyes of their friends, or the astronaut becomes a connoisseur of cosmic cuisine, each experience we have contributes to the multifaceted identity we present to the world. Each person who knows you has a different perception of who you are.

# IO --> 
# Learning to do a handstand can be an exciting and rewarding experience. It requires dedication, practice, and most importantly, confidence. To get started, find a suitable spot with plenty of space and a soft surface. Begin by positioning your hands shoulder-width apart and slowly lift your legs up into the air. With enough practice, it isn't difficult to do a handstand if you just stand on your hands.
# During a recent interview, an astronaut shared his intriguing experiences from his time in space. One peculiar observation he made was that the International Space Station had a distinct smell. He described it as a mixture of metal and something else distinctly familiar. It caught him off guard that space smelled of seared steak.
# In a crowded bar, a woman noticed a man attempting to approach her. She wasn't interested in his advances, so she decided to come up with a creative way to avoid engaging in conversation with him. Instead of simply turning him down, she acted as if she couldn't hear him. When she didn't like a guy who was trying to pick her up, she started using sign language.
# The way we perceive ourselves may not necessarily align with how others perceive us. Our friends, family, and acquaintances all have unique experiences and interactions with us that shape their individual understanding of our character. It is important to remember that, just like a kaleidoscope, each person who knows you has a different perception of who you are.

# ==========================================================
exit()
