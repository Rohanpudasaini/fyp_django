import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def recommend(df, book_title):
    book_title = str(book_title)
    if book_title in df['Book-Title'].values:
        rating_count=pd.DataFrame(df["Book-Title"].value_counts())
        rare_books=rating_count[rating_count["count"]<=100].index
        common_books=df[~df["Book-Title"].isin(rare_books)]
        # rare_books =   pd.read_csv('rare_books.csv', index_col=0)
        # common_books = pd.read_csv('common_books.csv', index_col=0)

        if book_title in rare_books:
            print("rare books")
            most_common=pd.Series(common_books["Book-Title"].unique()).sample(3).values
            # print("No Recommendation for that book")
            books = []
            for book in most_common:
                books.append(book)
            return books

        else:
            common_books=common_books.drop_duplicates(subset=["Book-Title"])
            common_books.reset_index(inplace=True)
            common_books["index"]=[i for i in range(common_books.shape[0])]
            targets=["Book-Title","Book-Author","Publisher"]
            common_books["all_features"] = [" ".join(common_books[targets].iloc[i,].values) for i in range(common_books[targets].shape[0])]
            vectorizer=CountVectorizer()
            common_booksVector=vectorizer.fit_transform(common_books["all_features"])
            similarity=cosine_similarity(common_booksVector)
            index=common_books[common_books["Book-Title"]==book_title]["index"].values[0]
            similar_books=list(enumerate(similarity[index]))
            similar_booksSorted=sorted(similar_books,key=lambda x:x[1],reverse=True)[1:5]
            books=[]
            for i in range(len(similar_booksSorted)):
                # books.append(common_books[common_books["index"]==similar_booksSorted[i][0]]["Book-Title"].item())
                book = common_books[common_books["index"]==similar_booksSorted[i][0]]["Book-Title"].item()
                # if len(book) <= 5:
                #     book = " ".join(book)
                # else:
                #     book = " ".join(book[:5])
                books.append(book)
            print(books)
            return(books)
    else:
        print("We currently have no data of that book.")
df = pd.read_csv('store/DataFrame.csv',index_col=0)
# book = input("Enter the book name: ").strip()
# result = recommend(df,book)
# if result:
#     print(result)

        
    
    