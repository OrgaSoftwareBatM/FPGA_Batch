# Python Environment
Guidelines for Measurement files and analysis Python Part

# General advices
1) Using only one Python environment with Python Version 3.* makes life/debugging easier

2) Commenting your functions and codes as shown below:
3) Please use the python Try-Except Error handling:
```python
def myFunction(*args, **kwargs):
    """
    myFunction reads spec data from hdf5 file

    Parameters
    ----------
    input: 
        filename and path
        
    output : 
        sweeplist, readoutlist
    """
    try:
        # ... load HDF5 file
		return sweeplist, readoutlist

    except Exception as error:
        # WAY 1: more individual
        tb = sys.exc_info()[2]
        print('myFunction.py - ERROR IN LINE '+str(tb.tb_lineno)+':')
        print(error)
        # WAY 2: standard output
        traceback.print_exc()
```

5) Document what you measure, analyse and back up using for instance: Jupyter Notebook, OneNote or similar

# Software and Hacks - to be completed

- Anaconda Software Suite 3.* https://www.anaconda.com/download/
- H5PY: Open Anaconda prompt then: pip install h5py
- Create Shortcuts:
For Open Anaconda Prompt here:
Lookup your Anaconda3 path eg. C:\\ProgramData\\Anaconda3
insert right path (contains pythonw.exe) before and then double click AnacondaPromptHere.reg file
For Ipython Console and Jupyter Notebook 
https://github.com/hyperspy/start_jupyter_cm.git 

- Documentation with Jupyter Notebook/LAB https://github.com/jupyterlab/jupyterlab
- Python for Data Science (Books ISBN: 978-3-527-41315-7 ) or QuickStart Online HowTo
https://www.analyticsvidhya.com/blog/2016/01/complete-tutorial-learn-data-science-python-scratch-2/
