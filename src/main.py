import os
from dotenv import load_dotenv
import supervisely as sly


print("Load server address and API token from env")
# load .env file with secrets (recommended)
src_dir = os.getcwd()
load_dotenv(os.path.join(src_dir, "debug_secret.env"))
# or init ENVs right in your code
# os.environ["SERVER_ADDRESS"] = "address of your Supervisely instance"
# os.environ["API_TOKEN"] = "your personal api token"

api = sly.Api.from_env()

# let's test that authentication was successful and we can communicate with the platform
my_teams = api.team.get_list()
print(f"I'm the member of {len(my_teams)} teams")

# get the basic information about specific team and workspace
team_id = 331
workspace_id = 508

team = api.team.get_info_by_id(team_id)
print(team)
workspace = api.workspace.get_info_by_id(workspace_id)
print(workspace)

api.project.remove(api.project.get_info_by_name(workspace_id, "my project").id)

# create project, classes and tags
project = api.project.create(workspace.id, "my project")
dataset = api.dataset.create(project.id, "dataset 01")

# init classes
class_cat = sly.ObjClass("cat", sly.Rectangle)
class_dog = sly.ObjClass("dog", sly.Rectangle)
classes = sly.ObjClassCollection([class_cat, class_dog])

# init tags
scene_tag = sly.TagMeta("scene", sly.TagValueType.ONEOF_STRING, ["indoor", "outdoor"])
tags = sly.TagMetaCollection([scene_tag])

# update project classes and tags
project_meta = sly.ProjectMeta(classes, tags)
api.project.update_meta(project.id, project_meta.to_json())

# upload images
im_info1 = api.image.upload_path(dataset.id, "cats.jpg", "images/cats.jpg")
im_info2 = api.image.upload_path(dataset.id, "dog.jpg", "images/dog.jpg")

# upload annotations
