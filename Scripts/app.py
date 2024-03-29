import os
import streamlit as stl
import sqlite3 as sql
from PIL import Image, ImageOps

stl.set_page_config(layout="wide")
connect = sql.connect(r'C:\Users\joelp\python\projects\mms\movies.db')
c = connect.cursor()

def add_movie():
    title = stl.text_input("Title:")
    director = stl.text_input("Director:")
    acting = stl.slider("Acting:", min_value=1, max_value=9, value=5)
    writing = stl.slider("Writing:", min_value=1, max_value=9, value=5)
    production = stl.slider("Production:", min_value=1, max_value=9, value=5)
    screenplay = stl.slider("Screenplay:", min_value=1, max_value=9, value=5)
    cinematography = stl.slider("Cinematography:", min_value=1, max_value=9, value=5)
    experience = stl.slider("Experience:", min_value=1, max_value=9, value=5)

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

def edit_movie():
    title = stl.text_input("Edit:")
    execute_search = stl.button("Search")
    if not title:
        return

    c.execute('''SELECT * FROM movies WHERE title = ?''', (title,))
    movie = c.fetchone()
    if not movie:
        stl.write("Movie Not Found!")
        return
    else:
        title, director, acting, writing, production, screenplay, cinematography, experience = movie

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
        acting = stl.slider("New Rating for Acting:", min_value=1, max_value=9, value=acting)
        writing = stl.slider("New Rating for Writing:", min_value=1, max_value=9, value=writing)
        production = stl.slider("New Rating for Production:", min_value=1, max_value=9, value=production)
        screenplay = stl.slider("New Rating for Screenplay:", min_value=1, max_value=9, value=screenplay)
        cinematography = stl.slider("New Rating for Cinematography:", min_value=1, max_value=9, value=cinematography)
        experience = stl.slider("New Rating for Experience:", min_value=1, max_value=9, value=experience)

        if stl.button("Submit"):
            try:
                c.execute('''UPDATE movies SET acting = ?, writing = ?, production = ?, screenplay = ?, cinematography = ?, experience = ?
                             WHERE title = ?''', (acting, writing, production, screenplay, cinematography, experience, title))
                connect.commit()
                stl.write("Movie Rating Edited Successfully!")
            except sql.IntegrityError:
                stl.write("Movie Already Exists!")
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
                stl.write("Movie Already Exists!")

def remove_movie():
    title = stl.text_input("Title:")
    if stl.button("Remove"):
        c.execute('''DELETE FROM movies WHERE title = ?''', (title,))
        connect.commit()
        stl.write("Movie Removed Successfully!")

def resize_images(directory, output_size=(200, 300)):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            filepath = os.path.join(directory, filename)
            try:
                with Image.open(filepath) as img:
                    img_resized = img.resize(output_size)
                    img_resized.save(filepath)
                    print(f"Resized {filename} successfully")
            except Exception as e:
                print(f"Error resizing {filename}: {e}")

choice = stl.sidebar.selectbox("Select Option:", ("Home", "Explore", "Settings"))

def add_border(image_path, border_size=3, border_color="#B2C8DE"):
    image = Image.open(image_path)
    bordered_image = ImageOps.expand(image, border=border_size, fill=border_color)
    return bordered_image

if choice == 'Home':  
    stl.title("Movie Rating Management Software ([Github](https://github.com/JoelPunniaraj/mms))")
    posters_dir = r'C:\Users\joelp\python\projects\mms\posters'

    c.execute('''SELECT title
                  FROM movies
                  ORDER BY ((acting + writing + screenplay) * 0.5 
                            + (production + cinematography) * 0.25 
                            + (experience) * 0.25) / 20.50 DESC''')
    top_movie_titles = [row[0] for row in c.fetchall()]

    if top_movie_titles:
        stl.subheader("My Top Rated Movies:")
        
        resize_images(posters_dir)

        rows = 10
        cols = 5
        images_per_page = rows * cols

        for i in range(min(len(top_movie_titles), images_per_page)):
            title = top_movie_titles[i].replace('_', ' ')
            image_filename = title + '.jpg'
            image_path = os.path.join(posters_dir, image_filename)

            if os.path.exists(image_path):
                row_index = i // cols
                col_index = i % cols
                if col_index == 0:
                    cols_container = stl.columns(cols)
                with cols_container[col_index]:
                    bordered_image = add_border(image_path)
                    stl.image(bordered_image, caption=title, width=250)
                    
            else:
                stl.write(f"Image not found for {title}")
    else:
        stl.write("No Movies Found!")

elif choice == 'Explore':
    ranking_option = stl.sidebar.selectbox("Select Explore Option:", ("All Movies", "Search"))
    
    if ranking_option == "All Movies":
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

    elif ranking_option == "Search":

        search_query = stl.text_input("Title of the Movie:")
        search_query = search_query.strip()

        if search_query:
            c.execute('''SELECT * FROM movies WHERE title LIKE ?''', ('%' + search_query + '%',))
            movie_details = c.fetchone()

            if movie_details:
                title, director, acting, writing, production, screenplay, cinematography, experience = movie_details

                stl.write(f"<b>Director:</b> {director}", unsafe_allow_html=True)
                stl.write(f"<b>Acting:</b> {acting}", unsafe_allow_html=True)
                stl.write(f"<b>Writing:</b> {writing}", unsafe_allow_html=True)
                stl.write(f"<b>Production:</b> {production}", unsafe_allow_html=True)
                stl.write(f"<b>Screenplay:</b> {screenplay}", unsafe_allow_html=True)
                stl.write(f"<b>Cinematography:</b> {cinematography}", unsafe_allow_html=True)
                stl.write(f"<b>Experience:</b> {experience}", unsafe_allow_html=True)

            else:
                stl.write("Movie not found.")
        else:
            pass

elif choice == 'Settings':
    setting_option = stl.sidebar.selectbox("Settings Option:", ("Add", "Edit", "Remove"))
    stl.subheader(setting_option + " Movie")

    if setting_option == "Add":
        add_movie()
    elif setting_option == "Edit":
        edit_movie()
    elif setting_option == "Remove":
        remove_movie()
else:
    pass
