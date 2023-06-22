db.SeniorStaff.aggregate([
	{
		$match: {
			seniority_year: { $gt: 2013 }
		}
	},
	{
	  $group: {
		_id: "$university",
		staff_members: {
			$push: {
				staff_member_name: "$staff_member_name",
				staff_member_id: "$staff_member_id"
			}
		}
	  }
	}
])