This script reads monthly statements from Questrade and renames them to YYYYMM_{AccoutNum}_{AccountType}_{FirstNameInitial}{LastNameInital}.pdf where AccountType options are RRSP, TFSA, RESP and Margin.

When downloading statements from Questade, their default format is statement.pdf. If you download more than one statement, the next statement will be renamed to statement(01).pdf. I have 7 monthly statements for our household so this is cumbersome.

Place the statement(x).pdf in the root directory, run the script and all of the pdfs will get renamed.