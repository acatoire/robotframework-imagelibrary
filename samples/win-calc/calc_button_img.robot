*** Settings ***
Documentation  Simple test case usign calculator button defined as images

Library         OperatingSystem
Library         ImageLibrary        screenshot_folder=${CURDIR}${/}output

# In Suite Setup keyword init the Image Library with special keyword Init.
Suite Setup 	    On Suite Setup
Suite Teardown      On Suite Teardown

*** Test Cases ***
Basic button usage
    sleep               5
    Press Button        menu
    sleep               1
    Press Button        menu
    sleep               1
    Press Button        menu
    sleep               1
    Press Button        menu
    sleep               1
    Press Button        menu


*** Keywords ***
On Suite Setup

    # Start the calculator application
    Run   calc

    # Get window area to specify only the area of a currently running program (Library will use it for zones).
    # If you need the whole window just don't pass argument area to Init keyword.
    # ${windowArea} =

    # Keyword to initialize the Image Library. Pass settings as list with paths to yaml config files, references
    # as list with paths to template images and optional area if you want to work only with currently active window.
    # You need also to specify the area region by using keyword Get Window Area which will automatically detect the
    # active window or pass your own.
    Init                settings=${Settings}     references=${References}


On Suite Teardown
    Run   taskkill /IM Calculator.exe /F /T

*** Variables ***
# List with yaml configs
@{SETTINGS}     ${CURDIR}${/}config_img.yaml
# List with template images dirs
@{REFERENCES}   ${CURDIR}${/}images
