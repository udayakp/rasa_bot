 ## story1
 * greet
 - utter_ask_howcanhelp
 * Reporting Issue
 - utter_checkrefresh
 * deny
 - utter_goodbye


##story2
* greet
 - utter_ask_howcanhelp
 * Reporting Issue{"Report_name": "BI_dashboard","Issue_in":"budget","inputs":"today"}
 - utter_checkrefresh
 * affirm
 - utter_on_it
 - utter_goodbye

##story3
* greet
 - utter_ask_howcanhelp
 * Reporting Issue{"Report_name": "BI_dashboard"}
 - utter_checkrefresh
 * affirm
 - utter_getinput
 *inform{"inputs":"today"}
 - utter_on_it
 -utter_goodbye

##story4
* greet
 - utter_ask_howcanhelp
 * Access Issue{"Report_name": "BI_dashboard"}
 - utter_checkrefresh
 - utter_statuscheck
 * affirm
 - utter_getinput
 *inform{"inputs":"today"}
 - utter_on_it
 -utter_goodbye
