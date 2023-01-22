import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# I am going to use the collaborative filtering algo


df1 = pd.read_csv("anime.csv")
df2 = pd.read_csv("rating.csv")
n_users = df2.user_id.unique().shape[0] # 73515
n_items = df2.anime_id.unique().shape[0] # 11200
print(n_users, n_items)




information = '''
    (1) USER_ID 46809 IS MISSING 
    (2) anime_id is NOT in consecutive order
'''




df_merge = pd.merge(df1, df2, on = 'anime_id')


df = df_merge[["user_id", "anime_id", "name", "rating_y"]]
df = df[df.rating_y != -1]
df = df.sample(n=60000)
n_user = df.user_id.unique().shape[0]
n_item = df.anime_id.unique().shape[0]

matrix = np.zeros((n_user, n_item))
anime_id_sorted = sorted(df.anime_id.unique())
user_id_sorted = sorted(df.user_id.unique())


for index, row in df.iterrows():
    row_index = user_id_sorted.index(int(row["user_id"]))
    col_index = anime_id_sorted.index(int(row["anime_id"]))
    matrix[row_index, col_index] = row["rating_y"]


new_row = np.zeros((n_item,))
num_inputs = int(input("How many shows do you want to rate? "))
for i in range(num_inputs):
    anime = input("Which anime would you like for #%s? " % (i+1,))
    while df[df["name"] == anime].empty:
        anime = input("Invalid anime. Which anime would you like for #%s? " % (i + 1,))
    rating = float(input("What would you like to rate it on a scale of 1-10? "))
    anime_index = anime_id_sorted.index(int(df1[df1["name"] == anime]["anime_id"].item()))
    new_row[anime_index] = rating




np.append(matrix, new_row)





similarity_matrix = cosine_similarity(matrix, matrix)
index = 0
users_dict = dict()
recommended = dict()

# First check for people who have high scores
for score in similarity_matrix[-1]:
    if (score > 0 and score <= 1) and index < n_user:
        user = user_id_sorted[index]
        users_dict[user] = (score, matrix[index])
    index += 1
user_dict_sorted = sorted(users_dict.items(), key=lambda x:x[1][0], reverse=True)
#print(user_dict_sorted)
# Now go through the top 3 (or however many there are if less than 3)
end = 5 if len(user_dict_sorted) >= 5 else len(user_dict_sorted)
ind = 0
for key, value in user_dict_sorted:
    if ind < end:
        score, ratings = value
        # Now look for anything rated 7 or higher
        print("Score for this user (ID = %s) : %s" % (key, score))
        for r in range(len(ratings)):
            if ratings[r] >= 7:
                anime = anime_id_sorted[r]
                print(df1[df1["anime_id"] == anime]["name"].item())
        ind += 1
    else:
        break




