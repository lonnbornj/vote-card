"""
Collects the user's views on n different policies, and finds MPs who have the most 
similar views by computing the weighted euclidean distance in n-dimensional space.
Uses the importance assigned these issues by the user as the weights.
"""
import process_policy_data
import numpy as np
import operator


def weighted_eucl_dist(weights, v1, v2):
    """
	Calculates the weighted Euclidean distance between two vectors
	"""
    norm = len(v1)
    dist_vec = np.array(v1) - np.array(v2)
    return np.sqrt(np.sum(weights * (dist_vec) ** 2)) / norm


def get_user_input(question):
    """
	Accepts and validates user input to a policy question.
	"""
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
    """
	Asks the user a series of questions on different policies,
	and returns their agreement with and weighting of those issues as lists
	"""

    user_pos = []
    user_weights = []

    input(
        "For each of the following statements, enter a number out of 100 indicating:\n"
        "\ti.\tThe extent to which you agree;\n"
        "\tii.\tThe extent to which you feel the issue is important; "
        "in other words, the extent to which it is important to you that a "
        "politician agrees with your position on it.\n"
        "100 means complete agreement (importance), 0 means complete disagreement "
        "(of no importance)\n\n"
        "Press ENTER to continue."
    )

    for i, pol_id in enumerate(policy_ids):
        pol_name, pol_desc = process_policy_data.fetch_policy_info(pol_id)

        print(
            "\n----------\n{}. ".format(i + 1)
            + pol_name
            + "\n----------\n"
            + pol_desc
            + "\n"
        )

        a = get_user_input("Agreement")
        i = get_user_input("Importance")

        user_pos.append(a)
        user_weights.append(i)

    return user_pos, user_weights


def get_dists(policy_ids, user_pos, user_weights):
    """
	Computes the weighted euclidean distance (with respect to a series of policy
	issues) between the user and everyone in parliament who has voted on one
	of those issues.
	"""
    rep_dists = []
    rep_objects, _ = process_policy_data.main(policy_ids)
    for rep in rep_objects:
        rep_pos = [i[1] for i in rep.policies.values()]
        dist = weighted_eucl_dist(user_weights, user_pos, rep_pos)
        rep_dists.append((" ".join(rep.name), rep.party, dist))
    rep_dists.sort(key=operator.itemgetter(2))
    return rep_dists


def main(policy_ids):

    filename = "test.txt"

    user_pos, user_weights = quiz_user(policy_ids)
    dists = get_dists(policy_ids, user_pos, user_weights)
    with open("{}".format(filename), "w") as f:
        for i, d in enumerate(dists):
            f.write("{0}. {1[0]} ({1[1]}): {1[2]:1.4f}\n".format(i + 1, d))
        f.write(
            "# INPUT\nPolicy IDs: {0}\nUser agreement: {1}\nUser weights: {2}".format(
                policy_ids, user_pos, user_weights
            )
        )
    print("\nWrote output to {}".format(filename))


if __name__ == "__main__":
    policy_ids = list(range(1, 26))
    main(policy_ids)
