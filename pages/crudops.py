import streamlit as st
import psycopg2
import pandas as pd
import requests

# creating SQL connection

con = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    database = 'cricbuzz',
    password = 'Jalaj@123',
    port = 5432
)

cursor = con.cursor()
con.autocommit=True

def title():
    st.markdown("#### 🗒️ Create, Read, Update, Delete Player records")

def create():
    st.markdown("#### 🏗️ Create/Re-create the player stats table")
    if st.button("Re-create Table from API"):
        try:
            cursor.execute("drop table if exists cruds_table")
            cursor.execute("""
                create table cruds_table (
                id int,
                name varchar(50),
                matches int,
                overs float,
                wickets int,
                economy float
                )
            """)
            insertCRUDs = """
                insert into cruds_table values
                (%s,%s,%s,%s,%s,%s)
            """

            url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"
            querystring = {"statsType":"lowestEcon","matchType":"1"}
            headers = {
                "x-rapidapi-key": "26ac642350msh32a0dd01efaadf5p102886jsnc1f3d91af0ab",
                "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # This will raise an exception for HTTP errors

            datacruds = response.json()

            # For debugging, let's see the response
            st.write("API Response:")
            st.json(datacruds)

            if 'values' in datacruds:
                for i in datacruds['values']:
                    row = i.get('values', [])
                    if row:
                        cursor.execute(insertCRUDs, row)
                st.success("Table 'cruds_table' created and populated successfully!")
            else:
                st.warning("The API response did not contain 'values'. No data was inserted.")

        except requests.exceptions.RequestException as e:
            st.error(f"API Request failed: {e}")
        except (psycopg2.Error, KeyError, IndexError) as e:
            st.error(f"An error occurred: {e}")


def add():
    st.markdown("#### ➕ Add a new player")

    col1, col2 = st.columns(2)

    with col1:
        id = st.number_input("Player ID", min_value=0, step=1, key="add_id")
        name = st.text_input("Player Name", placeholder= "enter player name", key="add_name")
        matches = st.number_input("Matches", min_value=0, step=1, key="add_matches")

    with col2:
        overs = st.number_input("Overs", key="add_overs")
        wickets = st.number_input("Wickets", min_value=0, step=1, key="add_wickets")
        economy = st.number_input("Economy", key="add_economy")

    if st.button("➕Add Player"):
        try:
            insertCRUDs = """
                insert into cruds_table values
                (%s,%s,%s,%s,%s,%s)
            """
            row = (id, name, matches, overs, wickets, economy)

            cursor.execute(insertCRUDs, row)
            st.success(f"Player '{name}' added successfully!")
        except psycopg2.Error as e:
            st.error(f"Database error: {e}")


def read():
    st.markdown("#### 📖 View All Players")

    if st.button("📊 Load All Players"):
        try:
            query = "select * from cruds_table"
            data = pd.read_sql(query, con)
            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True
            )
        except Exception as e:
            st.error(f"An error occurred while reading the data: {e}")

def update():
    st.markdown("##### ✏️ Update player information")

    player_name_to_update = st.text_input(
        "🔍 Search for player to update:",
        placeholder= "enter player name",
        key="update_search"
    )

    if player_name_to_update:
        try:
            queryget2 = "select name, id, wickets, matches, economy, overs from cruds_table where name = %s"
            df1 = pd.read_sql(queryget2, con, params=(player_name_to_update,))

            if not df1.empty:
                df = df1.iloc[0]
                pname = df['name']
                pmatches = df['matches']
                povers = df['overs']
                pwickets = df['wickets']
                peco = df['economy']
                Id = df['id']

                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input("Player Name", value=pname, key="update_name")
                    matches = st.number_input("Matches", value=pmatches, step=1, key="update_matches")
                    overs = st.number_input("Overs", value=povers, key="update_overs")

                with col2:
                    wickets = st.number_input("Wickets", value=pwickets, step=1, key="update_wickets")
                    economy = st.number_input("Economy", value=peco, key="update_economy")

                if st.button("Update Player"):
                    update_query = """
                        update cruds_table
                        set name = %s, matches = %s, overs = %s, wickets = %s, economy = %s
                        where id = %s
                    """
                    cursor.execute(update_query, (name, matches, overs, wickets, economy, Id))
                    st.success(f"Player '{name}' updated successfully!")
            else:
                st.warning("No player with this name found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

def delete():
    st.markdown("##### 🗑️ Delete a player")

    player_name_to_delete = st.text_input(
        "🔍 Search Player to delete",
        placeholder= "enter full name of player",
        key="delete_search"
    )

    if player_name_to_delete:
        try:
            queryget = "select name, id, wickets from cruds_table where name = %s"
            df = pd.read_sql(queryget, con, params=(player_name_to_delete,))

            if not df.empty:
                df['disp'] = (
                    df['name'] +
                    " (ID : " + df['id'].astype(str) + ")" +
                    " - " + df['wickets'].astype(str) + " wickets"
                )
                selected_player_disp = st.selectbox(
                    "Select player to delete:",
                    df['disp']
                )
                
                selected_id = int(df[df['disp'] == selected_player_disp]['id'].iloc[0])


                confirmation = st.text_input(
                    f"Type DELETE to permanently delete {selected_player_disp}"
                )

                if confirmation == 'DELETE':
                    del_query = "delete from cruds_table where id = %s"
                    cursor.execute(del_query, (selected_id,))
                    st.success(f"Player '{selected_player_disp}' has been deleted.")
                    # Also need to make streamlit rerun to clear the selectbox
                    st.experimental_rerun()

            else:
                st.warning("No player with this name found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
