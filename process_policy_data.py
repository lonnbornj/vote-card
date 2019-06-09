import json
import os
import pull_policy_data
from Classes import *

def read_policy_data(policy_id):
	with open("data/policy{}.txt".format(policy_id), "rb") as f:
		raw_policy_data = f.read()
	return json.loads(raw_policy_data.decode('utf-8'))

def fetch_policy_info(policy_id):
	raw_data = read_policy_data(policy_id)
	return raw_data["name"], raw_data["description"]

def repackage_rep_data(raw_data):
	rep_info = raw_data["person"]["latest_member"]
	name = (rep_info["name"]["first"], rep_info["name"]["last"])
	data = {"name": name, 
			"tvfy_id": raw_data["person"]["id"],
			"electorate": rep_info["electorate"], 
			"party": rep_info["party"], 
			"house": rep_info["house"],  
			"voted": raw_data["voted"],
			"agreement": raw_data["agreement"]}
	return data

def get_or_make_rep(data, all_reps, policy_ids):
	obj = next((rep for rep in all_reps if rep.name == data["name"]), None)
	if obj is None:
		obj = Representative(data)
		obj.add_missing_policies(policy_ids)
		all_reps.append(obj)
	return obj


def main(policy_ids):

	all_reps = []
	all_parties = []

	for pol_id in policy_ids:

		if not os.path.exists("data/policy{}.txt".format(pol_id)):
			pull_policy_data.write_data(pol_id)
		raw_data = read_policy_data(pol_id)

		for rep in raw_data["people_comparisons"]:
			data = repackage_rep_data(rep)
			rep_obj = get_or_make_rep(data, all_reps, policy_ids)
			rep_obj.update_pol_position(pol_id, data["voted"], data["agreement"])
			p = rep_obj.join_or_make_party(all_parties)
			p.add_missing_policies(policy_ids)

	for party in all_parties:
		for pol_id in policy_ids:
			party.calc_ave_agreem(pol_id, all_reps)

	for rep in all_reps:
		rep.update_None_agreem(policy_ids, all_parties)

	return all_reps, all_parties

if __name__ == "__main__":
	main([21])