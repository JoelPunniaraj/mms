import os
import streamlit as stl
import sqlite3 as sql

# Set up Streamlit layout
stl.set_page_config(layout="wide")

# Connect to the SQLite database
connect = sql.connect(r'C:\Users\joelp\python\projects\mms\movies.db')
c = connect.cursor()

# Function to add a movie to the database
def add_movie():
    title = stl.text_input("Title:")
    director = stl.text_input("Director:")
    acting = stl.slider("Acting:", min_value=1, max_value=10, value=5)
    writing = stl.slider("Writing:", min_value=1, max_value=10, value=5)
    production = stl.slider("Production:", min_value=1, max_value=10, value=5)
    screenplay = stl.slider("Screenplay:", min_value=1, max_value=10, value=5)
    cinematography = stl.slider("Cinematography:", min_value=1, max_value=10, value=5)
    experience = stl.slider("Experience:", min_value=1, max_value=10, value=5)

    if stl.button("Add"):
        try:
            c.execute('''INSERT INTO movies (title, director, acting, writing, production, screenplay, cinematography, experience)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (title, director, acting, writing, production, screenplay, cinematography, experience))
            connect.commit()
            stl.write("Movie Added Successfully!")
            stl.experimental_rerun()
        except sql.IntegrityError:
            stl.write("Movie Already Exists!")

def remove_movie():
    title = stl.text_input("Title Of The Movie to Remove:")
    if stl.button("Remove"):
        c.execute('''DELETE FROM movies WHERE title = ?''', (title,))
        connect.commit()
        stl.write("Movie Removed Successfully!")

def edit_movie():
    title = stl.text_input("Title Of The Movie To Edit:")
    c.execute('''SELECT * FROM movies WHERE title = ?''', (title,))
    movie = c.fetchone()
    if not movie:
        stl.write("Movie Not Found!")
        return

    # Define the choices for editing
    edit_options = ["Title", "Director", "Acting", "Writing", "Production", "Screenplay", "Cinematography", "Experience", "All"]
    choice = stl.selectbox("What Do You Want to Edit?", edit_options)

    field_name = ''
    if choice.lower() == 'title':
        field_name = 'title'
    elif choice.lower() == 'director':
        field_name = 'director'
    elif choice.lower() == 'acting':
        field_name = 'acting'
    elif choice.lower() == 'writing':
        field_name = 'writing'
    elif choice.lower() == 'production':
        field_name = 'production'
    elif choice.lower() == 'screenplay':
        field_name = 'screenplay'
    elif choice.lower() == 'cinematography':
        field_name = 'cinematography'
    elif choice.lower() == 'experience':
        field_name = 'experience'
    elif choice.lower() == 'all':
        field_name = 'all'
    else:
        stl.write("Invalid choice!")
        return

    if field_name == 'all':
        stl.write("")
        acting = stl.slider("New Rating for Acting:", min_value=1, max_value=10, value=5)
        writing = stl.slider("New Rating for Writing:", min_value=1, max_value=10, value=5)
        production = stl.slider("New Rating for Production:", min_value=1, max_value=10, value=5)
        screenplay = stl.slider("New Rating for Screenplay:", min_value=1, max_value=10, value=5)
        cinematography = stl.slider("New Rating for Cinematography:", min_value=1, max_value=10, value=5)
        experience = stl.slider("New Rating for Experience:", min_value=1, max_value=10, value=5)

        if stl.button("Submit"):
            try:
                c.execute('''UPDATE movies SET acting = ?, writing = ?, production = ?, screenplay = ?, cinematography = ?, experience = ?
                             WHERE title = ?''', (acting, writing, production, screenplay, cinematography, experience, title))
                connect.commit()
                stl.write("Movie Rating Edited Successfully!")
            except sql.IntegrityError:
                stl.write("Movie with new title already exists!")
    else:
        new_value = stl.text_input(f"Enter the new value for {field_name.capitalize()}:")
        if field_name in ['acting', 'writing', 'production', 'screenplay', 'cinematography', 'experience']:
            new_value = int(new_value)

        if stl.button("Submit"):
            try:
                c.execute(f'''UPDATE movies SET {field_name} = ? WHERE title = ?''', (new_value, title))
                connect.commit()
                stl.write("Movie Rating Edited Successfully!")
            except sql.IntegrityError:
                stl.write("Movie with new title already exists!")



choice = stl.sidebar.selectbox("Select Option:", ("Home", "Rankings", "Settings"))

if choice == 'Home':
    stl.title("Movie Management Software")
    posters_dir = r'C:\Users\joelp\python\projects\mms\posters'
    image_files = os.listdir(posters_dir)

    if image_files:
        stl.subheader("My Top Rated Movies:")
    
        col1, col2, col3, col4, col5 = stl.columns(5)
        
        if len(image_files) >= 1:
            title = os.path.splitext(image_files[0])[0].replace('_', ' ')
            image_path = os.path.join(posters_dir, image_files[0])
            with col5:
                stl.image(image_path, caption=f"5. {title}", width=200) 

        if len(image_files) >= 2:
            title = os.path.splitext(image_files[1])[0].replace('_', ' ')
            image_path = os.path.join(posters_dir, image_files[1])
            with col4:
                stl.image(image_path, caption=f"4. {title}", width=200)

        if len(image_files) >= 3:
            title = os.path.splitext(image_files[2])[0].replace('_', ' ')
            image_path = os.path.join(posters_dir, image_files[2])
            with col3:
                stl.image(image_path, caption=f"3. {title}", width=200)

        if len(image_files) >= 4:
            title = os.path.splitext(image_files[3])[0].replace('_', ' ')
            image_path = os.path.join(posters_dir, image_files[3])
            with col2:
                stl.image(image_path, caption=f"2. {title}", width=200)

        if len(image_files) >= 5:
            title = os.path.splitext(image_files[4])[0].replace('_', ' ')
            image_path = os.path.join(posters_dir, image_files[4])
            with col1:
                stl.image(image_path, caption=f"1. {title}", width=200)
    else:
        stl.write("No Movies Found!")

elif choice == 'Rankings':

    ranking_option = stl.sidebar.selectbox("Select Ranking Option:", ("Top 10", "All Movies"))

    if ranking_option == "Top 10":
        print("")
        c.execute('''SELECT title, 
                    ROUND(((acting + writing + screenplay) * 0.5 
                    + (production + cinematography) * 0.25 
                    + (experience) * 0.25) / 20.50, 2) * 10 AS avg_rating 
                    FROM movies 
                    ORDER BY avg_rating DESC 
                    LIMIT 10''')
        top_movies = c.fetchall()
        if top_movies:
            stl.subheader("Top 10 Rated Movies:")
            for i, (title, rating_average) in enumerate(top_movies, start=1):
                rating_average = round(rating_average, 1) 
                stl.write(f"{i}. {title} - {rating_average}")
        else:
            stl.write("No Movies Found!")

    elif ranking_option == "All Movies":
        print("")
        c.execute('''SELECT title, 
                    ROUND(((acting + writing + screenplay) * 0.5 
                    + (production + cinematography) * 0.25 
                    + (experience) * 0.25) / 20.50, 2) * 10 AS avg_rating 
                    FROM movies 
                    ORDER BY avg_rating DESC''')
        all_movies = c.fetchall()
        if all_movies:
            stl.subheader("All Movies:")
            for i, (title, rating_average) in enumerate(all_movies, start=1):
                rating_average = round(rating_average, 1) 
                stl.write(f"{i}. {title} - {rating_average}")
        else:
            stl.write("No Movies Found!")

elif choice == 'Settings':
    stl.subheader("Settings")
    
    # Submenu for Settings
    setting_option = stl.sidebar.selectbox("Settings Option:", ("Add", "Edit", "Remove"))

    if setting_option == "Add":
        add_movie()
    elif setting_option == "Edit":
        edit_movie()
    elif setting_option == "Remove":
        remove_movie()
else:
    pass
