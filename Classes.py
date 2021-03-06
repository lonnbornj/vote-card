import numpy as np


class Representative:
    def __init__(self, data):

        self.name = data["name"]
        self.tvfy_id = data["tvfy_id"]  # id assigned by theyvoteforyou.org
        self.party = data["party"]
        self.house = data["house"]  # senate or HoR
        self.electorate = data["electorate"]
        self.policies = {}

    def join_or_make_party(self, all_parties):
        """
		If it doesn't exist, creates a Party object for the rep's party. Adds the rep to its list of members.
		"""
        party_obj = next((p for p in all_parties if p.name == self.party), None)
        if party_obj is None:
            party_obj = Party(self.party)
            all_parties.append(party_obj)
        if self.name not in party_obj.all_members:
            party_obj.all_members.append(self.name)
        return party_obj

    def update_pol_position(self, policy_id, voted, agreement):
        """
		Updates a rep's position on a policy, if they've ever voted on it.
		"""
        if voted:
            self.policies[policy_id] = [voted, float(agreement)]

    def add_missing_policies(self, policy_ids):
        """
		For each policy, creates a placeholder entry in `policies`. The placeholder
		values ([False, None]) are later updated according to voting history.
		"""
        for pol_id in policy_ids:
            if not pol_id in self.policies:
                self.policies[pol_id] = [False, None]

    def update_None_agreem(self, policy_ids, all_parties):
        """
		Where the rep hasn't voted on any divisions relating to a policy,
		inserts their party's average position.
		"""
        for pol_id in policy_ids:
            if self.policies[pol_id][1] == None:
                p = self.join_or_make_party(all_parties)
                self.policies[pol_id][1] = p.policies[pol_id][1]


class Party:
    def __init__(self, name):

        self.name = name
        self.candidates = []
        self.all_members = []
        self.policies = {}

    def get_member_objs(self, all_reps):
        """
		Returns the Representative object for all members of a party
		"""
        member_objs = [rep for rep in all_reps if rep.name in self.all_members]
        return member_objs

    def add_missing_policies(self, policy_ids):
        """
		For each policy, creates a placeholder entry in `policies`.
		See also Representative.add_missing_policies.
		"""
        for pol_id in policy_ids:
            if not pol_id in self.policies:
                self.policies[pol_id] = [False, None]

    def calc_ave_agreem(self, policy_id, all_reps):
        """
		Calculates the party's average position on a policy, based on the
		voting history of members who have voted on that policy.
		"""
        member_objs = self.get_member_objs(all_reps)
        mask = [r.policies[policy_id][0] for r in member_objs]
        positions = np.array([r.policies[policy_id][1] for r in member_objs])[mask]

        if len(positions) == 0:
            # If nobody in the party has ever voted on the issue,
            # set voted flag to `false` and assign 50/100
            voted, ave_agreem = False, 50.0
        else:
            # Otherwise, assign the mean position of members who have voted
            voted, ave_agreem = True, np.mean(positions)
        self.policies[policy_id] = [voted, ave_agreem]
