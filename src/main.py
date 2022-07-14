import os
from dotenv import load_dotenv
import supervisely as sly


print("Load server address and API token from env")
# load .env file with secrets (recommended)
load_dotenv(os.path.join(os.getcwd(), "debug_secret.env"))
# or init ENVs right in your code
# os.environ["SERVER_ADDRESS"] = "address of your Supervisely instance"
# os.environ["API_TOKEN"] = "your personal api token"

api = sly.Api.from_env()

# let's test that authentication was successful and we can communicate with the platform
my_teams = api.team.get_list()
for team_info in my_teams:
    print(team_info.id, team_info.name)
