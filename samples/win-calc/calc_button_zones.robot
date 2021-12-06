*** Settings ***
Documentation  Simple test case usign calculator button defined as zones, move the calculator in the top right corner and close it before starting the script

Library         OperatingSystem
Library         ImageLibrary        screenshot_folder=${CURDIR}${/}output

# In Suite Setup keyword init the Image Library with special keyword Init.
Suite Setup 	    On Suite Setup
Suite Teardown      On Suite Teardown

*** Test Cases ***
Basic button usage
    sleep               1
    Press Button        one
    sleep               ${CLICK_DELAY}
    Press Button        two
    sleep               ${CLICK_DELAY}
    Press Button        three
    sleep               ${CLICK_DELAY}
    Press Button        four
    sleep               ${CLICK_DELAY}
    Press Button        five
    sleep               ${CLICK_DELAY}
    Press Button        six
    sleep               ${CLICK_DELAY}
    Press Button        seven
    sleep               ${CLICK_DELAY}
    Press Button        eight
    sleep               ${CLICK_DELAY}
    Press Button        nine
    sleep               ${CLICK_DELAY}
    Press Button        zero

    # Read the zone
    Get Number From Zone     screen
    ${value} = 1234567890
    Should Be Equal     ${value}    1234567890

    # End wait foe convinence
    sleep               5


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
    Init                settings=@{SETTINGS}     references=@{REFERENCES}


On Suite Teardown
    Run   taskkill /IM Calculator.exe /F /T

*** Variables ***
# Delay between click
${CLICK_DELAY}    0.1s
# List with yaml configs
@{SETTINGS}       ${CURDIR}${/}config_zones.yaml
# List with template images dirs
@{REFERENCES}     ${CURDIR}${/}images
