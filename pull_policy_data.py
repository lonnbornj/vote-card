import requests

key = "XXXXXXXXXXXXXXXXXXXXX"

def get_data(policy_id):
	http = "https://theyvoteforyou.org.au/api/v1/policies/" + policy_id + ".json?key=" + key
	return requests.get(http)

def write_data(policy_id):
	policy_data = get_data(str(policy_id))
	with open("data/policy{}.txt".format(policy_data.json()["id"]), "wb") as f:
		f.write(policy_data.content)
