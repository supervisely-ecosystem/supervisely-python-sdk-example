import os
from dotenv import load_dotenv
from datetime import datetime
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

# just to run the scipt multiple times, to avoid name conflicts and to keep this script simple  
current_dt = datetime.now().strftime("%m-%d-%Y %H-%M-%S")

# create structure - team, workspace, project, dataset
team = api.team.create(f"my team {current_dt}")
workspace = api.workspace.create(team.id, f"my workspace {current_dt}")
print(team, '\n', workspace)

# create project, classes and tags
project = api.project.create(workspace.id, "my project")
dataset = api.dataset.create(project.id, "dataset 01")

# init classes
class_cat = sly.ObjClass("cat", sly.Rectangle, color=[0, 255, 0])
class_dog = sly.ObjClass("dog", sly.Rectangle, color=[255, 0, 0])
classes = sly.ObjClassCollection([class_cat, class_dog])

# init tags
scene_tag = sly.TagMeta("scene", sly.TagValueType.ONEOF_STRING, ["indoor", "outdoor"])
tags = sly.TagMetaCollection([scene_tag])

# update project classes and tags to server
project_meta = sly.ProjectMeta(classes, tags)
api.project.update_meta(project.id, project_meta.to_json())

# upload images
image_info1 = api.image.upload_path(dataset.id, "cats.jpg", "images/cats.jpg")
image_info2 = api.image.upload_path(dataset.id, "dog.jpg", "images/dog.jpg")

# prepare annotation for the first image
cat1 = sly.Label(sly.Rectangle(top=875, left=127, bottom=1410, right=581), class_cat)
cat2 = sly.Label(sly.Rectangle(top=549, left=266, bottom=1199, right=1499), class_cat) 
tag_img1 = sly.Tag(scene_tag, "indoor")
ann1 = sly.Annotation(img_size=[1600, 1200]) # height x width
ann1 = ann1.add_labels([cat1, cat2]) # Note: most objects in SDK are immutable 
ann1 = ann1.add_tags([tag_img1])
api.annotation.upload_ann(image_info1.id, ann1)

# prepare annotation for the first image
dog1 = sly.Label(sly.Rectangle(top=580, left=295, bottom=857, right=576), class_dog)
tag_img2 = sly.Tag(scene_tag, "outdoor")
ann2 = sly.Annotation(img_size=[1080, 810]) # height x width
ann2 = ann2.add_label(dog1)
ann2 = ann2.add_tag(tag_img2)
api.annotation.upload_ann(image_info2.id, ann2)