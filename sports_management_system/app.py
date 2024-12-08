from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import os
import mysql.connector
app = Flask(__name__)


app.secret_key = os.urandom(24)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'  #  database host
app.config['MYSQL_USER'] = 'root'  #  MySQL username
app.config['MYSQL_PASSWORD'] = ''  #  MySQL password
app.config['MYSQL_DB'] = 'sports_meeting_db'  #  database name

# Establish a MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

Bootstrap(app)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Display and manage students (Add)
@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    connection = get_db_connection() 
    cursor = connection.cursor()
    
    if request.method == 'POST':  
        firstname = request.form['firstname']
        nationality = request.form['nationality']
        dateofbirth = request.form['dateofbirth']
        cursor.execute("INSERT INTO STUDENT (firstname, nationality, dateofbirth) VALUES (%s, %s, %s)", 
                       (firstname, nationality, dateofbirth))
        connection.commit()  # Commit the transaction using the connection object
        return redirect(url_for('manage_students'))

    # Fetch all students from the database
    cursor.execute("SELECT * FROM STUDENT")
    students = cursor.fetchall()
    cursor.close()  # Always close the cursor
    connection.close()  # Always close the connection
    return render_template('students.html', students=students, student=None)


# Update student (Pre-populate form)
@app.route('/students/update/<int:sid>', methods=['GET', 'POST'])
def update_student(sid):
    connection = get_db_connection()  # Get the database connection
    cursor = connection.cursor()
    
    if request.method == 'POST':  # Handle student update
        firstname = request.form['firstname']
        nationality = request.form['nationality']
        dateofbirth = request.form['dateofbirth']
        cursor.execute("UPDATE STUDENT SET firstname = %s, nationality = %s, dateofbirth = %s WHERE sid = %s", 
                       (firstname, nationality, dateofbirth, sid))
        connection.commit()  # Commit the transaction using the connection object
        return redirect(url_for('manage_students'))
    
    # Fetch student details for the update page
    cursor.execute("SELECT * FROM STUDENT WHERE sid = %s", (sid,))
    student = cursor.fetchone()
    cursor.execute("SELECT * FROM STUDENT")  # Fetch all students
    students = cursor.fetchall()
    cursor.close()  # Always close the cursor
    connection.close()  # Always close the connection
    return render_template('students.html', students=students, student=student)


# Delete student
@app.route('/students/delete/<int:sid>', methods=['GET'])
def delete_student(sid):
    connection = get_db_connection()  
    cursor = connection.cursor()
    cursor.execute("DELETE FROM STUDENT WHERE sid = %s", (sid,))
    connection.commit() 
    cursor.close()  
    connection.close()  # Close the connection after use
    return redirect(url_for('manage_students'))



# Display and manage meetings (Add)
@app.route('/meetings', methods=['GET', 'POST'])
def manage_meetings():
    connection = get_db_connection()  
    cursor = connection.cursor()

    if request.method == 'POST': 
        meetingname = request.form['meetingname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        cursor.execute("INSERT INTO SPORTSMEETING (meetingname, startdate, enddate) VALUES (%s, %s, %s)", 
                       (meetingname, startdate, enddate))
        connection.commit() 
        return redirect(url_for('manage_meetings'))

    # Fetch all meetings from the database
    cursor.execute("SELECT * FROM SPORTSMEETING")
    meetings = cursor.fetchall()
    cursor.close()  # Always close the cursor
    connection.close()  # Always close the connection
    return render_template('meetings.html', meetings=meetings, meeting=None)


