# FPGA_Batch
Instrument control and analysis software. Measurement files and analysis are done in Python, instrument control is in Labview.

# General rules
1) Create 1 development fork per person (for example Baptiste-Dev, Everton-Dev or Sionludi-Dev) or one per main project (New-FPGA-Dev).

2) Direct commits to the master branch are disabled, only commit to your own branch. Update master branch via pull request from your personal fork, and only after proper tests and debuging. 

3) Someone else should be responsible for checking the added parts (and the debuging) and accepting the pull request.

4) Updating the code while running an experiment is not mandatory, but if you develop something new you need to either start from the last "master" version or make sure it will be compatible.

5) Please comment your commits.

6) The gitignore file prevents .pyc files from being commited. Please make sure not to upload useless (or setup-dependant) files. 

7) We should keep a clear version number for both the Python and the Labview part. Ideally with a clear changelog that matches the 2.

8) The "Projects" tab is here to share your on-going and future development ideas.

9) If you modify something in your code and don't want to commit it, please at least write the changes in the "Projects" tab, instead of trusting oral transmission.

10) As soon as you start adding an instrument, please register the new number (on the "Prjects" tab for example). This will make merging easier.
