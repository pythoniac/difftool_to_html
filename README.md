# difftool_to_html
compare two files and output the diff to html (python3)

Simply drag and drop two files onto the script and it will output the diff
in form of a html document which is then opened in your standard webbrowser.

You can also start the script from the command line and give the two files as arguments.

The script has been designed to work with binary files but will compare any file format.

The output format of the html can be adjusted in the 'html_template.htm' file. Simply adjust the
'style' section of the document. p-Tag is the format for normal text; d-Tag formats the diff value highlights.

Finally, adjust the global names within the script if you want to (self explanatory, I think):



TEMPLATENAME = html_template.htm
OUTFILENAME = result.htm
