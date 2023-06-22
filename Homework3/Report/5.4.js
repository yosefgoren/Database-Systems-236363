db.s.mapReduce(
	function() {
		emit(this.university, [this.estimated_retirement_year, this.salary, this.estimated_retirement_salary]);
	},
	function(university, staff_memebers) {
		expensive_staff_memebers_count = 0;
		for(memebr_details in staff_memebers){
			retire_year = memebr_details[0];
			cur_salary = memebr_details[1];
			retire_salary = memebr_details[2];
			if(retire_salary*1.5 <= cur_salary){
				expensive_staff_memebers_count++;
				if(expensive_staff_memebers_count > 20){
					break;
				}
			}
		}
		if(expensive_staff_memebers_count > 0){
			return 1;
		} else {
			return 0;
		}
	},
	{
		query: {estimated_retirement_year: {$gte:2025, $lte:2030}},
		out: "expensive_staff_unis"
	}
)
