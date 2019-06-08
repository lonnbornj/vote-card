import json
import os
from numpy import mean
from collections import defaultdict
import pull_policy_data


def read_policy_data(policy_id):
	with open("data/policy{}.txt".format(policy_id), "rb") as f:
		raw_policy_data = f.read()
	return json.loads(raw_policy_data.decode('utf-8'))

def get_agreement(rep):
	if rep["voted"] == True:
		return float(rep["agreement"])
	elif rep["voted"] == False:
		return py_agreem_av[rep["party"]]

def calculate_party_aves(rep_data):
	py_agreem_tmp, py_ave_agreem = defaultdict(list), dict()
	for rep_val in rep_data.values():
		if rep_val["voted"]:
			py_agreem_tmp[rep_val["party"]].append(float(rep_val["agreement"]))
	for party, value in py_agreem_tmp.items():
		py_ave_agreem[party] = mean(value)
	add_agreem_data(rep_data, py_ave_agreem)

def repackage_rep_data(policy_id):
	rep_data_temp = read_policy_data(policy_id)["people_comparisons"]
	rep_data = dict()
	for rep in rep_data_temp:
		person = rep["person"]["latest_member"]
		name = (person["name"]["first"], person["name"]["last"])
		rep_data[" ".join(name)] = {"name": name, 
									"electorate": person["electorate"], 
									"party": person["party"], 
									"house": person["house"],  
									"voted": rep["voted"],
									"agreement": rep["agreement"]}
	return rep_data

def add_agreem_data(rep_data, party_agreem_data):
	for rep in rep_data.values():
		if not rep["voted"]:
			try:
				rep["agreement"] = party_agreem_data[rep["party"]]
			except KeyError:
				rep["agreement"] = 50.0

def update_reps(policy_id):
	rep_data = repackage_rep_data(policy_id)
	calculate_party_aves(rep_data)

	for rep in rep_data.values():
		if rep["house"] == "representatives":
			plms_policy_vec[" ".join(rep["name"])].append(rep["agreement"])
		elif rep["house"] == "senate":
			snrs_policy_vec[" ".join(rep["name"])].append(rep["agreement"])


plms_policy_vec = defaultdict(list)
snrs_policy_vec = defaultdict(list)

def build_policy_vec():

	policy_ids = [1,2,3,4,5,6,7,8,9,10]
	for pol_id in policy_ids:
		if not os.path.exists("data/policy{}.txt".format(pol_id)):
			pull_policy_data.write_data(pol_id)
		update_reps(pol_id)

	return plms_policy_vec, snrs_policy_vec

if __name__=="__main__":
	build_policy_vec()