# Update meeting (Pre-populate form)
@app.route('/meetings/update/<int:smid>', methods=['GET', 'POST'])
def update_meeting(smid):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch the meeting by SMID for the update form
    cursor.execute("SELECT * FROM SPORTSMEETING WHERE smid = %s", (smid,))
    meeting = cursor.fetchone()

    # If no meeting is found, return an error page or redirect
    if meeting is None:
        return "Meeting not found", 404 
    
    if request.method == 'POST':
        meetingname = request.form['meetingname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        
        # Update the meeting details in the database
        cursor.execute("UPDATE SPORTSMEETING SET meetingname = %s, startdate = %s, enddate = %s WHERE smid = %s", 
                       (meetingname, startdate, enddate, smid))
        connection.commit()
        return redirect(url_for('manage_meetings'))
    
    cursor.close()
    connection.close()

    return render_template('meetings.html', meeting=meeting)



# Delete meeting
@app.route('/meetings/delete/<int:smid>', methods=['GET'])
def delete_meeting(smid):
    connection = get_db_connection()  
    cursor = connection.cursor()
    cursor.execute("DELETE FROM SPORTSMEETING WHERE smid = %s", (smid,))
    connection.commit()  
    cursor.close()  
    connection.close()  
    return redirect(url_for('manage_meetings'))

# Display and manage events (Add)
@app.route('/events', methods=['GET', 'POST'])
def manage_events():
    connection = get_db_connection() 
    cursor = connection.cursor()

    if request.method == 'POST':  # Add event
        eventname = request.form['eventname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        smid = request.form['smid']  
        cursor.execute("""
            INSERT INTO EVENT (eventname, startdate, enddate, smid) 
            VALUES (%s, %s, %s, %s)
        """, (eventname, startdate, enddate, smid))
        connection.commit() 
        return redirect(url_for('manage_events'))

    # Fetch all events along with the sports meeting names
    cursor.execute("""
        SELECT 
            e.eventid, 
            e.eventname, 
            e.smid, 
            e.startdate, 
            e.enddate, 
            sm.meetingname
        FROM EVENT e
        JOIN SPORTSMEETING sm ON e.smid = sm.smid
    """)
    events = cursor.fetchall()

    # Fetch available sports meetings for the form
    cursor.execute("SELECT smid, meetingname FROM SPORTSMEETING")
    sport_meetings = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('events.html', events=events, event=None, sport_meetings=sport_meetings)


@app.route('/events/update/<int:eid>', methods=['GET', 'POST'])
def update_event(eid):
    connection = get_db_connection()  
    cursor = connection.cursor()

    # Fetch event details for the update page
    cursor.execute("SELECT * FROM EVENT WHERE eventid = %s", (eid,))
    event = cursor.fetchone()

    # Fetch available sports meetings for the dropdown
    cursor.execute("SELECT smid, meetingname FROM SPORTSMEETING")
    sport_meetings = cursor.fetchall()

    if request.method == 'POST':  # Handle event update
        eventname = request.form['eventname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        smid = request.form['smid']  

        # Update the event with the new data
        cursor.execute("UPDATE EVENT SET eventname = %s, startdate = %s, enddate = %s, smid = %s WHERE eventid = %s",
                       (eventname, startdate, enddate, smid, eid))
        connection.commit()  
        return redirect(url_for('manage_events'))

    cursor.close()
    connection.close()
    return render_template('events.html', events=None, event=event, sport_meetings=sport_meetings)


# Delete event
@app.route('/events/delete/<int:eid>', methods=['GET'])
def delete_event(eid):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM EVENT WHERE eventid = %s", (eid,))  
    connection.commit()  
    cursor.close()
    connection.close()
    return redirect(url_for('manage_events'))

# CRUD routes for managing matches

@app.route('/matches', methods=['GET', 'POST'])
def manage_matches():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        try:
            # Extract form data
            eventid = request.form['eventid']
            matchdate = request.form['matchdate']

            # Insert a new match without location
            cursor.execute("""
                INSERT INTO `MATCH` (eventid, matchdate) 
                VALUES (%s, %s)
            """, (eventid, matchdate))
            connection.commit()
        except Exception as e:
            print("Error:", e)
            return "Error adding match", 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('manage_matches'))

    # Fetch all matches with meaningful information using JOINs
    cursor.execute("""
        SELECT `MATCH`.matchid, EVENT.eventname, JUDGE.name AS judgename, SPORTSMEETING.meetingname AS sportname, 
               `MATCH`.matchdate
        FROM `MATCH`
        JOIN EVENT ON `MATCH`.eventid = EVENT.eventid
        JOIN JUDGE ON `MATCH`.jid = JUDGE.jid
        JOIN SPORTSMEETING ON `MATCH`.smid = SPORTSMEETING.smid
    """)
    matches = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('matches.html', matches=matches)


@app.route('/matches/update/<int:matchid>', methods=['GET', 'POST'])
def update_match(matchid):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the match details for the update page with related data
    cursor.execute("""
        SELECT `MATCH`.matchid, EVENT.eventname, JUDGE.name AS judgename, SPORTSMEETING.meetingname AS sportname,
               `MATCH`.matchdate, `MATCH`.eventid, `MATCH`.jid, `MATCH`.smid
        FROM `MATCH`
        JOIN EVENT ON `MATCH`.eventid = EVENT.eventid
        JOIN JUDGE ON `MATCH`.jid = JUDGE.jid
        JOIN SPORTSMEETING ON `MATCH`.smid = SPORTSMEETING.smid
        WHERE `MATCH`.matchid = %s
    """, (matchid,))
    match = cursor.fetchone()

    if match is None:
        cursor.close()
        connection.close()
        return "Match not found", 404 

    # Fetch available sports meetings for the dropdown
    cursor.execute("SELECT smid, meetingname FROM SPORTSMEETING")
    sport_meetings = cursor.fetchall()

    if request.method == 'POST':
        try:
            # Extract form data
            eventid = request.form['eventid']
            matchdate = request.form['matchdate']
            smid = request.form['smid'] 

            # Check if the eventid exists in the EVENT table
            cursor.execute("SELECT 1 FROM EVENT WHERE eventid = %s", (eventid,))
            event_exists = cursor.fetchone()

            if not event_exists:
                return "Event not found", 404  

            # Update the match details without location
            cursor.execute("""
                UPDATE `MATCH` 
                SET eventid = %s, matchdate = %s, smid = %s
                WHERE matchid = %s
            """, (eventid, matchdate, smid, matchid))
            connection.commit()
        except Exception as e:
            print("Error:", e)
            return "Error updating match", 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('manage_matches'))

    cursor.close()
    connection.close()

    return render_template('matches.html', match=match, sport_meetings=sport_meetings)



# Route to delete a match
@app.route('/matches/delete/<int:matchid>', methods=['POST'])
def delete_match(matchid):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Delete the match
        cursor.execute("DELETE FROM `MATCH` WHERE matchid = %s", (matchid,))
        connection.commit()
    except Exception as e:
        print("Error:", e)
        return "Error deleting match", 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('manage_matches'))





