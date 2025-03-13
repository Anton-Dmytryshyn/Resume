*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${website}    https://the-internet.herokuapp.com
${browser}    Chrome
${last_name_header}    //table[@id='table2']//th[span[text()='Last Name']]

*** Test Cases ***
Making sure that sorting ascending and descending works fine
    [Documentation]  This test case checks, if sorting works correctly, by clicking on table column name
    [Tags]    TC-1
    Open Browser  ${website}    ${browser}
    Wait Until Element Is Visible    //a[text()='Sortable Data Tables']
    Click Element    //a[text()='Sortable Data Tables']
    Wait Until Element Is Visible    ${last_name_header}
    Click Element    ${last_name_header}
    Verify Sort Order Last Name    Ascending
    Click Element    ${last_name_header}
    Verify Sort Order Last Name    Descending



*** Keywords ***
Verify Sort Order Last Name
    [Arguments]    ${order}
    ${elements}=    Get Webelements    //table[@id='table2']//tr/td[1]
    ${elements_list}=    Create List
    FOR   ${element}    IN    @{elements}
    ${element_text}=    Get Text    ${element}
    Append To List    ${elements_list}    ${element_text}
    END
    IF    '${order}' == 'Ascending'
    ${order}    Set Variable    False
    END
    IF    '${order}' == 'Descending'
    ${order}    Set Variable    True
    END
    ${sorted_elements_list}=  Evaluate    sorted(${elements_list}, reverse=${order})
    ${are_lists_equal}=  Evaluate    ${sorted_elements_list} == ${elements_list}
    Should Be Equal    ${are_lists_equal}    ${True}