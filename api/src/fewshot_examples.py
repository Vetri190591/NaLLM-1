 return f"""
#How is Emil Eifrem connected to Michael Hunger?
MATCH (p1:Person {{name:"Emil Eifrem"}}), (p2:Person {{name:"Michael Hunger"}})
MATCH p=shortestPath((p1)-[*]-(p2))
RETURN p
#What are the latest news regarding Google?
MATCH (o:Organization {{name:"Google"}})<-[:MENTIONS]-(a:Article)-[:HAS_CHUNK]->(c)
RETURN a.title AS title, c.text AS text, c.date AS date
ORDER BY date DESC LIMIT 3
#Are there any news regarding return to office policies?
CALL apoc.ml.openai.embedding(["Are there any news regarding return to office policies?"], 
   "{openai_api_key}") YIELD embedding
MATCH (c:Chunk)
WITH c, gds.similarity.cosine(c.embedding, embedding) AS score
ORDER BY score DESC LIMIT 3
RETURN c.text, score
#What is Microsoft policy regarding to the return to office?
CALL apoc.ml.openai.embedding(["What is Microsoft policy regarding to the return to office?"], "{openai_api_key}") YIELD embedding
MATCH (o:Organization {{name:"Microsoft"}})<-[:MENTIONS]-()-[:HAS_CHUNK]->(c)
WITH distinct c, embedding
WITH c, gds.similarity.cosine(c.embedding, embedding) AS score
ORDER BY score DESC LIMIT 3
RETURN c.text, score
#What are the relationships associated with the batch node?
MATCH (Batch) MATCH ()-[r]->() RETURN Batch, r
#What are the properties of my node?
Match (n) return properties(n), ID(n)
#What are the properties of Batch?
Match (Batch) return properties(Batch)
#What are the sites nucala is manufactured?
match(m:Batch)-[made_of]->(n:Material) where n.`material desc` contains 'nucala' return m.sitecode
#What are the various sites nucala is manufactured?
CALL apoc.ml.openai.embedding(["Which sites nucala is manufactured?"], "{openai_api_key}") YIELD embedding
MATCH (n:Material {`material desc`:"nucala"})<-[:made_of]-()-[:HAS_CHUNK]->(c)
WITH distinct c, embedding
WITH c, gds.similarity.cosine(c.embedding, embedding) AS score
ORDER BY score DESC LIMIT 3
RETURN c.text, score
When searching for specific information in the text chunks, never use the CONTAINS clause, but always use the apoc.ml.openai.embedding
and gds.similarity.cosine functions as shown in the examples.
When returning text chunks, always return exactly three chunks, no more, no less.
Remember, instead of using CONTAINS to find information within text chunks use the apoc.ml.openai.embedding and gds.similarity.cosine functions.
"""
