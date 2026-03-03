import psycopg 
import streamlit as st
import psycopg2
import pandas as pd
import live
import playerstat
import sqlquery
import crudops

connection = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    database = 'cricbuzz',
    password = 'Jalaj@123',
    port = 5432
)

cursor = connection.cursor()
connection.autocommit=True


st.set_page_config(layout="wide")

# create a naviagation side bar
st.sidebar.title("Dashboard")
st.title("Cricbuzz LiveStats")     
select = st.sidebar.radio(
    "select page",
    ["live stats", "player stat","📊sql query","crudops"])


   # title on our main page
if select == live:
    st.title("live stats")
elif select == playerstat:

    playerstat.title()
elif select == "📊sql query":

    st.subheader("🏏 Database Query Questions")


    question_list = [
            "1- Players representing India",
            "2 -Recent matches",
            "3- Top 10 highest run scorers in ODI",
            "4- Venue having capacity of more than 25,000 spectators",
            "5- Win count of each team",
            "6- Count of players belonging to each playing role",
            "7- Highest individual batting score in each format",
            "8- Series started in 2024",
            "9- All rounder player statistics",
            "10- Last 20 completed matches",
            "11- Player performance comparision across different formats",
            "12- Team performance at home vs away",
            "13- Batting partnership of cinsecutive batsmen",
            "14- Bowling performance at different venues",
            "15- Close match performing players",
            "16- Batting perfromance over the year",
            "17- Win when winning the toss",
            "18- Economical bowlers in limited overs",
            "19- Consistent batsmen",
            "20- Matches played in different format by each player",
            "21- Player ranking",
            "22- Head-to-head match prediction analysis between teams",
            "23- Recent form and momentum of player",
            "24- Best player combination",
            "25- Time-series analysis"
        ]
    selection = st.selectbox(
        "☑️ Select a question to analyse",
        question_list
    )
    if selection == question_list[0]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question1()
            st.markdown("📊 Query Result:")
            query1 ="""
                    select
                    id, player_name, playing_role, batting_style, bowling_style
                    from team_india
                """
            players_table = pd.read_sql(query1, connection)

            # display on dashboard
            st.dataframe(players_table, use_container_width=True, hide_index=True)

    elif selection == question_list[1]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
                # sqlquery.question2()
            st.markdown("📊 Query Result:")
        
            query2 = """
                    SELECT 
                    id,
                    description,
                    team1,
                    team2,
                    venue ,
                    city,
                    status
                    FROM recent_matches
                    """
                
                # get data from database table 
            recent_matches = pd.read_sql(query2, connection)

                # display on dashboard
            st.dataframe(
                    recent_matches,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "description" : st.column_config.TextColumn(
                        "description",
                        width= "large"
                        ),
                        "team1" : st.column_config.TextColumn(
                        "Team 1"
                        ),
                        "team2" : st.column_config.TextColumn(
                        "Team 2"
                        ),
                        "venue" : st.column_config.TextColumn(
                        "Venue"
                        ),
                        "match_city" : st.column_config.DateColumn(
                        "city"
                        ),
                        "match_status" : st.column_config.DateColumn(
                        "status"
                        )
                    }
                )
# QUESTION 3
    elif selection == question_list[2]:
        st.markdown(f"#### {selection}")

        if st.button("🏃🏻‍➡️ Execute Query", use_container_width=True):
            st.markdown("### 📊 Query Result:")
            # sqlquery.question3()
            query3 = """
                select 
                player_id,
                player_name,
                runs,
                matches,
                innings,
                average
                from odi_scorers
                limit 10
                """
            # get data from database table 
            odi_scorers = pd.read_sql(query3, connection)

            # display on dashboard
            st.dataframe(
                odi_scorers,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name" : st.column_config.TextColumn(
                        "player Name"
                    ),
                    "runs" : st.column_config.TextColumn(
                        "Runs Scored"
                    ),
                    "average" : st.column_config.TextColumn(
                        "Batting Average"
                    ),
                    "innings" : st.column_config.TextColumn(
                        "Innings Played"
                    )
                }
            )
 # QUESTION 4

    elif selection == question_list[3]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question4()
            st.markdown("📊 Query Result:")
            query4 = """
                        select 
                        id,
                        ground_name,
                        city,
                        country,
                        capacity
                        from venue_capacity
                    """
            # get data from database table 
            venue_capacity = pd.read_sql(query4, connection)
            st.dataframe(
                        venue_capacity,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "groundname" : st.column_config.TextColumn(
                                "Ground Name"
                            ),
                            "city" : st.column_config.TextColumn(
                                "City"
                            ),
                            "country" : st.column_config.TextColumn(
                                "Country"
                            ),
                            "capacity" : st.column_config.TextColumn(
                                "Capacity"
                            )
                        }
                    )   
# QUESTION 5
    elif selection == question_list[4]:
        st.markdown(f"#### {selection}")
            
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question5()
            st.markdown("📊 Query Result:")
            query5 = """
                    select 
                    team_name,
                    total_wins
                    from team_wins
                    order by total_wins desc
                """
                # get data from database table 
            team_wins = pd.read_sql(query5, connection)
            st.dataframe(
                team_wins,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "team" : st.column_config.TextColumn(
                        "Team Name"
                    ),
                    "wincount" : st.column_config.TextColumn(
                        "Count of wins"
                    )
                }
            )

 # QUESTION 6
    elif selection == question_list[5]:
        st.markdown(f"#### {selection}")
        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question6()
            st.markdown("📊 Query Result:")
            query6 = """
                select 
                id,
                player_name,
                playing_role
                from team_india  
            """
            # get data from database table 
            team_india = pd.read_sql(query6, connection)

            # display on dashboard
            st.dataframe(
                team_india,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "player_name" : st.column_config.TextColumn(
                        "Player name"
                    ),
                    "playing_role" : st.column_config.TextColumn(
                        "playing role"
                    )
                }
            )
 # QUESTION 7
    elif selection == question_list[6]:
        st.markdown(f"#### {selection}")

        if st.button("🏃🏻‍➡️ Execute Query"):
            # sqlquery.question7()
            st.markdown("📊 Query Result:")
            query7 = """
                select 
                player_id,
                player_name,
                test_value,
                odi_value,
                t20_value
                from test_odi_t20
                """
            # get data from database table 
            test_odi_t20 = pd.read_sql(query7, connection)

            # display on dashboard
            st.dataframe(
                test_odi_t20,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "player_id" : st.column_config.TextColumn(
                        "Format"
                    ),
                    "player_name" : st.column_config.TextColumn(
                        "Highest Score"
                    ),
                    "test_value" : st.column_config.TextColumn(
                        "Highest Score"
                    ),
                    "odi_value" : st.column_config.TextColumn(
                        "Highest Score"
                    ),
                    "t20_value" : st.column_config.TextColumn(
                        "Highest Score"
                    )
                }
            )
 
                    


    
elif select == "crudops":
    st.title("CRUD Operations")
# when CRUDs page selected

    crudops.title()

    choice = st.selectbox(
        "Chose an operation:",
        ["➕Create (Add Player)", "📖Read (Load Players)", "🖊️Update player (Edit Player)", "🗑️Delete (Remove Player)"]
    )

    if choice == "➕Create (Add Player)":
        # crudops.create()
        crudops.add()
    
    elif choice == "📖Read (Load Players)":
        crudops.read()

    elif choice == "🖊️Update player (Edit Player)":
            crudops.update()

    elif choice == "🗑️Delete (Remove Player)":
            crudops.delete()

