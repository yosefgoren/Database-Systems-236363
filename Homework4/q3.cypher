Database Structure:
	Label types:
		Breed: name, origin, lifespan
		Cat: name, age gender
		Ownder: name, address

	Relation types:
		BELONGS_TO(Cat, Owner): relationship_length
		DESCENDANT_OF(Breed, Breed):
		OF_BREED(Cat, Breed):

Questions:
	for each Breed, return the name of the breed and the number of cats which directly belong to that breed (OF_BREED).
	Breeds without any cats do not have to be included:
		MATCH (b:Breed) OPTIONAL MATCH (b)<-[:OF_BREED]-(c:Cat) RETURN b.name, count(c) as count ORDER BY count DESC


MATCH (b:Breed)
WITH collect(b) AS breeds

MATCH (o: Owner)
WHERE ALL(b IN breeds WHERE (b)<-[:OF_BREED]-(:Cat)-[:BELONGS_TO]->(o))
RETURN o.name