from app.db import connect, create_table
from app.seed import seed

con = connection()
create_table(con)
print(seed(con))