import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from tools.tools import SQLTool

class SQLAgents:
    def __init__(self):
        # Agent that generates and executes queries
        self.generator = Agent(
            role='Make SQL Query',
            goal='Query a MySQL database',
            backstory="""You are an expert at MySQL databases.
                You are given a relational database consisting of tables related by foreign key ids.
                Given a task on a database, you MUST first get a list of all the table names in the database.
                Then, you MUST execute relavant SQL queries to the MySQL database to accomplish the task.""",
            allow_delegation=False,
            tools=[SQLTool().query],
            verbose=True
        )

        # Agent that formats query output into JSON
        self.json_formattor = Agent(
            role='Format data list to JSON',
            goal='Return a JSON object',
            backstory="""You are an expert at converting a list of data to a JSON object.
                Given a list of data, you MUST convert it to a JSON object.""",
            allow_delegation=False,
            verbose=True
        )

        self.format = Task(
            description="""Using the SQL query results provided, format the results to a JSON object.""",
            agent=self.json_formattor
        )
    
    def set_query(self, query):
        self.task = Task(
            description=f"""Make SQL queries to a MySQL database to accomplish the task: {query}""",
            agent=self.generator
        )

    def run_agents(self, query):
        start = time.time()
        self.set_query(query)
        crew = Crew(
            agents=[self.generator, self.json_formattor],
            tasks=[self.task, self.format],
            verbose=2, # Set to 1 or 2 for different logging levels
        )
        result = crew.kickoff()
        end = time.time()
        print("###################### FINAL OUTPUT ######################\n")
        print(result)
        print(f"Task Complete, took {end - start}s")


load_dotenv()
agents = SQLAgents()

while True: 
    query = input("Database Query: ")
    agents.run_agents(query)
