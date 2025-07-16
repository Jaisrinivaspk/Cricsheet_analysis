from database.run_query import run_query

def load_queries(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return [q.strip() for q in content.split(";") if q.strip()]

queries = load_queries("sql/analysis_queries.sql")  # use relative path

for i, query in enumerate(queries, start=1):
    print(f"\n🟦 Query {i}:\n{'-'*40}")
    try:
        result_df = run_query(query)
        print(result_df.head())  # show top few rows
    except Exception as e:
        print(f"❌ Error in Query {i}: {e}")
