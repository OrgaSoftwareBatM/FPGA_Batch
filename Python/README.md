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

10) As soon as you start adding an instrument, please register the new number (on the "Projects" tab for example). This will make merging easier.

# Instruments
This is a non-commercial (for educational purposes only) project based on LabVIEW.
We try to comply with http://www.ni.com/downloads/instrument-drivers/license/ 

The drivers' references/sources are available online at:

- NI FPGA : sbRIO, cRIO, NI RealTime e.g. http://www.ni.com/product-documentation/14031/en/#toc3
- HDF5 file format : http://h5labview.sourceforge.net/

- ADC : NI-DAQmx e.g. http://www.ni.com/download/ni-daqmx-17.0/6624/en/
- ATM DelayLine : MCode driver Schneider electric http://motion.schneider-electric.com/support/mdrive/programs/MCode_LV_86.zip
- AWG : Tektronix AWG700 http://www.tek.com/awg710-0-software/awg700-series-gpib-programming-and-labview-driver
- DAC/DAC_Lock-In : FPGA DAC http://www.ni.com/product-documentation/10622/en/ e.g. Readout FPGA ADC : http://www.ni.com/example/31180/en/
- DSP Lock-In : http://sine.ni.com/apps/utf8/niid_web_display.model_page?p_model_id=1998
- GPIB : https://forums.ni.com/t5/Example-Programs/GPIB-Example-for-LabVIEW/ta-p/3526176
- Keithley K2000 : http://sine.ni.com/apps/utf8/niid_web_display.download_page?p_id_guid=014E6EF883B9743DE0440003BA7CCD71
- LeCroy6050A : http://sine.ni.com/apps/utf8/niid_web_display.model_page?p_model_id=14658
- RF : Rohde Schwarz SMB100A https://www.rohde-schwarz.com/fr/pilote/smb100a/ 
- RF Attenuator : Vaunix http://vaunix.com/products/digital-attenuators/overview/
