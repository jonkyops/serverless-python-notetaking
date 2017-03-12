# serverless-python-notetaking
Practice project to recreate the tutorial on http://serverless-stack.com/ using python and serverless

## Initial setup
This was mostly set up using Windows 10, but should be pretty platform agnostic. May need to go back and edit this, since this the setup was done in other projects and I may be missing something.

### Folder structure
Using a modification of https://github.com/alexcasalboni/serverless-starter-python. This one seems to have a pretty good separation of the code and serverless, so the code isn't reliant on serverless.

api <-- folder with all the python junk

-- function1 <------------ will be a folder for each function
  
  -- handler.py <--------- wrapper script to call on the function in the lib folder

-- function2 <------------ some other function
  
  -- handler.py <--------- see above

-- function3 <------------ see above
  
  -- handler.py <--------- see above

-- lib <------------------ folder containing the actual, non-serverless code
  
  -- \_\_init\_\_.py <------- module to load the other functions in lib
  
  -- functiongroup1.py <-- contains function1 and function2
  
  -- functiongroup2.py <-- contains function3

-- vendored <------------- git ignored folder containing the python dependencies in requirements.txt

-- requirements.txt <----- list of dependencies that gets installed with pip during deploy

buildspec.yml <----------- buildspec file for deploying with codedeploy

### Side Notes
Initial AWS setup was done using this: https://stelligent.com/2014/02/04/getting-started-with-aws-the-right-way/
Probably want to go back and use something like the NIST cloud formation templates, but this seems to have decent security/logging for now

## Website Steps
Subsections are what I did differently for each of the sections from http://serverless-stack.com/

### Introduction
Nothing needed from here

### Setup your AWS account
Already done

### Setting up the backend
#### Create a DynamoDB Table
Provisioned with the serverless.yml file. Guide uses default settings of 5 read/5 write, but I went with 1/1, since this is just a small project. Had a hard time finding documentation on how to do the cloudformation template for this one, not 100% how composite keys work and how they fit into the dynamodbtable properties. I went with using userID as hash and noteid as range because of this article: http://stackoverflow.com/questions/27085891/create-a-table-in-dynamodb-with-2-columns-as-a-key-composite-keys

(yup, looks like it worked. definitely need to learn more about hash and range)

Doing this through cloudformation also means I had to set up the IAM policy to allow lambda to interact with the table.