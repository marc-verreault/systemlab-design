
SystemLab|Design installation
=============================

SystemLab|Design is delivered as a ready-to-use, bundled program that includes pre-installed
libraries for:

* Python 3.7.3
* PyQt 5.12.2(GPLv3)/Qt 5.12.3(LGPLv3) (GUI interface)
* NumPy (1.16.3) (mathematical operations and signal array manipulation)
* Matplotlib (3.0.3) (data viewers and customized graphs)
* SciPy (1.2.1) (specialized numerical procedures)
* Scintilla/SciTE (4.1.4) (integrated Python script editor)

  .. note::
    Please note that SystemLab|Design is only currently supported on Windows 10.

To install and run SystemLab|Design, complete the following steps:

1. Download the latest version of SystemLab|Design from: 
   https://systemlabdesign.com/systemlab_design/systemlab_design_1902.zip

  .. note::   
    If prompted by your web browser, select the "Save file" option.
      
2. Extract the contents of the zip folder to any location on your computer (right-click 
   on the zipped folder and select **Extract All...** followed by **Extract**).
3. Once the extraction is complete (Fig 1), you will see the folder *systemlab_design* 
   (this is main operating folder for the application). If desired, you can drag and drop 
   this folder to any other location on your computer.
   
  .. figure:: Installation_1.png
    :figclass: align-center
    :width: 350
    
    Fig 1: Completion of folder extraction "systemlab_design".  
   
4. Double left-click on the *systemlab_design* folder and scroll down the folder/file list 
   until you see the application file *SystemLab-Design.exe* (see Fig 2).
   
  .. figure:: Installation_2.png
    :figclass: align-center
    :width: 550  
    
    Fig 2: How to launch the SystemLab|Design application. For this procedure we moved the 
    folder to the Windows Desktop
    
5. **Double left-click** on the application file to launch the software (or optionally 
   **right-click + open**).   
6. **Windows Defender SmartScreen** (or similar anti-virus software) will likely initially 
   flag *"SystemLab-Design.exe"* as an unrecognized app (this is normal as it has 
   been downloaded from the internet). Select **More Info** to verify the publisher.
   
  .. note::   
    The SmartScreen flag should only appear once after downloading the SystemLab|Design application 
    from an internet connection. After local installation, it should run normally on your 
    computer without further warnings.
    
  .. figure:: Installation_3.png
    :figclass: align-center
    :width: 350
    
    Fig 3: Windows Defender SmartScreen. Publisher should show **SystemLab Inc.**
    
7. The publisher should indicate *SystemLab Inc.* (Fig 3), the issuer of the Digital Signature 
   certificate, thus verifying the source and integrity of the software. Once the publisher 
   is verified, select **Run anyway** to launch the application. 
   
   *For further information on digital signature see the section below: About software digital signatures...*. 
   **Note**: If the publisher field displays unknown, **we do not recommend** that you launch the 
   application. Please contact us at info@systemlabdesign.com for assistance.
   
  .. note::   
    When launching SystemLab|Design for the first time there will be an initial delay (~15 seconds) 
    before the application appears (Fig 5) (during this time Python compiles the code into bytecode 
    (.pyc files)). After these cached files are built, subsequent instances of the 
    application will load more quickly.
   
  .. admonition:: About software digital certificates...
     
     Software code signing is an industry best practice used to ensure users 
     of the integrity and identity (source) of online software. SystemLab Inc. digitally 
     signs its SystemLab|Design application software through 
     `K-Software <http://www.ksoftware.net>`_/`Sectigo <https://sectigo.com/>`_ RSA Code Signing 
     for `Microsoft Authenticode <https://docs.microsoft.com/en-us/windows-hardware/drivers/install/authenticode>`_.
         
     You can thus verify that the downloaded software application was not altered 
     after publication on our server and that the application executable came directly from us 
     (SystemLab Inc.). For futher information on our digital signature, open the **Properties** of 
     *SystemLab-Design.exe*, go to the tab **Digital Signatures**, left-click select the 
     line for **SystemLab Inc** (name of signer) and click on **Details** (Fig 4).
     
     If you have any questions or concerns on the digital signature information, please don't 
     hesitate to contact us at info@systemlabdesign.com.
     
  .. figure:: Installation_4.png
    :figclass: align-center
    :width: 550  
    
    Fig 4: Digital Signature information for publisher **SystemLab Inc.**
    
  .. important::
    With the exception of SystemLab|Design project folders or application examples, it is 
    not recommended to move any folders or files outside of the main "systemlab_design"
    directory as this may cause portions of the software to work incorrectly.
    
  .. figure:: Installation_App.png
    :figclass: align-center
    
    Fig 5: SystemLab|Design application GUI.
    
