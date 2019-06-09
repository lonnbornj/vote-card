import process_policy_data
import numpy as np
import operator
import time


def weighted_eucl_dist(weights, v1, v2):
	norm = np.sqrt(len(v1))*100
	dist_vec = np.array(v1)-np.array(v2)
	return np.sqrt(np.sum(weights*(dist_vec)**2))/norm

def get_user_input(question):
	while True:
			try:
				inp = float(input("{}: ".format(question)))
				if inp < 0 or inp > 100:
					raise ValueError
				break
			except ValueError:
				print("Please enter a number between 0 and 100")
	return inp

def quiz_user(policy_ids):

	user_pos = []
	user_weights = []

	input("For each of the following statements, enter a number out of 100 indicating:\n" + 
			"\ti.\tThe extent to which you agree;\n" +
			"\tii.\tThe extent to which you feel the issue is important; in other words, the extent to which it is important to you that a politician agrees with your position on it.\n"
		"100 means complete agreement (importance), 0 means complete disagreement (of no importance)\n\n" +
		"Press ENTER to continue.")

	for i, pol_id in enumerate(policy_ids):
		pol_name, pol_desc = process_policy_data.fetch_policy_info(pol_id)

		print(	"\n----------\n{}. ".format(i+1) + pol_name +
				"\n----------\n" + pol_desc + "\n")

		a = get_user_input("Agreement")
		i = get_user_input("Importance")

		user_pos.append(a)
		user_weights.append(i)

	return user_pos, user_weights


def get_dists(policy_ids, user_pos, user_weights):
	rep_dists = []
	rep_objects, _ = process_policy_data.main(policy_ids)
	for rep in rep_objects:
		rep_pos = [i[1] for i in rep.policies.values()]
		dist = weighted_eucl_dist(user_weights, user_pos, rep_pos)
		rep_dists.append((" ".join(rep.name), rep.party, dist))
	rep_dists.sort(key = operator.itemgetter(2))
	return rep_dists

def main(policy_ids):

	user_pos, user_weights = quiz_user(policy_ids)
	dists = get_dists(policy_ids, user_pos, user_weights)
	print("\nYour political spirit animal is......\n")
	print(dists[0][0].upper() + "!!! ({})".format(dists[0][1]))
	print("...at a distance of {0:1.4f}".format(dists[0][2]))
	input("Press ENTER. ")
	print(	"\nA smaller distance means greater political affinity.\n" +
			"The politicians closest to you in this `ideology-space` are:\n")
	for i, dist in enumerate(dists[:10]):
		print("{0}. {1[0]} ({1[1]}): {1[2]:1.4f}".format(i+1, dist))
	input("Press ENTER. ")	
	print("\n...While those furthest away are:")
	for i, dist in enumerate(dists[-10:]):
		print("{0}. {1[0]} ({1[1]}): {1[2]:1.4f}".format(len(dists)-i, dist))

if __name__ == "__main__":
	policy_ids = list(range(1,3))
	main(policy_ids)