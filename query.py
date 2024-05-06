import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from tools.tools import SQLTool


start = time.time()
load_dotenv()

INPUT = "Give me all the data for user with first_name 'Super'."

generator = Agent(
	role='Make SQL Query',
	goal='Query a MySQL database',
	backstory="""You are an expert at MySQL relational databases.
		The database consists of tables that are related through foreign key ids.
    	Given a task on a database, you MUST first get a list of all the table names in the database.
        Then, you MUST execute a SQL query to the MySQL database to accomplish the task.""",
	allow_delegation=False,
    tools=[SQLTool().query],
    verbose=True
	# llm=language_model
)

json_formattor = Agent(
    role='Format data list to JSON',
    goal='Return a JSON object',
    backstory="""You are an expert at converting a list of data to a JSON object.
    	Given a list of data, you MUST convert it to a JSON object.""",
    allow_delegation=False,
    verbose=True
    # llm=language_model
)

task1 = Task(
    description=f"""Make a SQL query to a MySQL database called 'command_centerdb' to accomplish the task: {INPUT}""",
    agent=generator
)

task2 = Task(
    description="""Using the SQL query results provided, format the results to a JSON object.""",
    agent=json_formattor
)

# Instantiate your crew with a sequential process
crew = Crew(
	agents=[generator, json_formattor],
	tasks=[task1, task2],
	verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()
end = time.time()
print("###################### FINAL OUTPUT ######################\n")
print(result)
print(f"Process took {end - start}s")
