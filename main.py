import json
import supervisely as sly

# put your values (example is for Community edition) 
# learn more here - https://developer.supervise.ly/getting-started/first-steps/basics-of-authentication
api = sly.Api(server_address="https://app.supervise.ly", token="4r47NFo1ky-long.random.string.here-xaTatb")

# let's test that authentication was successful and we can communicate with the platform
my_teams = api.team.get_list()
print(f"I'm a member of {len(my_teams)} teams")

# get first team and workspace
team = my_teams[0]
workspace = api.workspace.get_list(team.id)[0]

# create on server project with name 'animals' with one dataset with name 'cats'
project = api.project.create(workspace.id, "animals", change_name_if_conflict=True)
dataset = api.dataset.create(project.id, "cats", change_name_if_conflict=True)
print(f"New project {project.id} with one dataset {dataset.id} on server are created")

# lets init one annotation class (rectangle), color is green for visual convenience
cat_class = sly.ObjClass("cat", sly.Rectangle, color=[0, 255, 0])
# lets init one annotation tag, value can be any string 
scene_tag = sly.TagMeta("scene", sly.TagValueType.ANY_STRING)

# init project meta - define classes and tags we are going to label
project_meta = sly.ProjectMeta(obj_classes=[cat_class], tag_metas=[scene_tag])

# set classes and tags in our new empty project on server
api.project.update_meta(project.id, project_meta.to_json())

# upload local image to dataset
image_info = api.image.upload_path(dataset.id, name="my-cats.jpg", path="images/my-cats.jpg")

# init labels (bboxs) for cats and one tag will be assigned to image
cat1 = sly.Label(sly.Rectangle(top=875, left=127, bottom=1410, right=581), cat_class)
cat2 = sly.Label(sly.Rectangle(top=549, left=266, bottom=1500, right=1199), cat_class) 
tag = sly.Tag(scene_tag, value="indoor")

# init annotaiton and then upload it to server
ann = sly.Annotation(img_size=[1600, 1200], labels=[cat1, cat2], img_tags=[tag]) # img_size=[height, width]
api.annotation.upload_ann(image_info.id, ann)

# let's download image and annotation from server
img = api.image.download_np(image_info.id)  # RGB ndarray
print("image shape (height, width, channels)", img.shape)
ann_json = api.annotation.download_json(image_info.id) 
print("annotaiton (default python dict):\n", json.dumps(ann_json, indent=4))