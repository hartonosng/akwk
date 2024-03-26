# akwk


import re

def extract_table_names(main_query_part):
    # Menemukan semua nama tabel yang didefinisikan dalam CTE
    table_names = re.findall(r'(\b\w+\b)\s+AS\s+\(', main_query_part)
    # Mengembalikan nama tabel dalam bentuk pasangan (nama, alias)
    return [(name, name) for name in table_names]


def replace_table_references(main_query_part, table_names):
    for name, alias in table_names:
        # Menerapkan penggantian string pada klausa SELECT dan WHERE
        main_query_part = re.sub(fr'\b{re.escape(name)}\b(?! AS \()', f'{{ref("{alias}")}}', main_query_part)
    return main_query_part


def extract_sql_queries(sql):
    # Regular expression pattern to match SQL queries including CTE definitions
    pattern = r'(?i)(?:\bWITH\b.*?\bAS\b|\bSELECT\b).*?(?=\bWITH\b|\bSELECT\b|\Z)'
    queries = re.findall(pattern, sql, re.DOTALL)
    return queries

def clean_sql_query(query):
    # Remove leading and trailing whitespace
    query = query.strip()
    # Remove semicolon at the end if present
    query = query.rstrip(';')
    # Remove CTE definitions
    query = re.sub(r'\bWITH\b.*?(?=\bSELECT\b)', '', query, flags=re.DOTALL)
    # Remove extra characters at the end
    query = re.sub(r'\)[^\)]*$', '', query)
    return query

def filter_select_queries(queries):
    return [query for query in queries if query.startswith('SELECT')]


# Example CTE SQL statement
cte_sql = """
WITH ayam AS (
    SELECT column1 FROM table1 WHERE condition1 and ayams
),
CTE2 AS (
    SELECT column2 FROM table2 WHERE condition2
),
CTE3 AS (
    SELECT column3 FROM table3
),
CTE4 AS (
    SELECT column4 FROM table4 WHERE condition4
),
CTE5 AS (
    SELECT column5 FROM table5 WHERE condition5
)
SELECT column1, column2, column3, column4, column5
FROM ayam
JOIN CTE2 ON CTE.column1 = CTE2.column2
JOIN CTE3 ON CTE2.column2 = CTE3.column3
JOIN CTE4 ON CTE3.column3 = CTE4.column4
JOIN CTE5 ON CTE4.column4 = CTE5.column5
WHERE additional_condition;
"""

table_names = extract_table_names(cte_sql)
main_query_part = replace_table_references(cte_sql, table_names)


# Extract SQL queries from CTE SQL
sql_queries = extract_sql_queries(main_query_part)

# Filter and clean SELECT queries
select_queries = filter_select_queries(sql_queries)
cleaned_queries = [clean_sql_query(query) for query in select_queries[:-1]]+[select_queries[-1]]

# Print cleaned SQL queries
for i, query in enumerate(cleaned_queries, start=1):
    print(f"SQL Query {i}:")
    print(query)
    print("\n-----------------------\n")
cleaned_queries
