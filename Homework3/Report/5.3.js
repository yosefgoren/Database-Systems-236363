db.s.aggregate([
	{
	  $group: {
		_id: {
		  university: "$university",
		  estimated_retirement_year: "$estimated_retirement_year"
		},
		total_current_salary: { $sum: "$salary" },
		total_retirement_salary: { $sum: "$estimated_retirement_salary" }
	  }
	},
	{
	  $group: {
		_id: "$_id.university",
		retirement_years: {
		  $push: {
			estimated_retirement_year: "$_id.estimated_retirement_year",
			salary_delta: { $subtract: ["$total_current_salary", "$total_retirement_salary"] }
		  }
		}
	  }
	}
  ])
  