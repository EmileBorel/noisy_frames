"""
    Read cids from a .txt
    Pins them to your Infura app.

"""

import os 


file_path = ""
project_id =""
project_secret = ""


stream = os.popen(
    f"ipfs-copy --cids={file_path} --project-id={project_id} --project-secret={project_secret}")
output = stream.read()


with open("infura_logs", "w") as f:
    f.write(output)


# option 1: all localy hosted
# ipfs-copy --source-api-url=http://localhost:5001 --project-id=<YOUR_PROJECT_ID> --project-secret=<YOUR_PROJECT_SECRET>

# option 2: .txt
# ipfs-copy --cids=/home/xxx/Documents/ipfs-cids.txt --project-id=<YOUR_PROJECT_ID> --project-secret=<YOUR_PROJECT_SECRET>
#https://blog.infura.io/migrate-your-files-to-infuras-new-ipfs-service-in-3-easy-steps/