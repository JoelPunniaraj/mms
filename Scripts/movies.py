import sqlite3

connect = sqlite3.connect(r'C:\Users\joelp\python\projects\mms\movies.db')

c = connect.cursor()

print("\nWelcome to My Movie List!")
def movie_rating():
    print("\nScore Rating Key:")
    print("9 - Elite")
    print("8 - Outstanding")
    print("7 - Expectational")
    print("6 - Average")
    print("5 - Subpar")
    print("4 - Unsatisfactory")
    print("3 - Poor")
    print("2 - Unplesant")
    print("1 - Horrible")

movie_rating()

c.execute('''CREATE TABLE IF NOT EXISTS movies (
                title TEXT PRIMARY KEY,
                director TEXT,
                acting INTEGER,
                writing INTEGER,
                production INTEGER,
                screenplay INTEGER,
                cinematography INTEGER,
                experience INTEGER
            )''')
connect.commit()

def add_movie():
    title = input("\nTitle: ")
    director = input("Director: ")
    acting = int(input("Acting: "))
    writing = int(input("Writing: "))
    production = int(input("Production: ")) 
    screenplay = int(input("Screenplay: "))
    cinematography = int(input("Cinematography: "))
    experience = int(input("Experience: "))

    try:
        c.execute('''INSERT INTO movies (title, 
                  director, acting, writing, production, screenplay, cinematography, experience)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (title, 
                     director, 
                     acting, 
                     writing, 
                     production, 
                     screenplay, 
                     cinematography, 
                     experience))
        connect.commit()
        print("Movie Added Successfully!")
    except sqlite3.IntegrityError:
        print("Movie Already Exists!")

def view_directors():
    print("> Top")
    print("> Name")
    choice = input("\nEnter Your Choice: ").lower()
    if choice == 'name':
        director_name = input("Enter The Director's Name: ")
        print("")
        c.execute('''SELECT * FROM movies WHERE director = ? ORDER BY title''', (director_name,))
        movies = c.fetchall()
        if not movies:
            print("No Movies Found for Director:", director_name)
        else:
            total_rating = 0
            movie_count = 0
            best_movies = []
            for movie in movies:
                title, director, acting, writing, production, screenplay, cinematography, experience = movie
                ratings_concatenated = int(f"{acting}{writing}{production}{screenplay}{cinematography}{experience}")
                rating_average = round(round(float(((acting + writing + screenplay) * 0.5 + (production + cinematography) * 0.25 + (experience) * 0.25) / 20.50), 2) * 10, 1)
                total_rating += rating_average
                movie_count += 1
                print((title, director, ratings_concatenated, rating_average))
                best_movies.append((title, rating_average))
            if movie_count > 0:
                average_rating = total_rating / movie_count
                print(f"\nAverage Rating for Movies by {director_name}: {round(average_rating, 1)}")
                print("")
                best_movies.sort(key=lambda x: x[1], reverse=True)
                if movie_count > 5:
                    top = 5
                else:
                    top = movie_count
                print(f"Top {top} Rated Movies by {director_name}:")
                for i, (title, rating) in enumerate(best_movies[:5], start=1):
                    print(f"{i}. {title} - {rating}")
    elif choice == 'top':
        print("")
        c.execute('''SELECT UPPER(SUBSTR(director, 1, 1)) || LOWER(SUBSTR(director, 2)) AS director, 
                     ROUND(AVG(ROUND(((acting + writing + screenplay) * 0.5 
                     + (production + cinematography) * 0.25 
                     + experience * 0.25) / 20.50, 2) * 10), 1) AS avg_rating 
                     FROM movies 
                     GROUP BY director 
                     HAVING COUNT(*) > 3
                     ORDER BY avg_rating DESC 
                     LIMIT 5''')
        top_directors = c.fetchall()
        if top_directors:
            print("Top Directors by Average Movie Rating:")
            for i, (director, avg_rating) in enumerate(top_directors, start=1):
                print(f"{i}. {director.title()} - {avg_rating}")  # Capitalize the director's name
            return
        else:
            print("No Movies Found!")

def view_movies():
    print("\nView Options:")
    print("> Top 5")
    print("> Top 20")
    print("> All Movies")
    
    choice = input("\nEnter Your Choice: ").lower()
    
    if choice == 'top 5':
        print("")
        c.execute('''SELECT title, 
                    ROUND(((acting + writing + screenplay) * 0.5 
                    + (production + cinematography) * 0.25 
                    + (experience) * 0.25) / 20.50, 2) 
                    * 10 AS avg_rating 
                    FROM movies 
                    ORDER BY avg_rating DESC 
                    LIMIT 5''')
        top_movies = c.fetchall()
        if top_movies:
            print("Top 5 Rated Movies:")
            for i, (title, rating_average) in enumerate(top_movies, start=1):
                rating_average = round(rating_average, 1) 
                print(f"{i}. {title} - {rating_average}")
            return  
        else:
            print("No Movies Found!")    

    if choice == 'top 20':
        print("")
        c.execute('''SELECT title, 
                    ROUND(((acting + writing + screenplay) * 0.5 
                    + (production + cinematography) * 0.25 
                    + (experience) * 0.25) / 20.50, 2) 
                    * 10 AS avg_rating 
                    FROM movies 
                    ORDER BY avg_rating DESC 
                    LIMIT 20''')
        top_movies = c.fetchall()
        if top_movies:
            print("Top 20 Rated Movies:")
            for i, (title, rating_average) in enumerate(top_movies, start=1):
                rating_average = round(rating_average, 1) 
                print(f"{i}. {title} - {rating_average}")
            return  
        else:
            print("No Movies Found!")

    elif choice == 'all':
        print("")
        c.execute('''SELECT * FROM movies ORDER BY title''')
        movies = c.fetchall()
        if not movies:
            print("No Movies Found!")
        else:
            for movie in movies:
                title, director, acting, writing, production, screenplay, cinematography, experience = movie
                ratings_concatenated = int(f"{acting}{writing}{production}{screenplay}{cinematography}{experience}")
                rating_average = round(round(float(((acting + writing + screenplay) * 0.5 + (production + cinematography) * 0.25 + (experience) * 0.25) / 20.50), 2) * 10, 1)
                print((title, director, ratings_concatenated, rating_average))
    else:
        print("Invalid Choice. Please Try Again!")

def remove_movie():
    title = input("Title Of The Movie to Remove: ")
    c.execute('''DELETE FROM movies WHERE title = ?''', (title,))
    connect.commit()
    print("Movie Removed Successfully!")

def edit_movie():
    title = input("Title Of The Movie To Edit: ")
    c.execute('''SELECT * FROM movies WHERE title = ?''', (title,))
    movie = c.fetchone()
    if not movie:
        print("Movie Not Found!")
        return

    print("\nEdit Options:")
    print("> Title")
    print("> Director(s)")
    print("> Acting")
    print("> Writing")
    print("> Production")
    print("> Screenplay")
    print("> Cinematography")
    print("> Experience")
    print("> All\n")

    choice = input("What Do You Want to Edit? ").lower()
    if choice == 'title':
        field_name = 'title'
    elif choice == 'director':
        field_name = 'director'
    elif choice == 'acting':
        field_name = 'acting'
    elif choice == 'writing':
        field_name = 'writing'
    elif choice == 'production':
        field_name = 'production'
    elif choice == 'screenplay':
        field_name = 'screenplay'
    elif choice == 'cinematography':
        field_name = 'cinematography'
    elif choice == 'experience':
        field_name = 'experience'
    elif choice == 'all':
        field_name = 'all'
    else:
        print("Invalid choice!")
        return

    if field_name == 'all':
        print("")
        acting = int(input("New Rating for Acting: "))
        writing = int(input("New Rating for Writing: "))
        production = int(input("New Rating for Production: "))
        screenplay = int(input("New Rating for Screenplay: "))
        cinematography = int(input("New Rating for Cinematography: "))
        experience = int(input("New Rating for Experience: "))

        c.execute('''UPDATE movies SET acting = ?, writing = ?, production = ?, screenplay = ?, cinematography = ?, experience = ?
                     WHERE title = ?''', (acting, writing, production, screenplay, cinematography, experience, title))
    else:
        new_value = input(f"Enter the new value for {field_name.capitalize()}: ")
        if field_name in ['acting', 'writing', 'production', 'screenplay', 'cinematography', 'experience']:
            new_value = int(new_value)

        c.execute(f'''UPDATE movies SET {field_name} = ? WHERE title = ?''', (new_value, title))
    connect.commit()
    print("Movie Rating Edited Successfully!")

def show_menu():
    print("\nList Options:")
    print("> View")
    print("> Add")
    print("> Edit")
    print("> Remove")
    print("> Exit\n")

def sub_menu():
    top = input("By Movies or Director? ")
    if top == 'movies':
        view_movies()
    elif top == 'director':
        view_directors()

def main():
    while True:
        show_menu()
        choice = input("Enter Your Choice: ").lower()
        if choice == 'view':
            sub_menu()
        elif choice == 'add':
            key = input("Do You Need a Rating Key? ").lower()
            if key == 'yes':
                movie_rating()
                print("")
                add_movie()
            else:
                add_movie()
        elif choice == 'edit':
            key = input("Do You Need a Rating Key? ").lower()
            if key == 'yes':
                movie_rating()
                print("")
                edit_movie()
            else:
                edit_movie()
        elif choice == 'remove':
            remove_movie()
        elif choice == 'exit':
            break
        else:
            print("Invalid Choice! Please try again.")

if __name__ == "__main__":
    main()