# Route to manage records (view and add records)
@app.route('/records', methods=['GET', 'POST'])
def manage_records():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == 'POST':
        # Add a new record
        sid = request.form['sid']
        matchid = request.form['matchid']
        record = request.form['record']
        rank = request.form['rank']
        cursor.execute("""
            INSERT INTO `RECORD` (sid, matchid, record, `rank`) 
            VALUES (%s, %s, %s, %s)
        """, (sid, matchid, record, rank))
        connection.commit()
        return redirect(url_for('manage_records'))
    
    # Fetch records with student and match details
    cursor.execute("""
        SELECT RECORD.sid, STUDENT.firstname, STUDENT.nationality, MATCH.matchdate, EVENT.eventname, 
               RECORD.record, RECORD.rank
        FROM RECORD
        JOIN STUDENT ON RECORD.sid = STUDENT.sid
        JOIN `MATCH` ON RECORD.matchid = `MATCH`.matchid
        JOIN EVENT ON `MATCH`.eventid = EVENT.eventid
    """)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('records.html', records=records, record=None)

@app.route('/records/update/<int:sid>', methods=['GET', 'POST'])
def update_record(sid):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Execute the SELECT query to fetch the record based on the sid
    cursor.execute("""
        SELECT RECORD.sid, STUDENT.firstname, MATCH.matchid, RECORD.record, RECORD.rank
        FROM RECORD
        JOIN STUDENT ON RECORD.sid = STUDENT.sid
        JOIN `MATCH` ON RECORD.matchid = `MATCH`.matchid
        WHERE RECORD.sid = %s
    """, (sid,))
    
    # Fetch the record
    record = cursor.fetchone()
    
    '''# Check if the record exists
    if record is None:
        cursor.close()  # Close the cursor if no record is found
        connection.close()  # Close the connection as well
        abort(404)  # Return a 404 error if the record doesn't exist
    '''
    # Handle POST request to update the record
    if request.method == 'POST':
        # Get the updated values from the form
        updated_record = request.form['record']
        updated_rank = request.form['rank']
        
        try:
            # Update the record in the database
            cursor.execute("""
                UPDATE `RECORD` 
                SET record = %s, `rank` = %s 
                WHERE sid = %s
            """, (updated_record, updated_rank, sid))
            
            # Commit the changes to the database
            connection.commit()
        except Exception as e:
            connection.rollback()  
            print("Error during update:", e)
    
    cursor.close()
    connection.close()
    
    # Render the template with the record
    return render_template('records.html', record=record)



