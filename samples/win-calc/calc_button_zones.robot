*** Settings ***
Documentation  Simple test case usign calculator button defined as zones, move the calculator in the top right corner and close it before starting the script

Library         OperatingSystem
Library         ImageLibrary        screenshot_folder=${CURDIR}${/}output
Library         String

# In Suite Setup keyword init the Image Library with special keyword Init.
Suite Setup 	    On Suite Setup
Suite Teardown      On Suite Teardown
Test Setup 	        On Test Setup

*** Test Cases ***

1- Basic all buttons usage
    sleep               1
    Press Button        one
    Press Button        two
    Press Button        three
    Press Button        four
    Press Button        five
    Press Button        six
    Press Button        seven
    Press Button        eight
    Press Button        nine
    Press Button        zero

    # Read the zone
    ${value}            Get Number From Screen
    Log                 Calculator text screen is: ${value}
    Should Be Equal     ${value}                   ${1234567890}

    # End wait for convinence
    sleep               3

2- Small integer calcul failed
    sleep               1
    Press Button        seven
    Press Button        plus
    Press Button        three
    Press Button        minus
    Press Button        five
    Press Button        equal

    # Read the zone
    ${value}            Get Number From Screen

    Should Be Equal     ${value}                   ${2}


    # End wait for convinence
    sleep               3

3- Small float calcul passed
    sleep               1
    Press Button        one
    Press Button        divide
    Press Button        four
    Press Button        multiply
    Press Button        five
    Press Button        equal

    # Read the zone
    # ${value}            Get Float Number From Zone       screen small     # Do not work on
    ${value}            Get Number From Screen

    Should Be Equal     ${value}                         ${1.25}

    # End wait for convinence
    sleep               3

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


On Test Setup
    # Start the calculator application
    Press Button        clear
    sleep               1

Get Number From Screen
    # I had issue with "Get Number From Zone" and "Get Float Number From Zone"
    # Sometimes no reconition
    # Issue with coma in french numbers

    ${value}    Get Text From Zone       screen
    ${value}    Replace String           ${value}       ,       .
    ${value}    Convert To Number        ${value}

    [return]      ${value}

*** Variables ***
# Delay between click
${CLICK_DELAY}    0s
# List with yaml configs
@{SETTINGS}       ${CURDIR}${/}config_zones.yaml
# List with template images dirs
@{REFERENCES}     ${CURDIR}${/}images
