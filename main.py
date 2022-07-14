import supervisely as sly

api = sly.Api(server_address="dfsdfsdf", token="dfsfsd")

# let's test that authentication was successful and we can communicate with the platform
my_teams = api.team.get_list()
print(f"I'm the member of {len(my_teams)} teams")

# get first team and workspace
team = my_teams[0]
workspace = api.workspace.get_list(team.id)[0]

# create project, classes and tags on server # TODO describe
project = api.project.create(workspace.id, f"animals", change_name_if_conflict=True)
dataset = api.dataset.create(project.id, f"cats", change_name_if_conflict=True)

# lets init two !!! annotation classes !!! of shape rectangles with green and red borders # TODO describe
class_cat = sly.ObjClass("cat", sly.Rectangle, color=[0, 255, 0])
scene_tag = sly.TagMeta("scene", sly.TagValueType.ANY_STRING)

# init project meta - classes and tags we are going to label?????
project_meta = sly.ProjectMeta([classes], [tags]) # - class and tags can be lists #TODO

# update project classes and tags to server
api.project.update_meta(project.id, project_meta.to_json())

# upload images to dataset
image_info = api.image.upload_path(dataset.id, "cats.jpg", "images/cats.jpg")

# prepare annotation for the first image
cat1 = sly.Label(sly.Rectangle(top=875, left=127, bottom=1410, right=581), class_cat)
cat2 = sly.Label(sly.Rectangle(top=549, left=266, bottom=1500, right=1199), class_cat) 
tag_img1 = sly.Tag(scene_tag, "indoor")
ann1 = sly.Annotation(img_size=[1600, 1200], labels=[cat1, cat2], tags=[tag_img1]) # height x width #TODO allow to input lists
api.annotation.upload_ann(image_info.id, ann1)

# let's download images and annotations
img1 = api.image.download_np(image_info1.id)  # RGB
print("width, height and channels of image "img1.shape, "\n", img2.shape) # delete?
ann1_json = api.annotation.download_json(image_info1.id) 
print("dict???:", ann1_json)