# Route to delete a record based on sid
@app.route('/records/delete/<int:sid>', methods=['POST'])
def delete_record(sid):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM `RECORD` WHERE sid = %s", (sid,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('manage_records'))




# CRUD routes for managing judges
@app.route('/judges', methods=['GET', 'POST'])
def manage_judges():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Add new judge
        name = request.form['name']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        cursor.execute("""
            INSERT INTO JUDGE (name, email, phonenumber) 
            VALUES (%s, %s, %s)
        """, (name, email, phonenumber))
        connection.commit()
        return redirect(url_for('manage_judges'))
    
    cursor.execute("SELECT * FROM JUDGE")
    judges = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('judges.html', judges=judges, judge=None)

@app.route('/judges/update/<int:jid>', methods=['GET', 'POST'])
def update_judge(jid):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch judge details for pre-population
    cursor.execute("SELECT * FROM JUDGE WHERE jid = %s", (jid,))
    judge = cursor.fetchone()

    if judge is None:
        cursor.close()
        connection.close()
        return "Judge not found", 404

    if request.method == 'POST':
        # Update judge
        name = request.form['name']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        cursor.execute("""
            UPDATE JUDGE 
            SET name = %s, email = %s, phonenumber = %s 
            WHERE jid = %s
        """, (name, email, phonenumber, jid))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('manage_judges'))
    
    cursor.close()
    connection.close()
    return render_template('judges.html', judges=[], judge=judge)  


# Route to delete a judge
@app.route('/judges/delete/<int:jid>', methods=['POST'])
def delete_judge(jid):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM JUDGE WHERE jid = %s", (jid,))
    connection.commit()

    cursor.close()
    connection.close()
    return redirect(url_for('manage_judges'))

@app.route('/suspensions', methods=['GET', 'POST'])
def manage_suspensions():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == 'POST':
        # Add a new suspension
        sid = request.form['sid']
        details = request.form['details']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        cursor.execute("""
            INSERT INTO SUSPEND (sid, details, startdate, enddate) 
            VALUES (%s, %s, %s, %s)
        """, (sid, details, startdate, enddate))
        connection.commit()
        return redirect(url_for('manage_suspensions'))
    
    # Fetch suspensions with student details
    cursor.execute("""
        SELECT SUSPEND.suspendid, STUDENT.firstname, STUDENT.nationality, SUSPEND.details, SUSPEND.startdate, SUSPEND.enddate
        FROM SUSPEND
        JOIN STUDENT ON SUSPEND.sid = STUDENT.sid
    """)
    suspensions = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('suspensions.html', suspensions=suspensions, suspension=None)
@app.route('/suspensions/update/<int:suspensionid>', methods=['GET', 'POST'])
def update_suspension(suspensionid):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch suspension details with student info
    cursor.execute("""
        SELECT SUSPEND.suspendid, STUDENT.sid, STUDENT.firstname, STUDENT.nationality, SUSPEND.details, SUSPEND.startdate, SUSPEND.enddate
        FROM SUSPEND
        JOIN STUDENT ON SUSPEND.sid = STUDENT.sid
        WHERE suspendid = %s
    """, (suspensionid,))
    suspension = cursor.fetchone()
    
    if suspension is None:
        cursor.close()
        connection.close()
        return "Suspension not found", 404
    
    if request.method == 'POST':
        # Update suspension record
        sid = request.form['sid']
        details = request.form['details']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        cursor.execute("""
            UPDATE SUSPEND 
            SET sid = %s, details = %s, startdate = %s, enddate = %s 
            WHERE suspendid = %s
        """, (sid, details, startdate, enddate, suspensionid))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('manage_suspensions'))
    
    cursor.close()
    connection.close()
    return render_template('suspensions.html', suspensions=[], suspension=suspension)

@app.route('/suspensions/delete/<int:suspensionid>', methods=['POST'])
def delete_suspension(suspensionid):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM SUSPEND WHERE suspendid = %s", (suspensionid,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('manage_suspensions'))


if __name__ == '__main__':
    app.run(debug=True)
