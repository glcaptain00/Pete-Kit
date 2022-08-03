############################################
# Step 1: Perform initial setup of devices #
############################################
import boto3
import cv2
from datetime import datetime

#Configuration
bucketName = "pete-object-detection-bucket" #This must fit S3's naming conventions
region = "us-east-2"

#Setup camera
cam = cv2.VideoCapture(0)

#Create the necessary boto3 clients
s3client = boto3.client('s3', region_name=region)
rekoclient = boto3.client('rekognition')


###########################################################
# Step 2: Create an S3 bucket if it doesn't already exist #
###########################################################
# Get a list of buckets, then filter the JSON response to only include the buckets
bucketResponse = s3client.list_buckets()["Buckets"]

#Variable to track whether to create the bucket or not
needsCreation = True
#For loop, looping from 0 to the number of buckets in the list.
for i in range(len(bucketResponse)):
	if bucketResponse[i]["Name"] == bucketName:
		needsCreation = False
		break
if needsCreation:
	createRes = s3client.create_bucket(
		Bucket=bucketName,
		CreateBucketConfiguration={'LocationConstraint': region},
		ACL='private'
	)
	print(createRes)
	privateRes = s3client.put_public_access_block( #This method will make the new bucket private
		Bucket=bucketName,
		PublicAccessBlockConfiguration={
			'BlockPublicAcls': True,
			'IgnorePublicAcls': True,
			'BlockPublicPolicy': True,
			'RestrictPublicBuckets': True
		}
	)
else:
	print(f"Bucket {bucketName} already exists")


##########################
# Step 3: Take a picture #
##########################
ret, image = cam.read() #ret is true if the frame was read correctly, false otherwise. image is the frame itself.
filename = datetime.now().strftime("%m-%d-%YT%H-%M-%S.png")
cv2.imwrite(f'./images/{filename}', image)

############################
# Step 4: Upload the image #
############################
print("Reading file...")
img = open(f"./images/{filename}","rb")
print("Uploading file...")
s3client.put_object(
	Bucket=bucketName,
	Body=img,
	Key=filename
)

###############################################
# Step 5: Tell Rekognition to label the image #
###############################################
labels = rekoclient.detect_labels(
	Image={
		'S3Object': {
			'Bucket': bucketName,
			'Name': filename
		}
	}
)

#######################################################
# Step 6: Print the labels in a human readable format #
#######################################################
for item in labels['Labels']:
	# Print a format string (specified with f)
	# For the first format, print item[Confidence] as a float with a rounding to 2 decimal places
	# For the second format, print item[Name]
	print(f"I am {item['Confidence']:0.2f}% sure that I see a {item['Name']}")
